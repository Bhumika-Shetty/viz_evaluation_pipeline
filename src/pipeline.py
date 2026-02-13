"""
Main Pipeline for AI Visualization Evaluation

This pipeline:
1. Calls an AI model API to generate visualization code
2. Executes the code (with 3 attempts/retries)
3. Calculates evaluation metrics
4. Saves results with proper naming
"""

import os
import sys
import json
import yaml
import logging
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import re
import requests
import subprocess
import shutil

# Import local modules
from .prompts import get_titanic_prompt, get_dataset_prompt
from .metrics import calculate_metrics_for_visualization

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VisualizationPipeline:
    """Main pipeline for AI visualization generation and evaluation"""

    def __init__(self, config_path: str = "../config/config.yaml"):
        """
        Initialize the pipeline

        Args:
            config_path: Path to configuration file
        """
        self.config = self.load_config(config_path)
        self.results = []
        self.setup_directories()

    def load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Loaded configuration from {config_path}")
            return config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            raise

    def setup_directories(self):
        """Create necessary output directories"""
        dirs = [
            self.config['outputs']['visualizations_dir'],
            self.config['outputs']['metrics_dir'],
            self.config['outputs']['logs_dir']
        ]

        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {dir_path}")

    def call_ollama_api(self, prompt: str, model: str = None) -> str:
        """
        Call Ollama API to generate code

        Args:
            prompt: The visualization prompt
            model: Model name (defaults to config)

        Returns:
            str: Generated code
        """
        if model is None:
            model = self.config['model']['name']

        api_base = self.config['model']['api_base']
        url = f"{api_base}/api/generate"

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.config['model']['temperature']
            }
        }

        try:
            logger.info(f"Calling Ollama API with model: {model}")
            response = requests.post(url, json=payload, timeout=300)
            response.raise_for_status()

            result = response.json()
            generated_text = result.get('response', '')

            logger.info(f"Received response from API ({len(generated_text)} characters)")
            return generated_text

        except requests.exceptions.RequestException as e:
            logger.error(f"API call failed: {e}")
            raise

    def call_openai_compatible_api(self, prompt: str, model: str = None) -> str:
        """
        Call OpenAI-compatible API (for other providers)

        Args:
            prompt: The visualization prompt
            model: Model name

        Returns:
            str: Generated code
        """
        if model is None:
            model = self.config['model']['name']

        # This can work with OpenAI, Together AI, etc.
        # Requires API key in environment variable

        try:
            import openai

            client = openai.OpenAI(
                base_url=self.config['model'].get('api_base'),
                api_key=os.getenv('OPENAI_API_KEY', 'dummy-key')
            )

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert data visualization specialist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config['model']['temperature']
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"OpenAI-compatible API call failed: {e}")
            raise

    def extract_code_from_response(self, response: str) -> str:
        """
        Extract Python code from API response

        Args:
            response: Raw API response

        Returns:
            str: Extracted Python code
        """
        # Look for code blocks
        code_block_pattern = r'```python\n(.*?)```'
        matches = re.findall(code_block_pattern, response, re.DOTALL)

        if matches:
            return matches[0].strip()

        # Alternative: look for any code block
        code_block_pattern = r'```\n(.*?)```'
        matches = re.findall(code_block_pattern, response, re.DOTALL)

        if matches:
            return matches[0].strip()

        # If no code blocks, try to find Python code by looking for imports
        if 'import ' in response and ('plt.' in response or 'sns.' in response or 'px.' in response):
            # Extract everything that looks like code
            return response.strip()

        logger.warning("Could not extract clean code block from response")
        return response

    def execute_visualization_code(
        self,
        code: str,
        attempt: int,
        model_name: str,
        dataset_name: str
    ) -> Dict:
        """
        Execute the generated visualization code

        Args:
            code: Python code to execute
            attempt: Attempt number (1-3)
            model_name: Name of the model
            dataset_name: Name of the dataset

        Returns:
            dict: Execution results
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{model_name}_{dataset_name}_attempt{attempt}_{timestamp}.png"
        output_path = os.path.join(
            self.config['outputs']['visualizations_dir'],
            output_filename
        )

        # Save the code
        code_filename = output_filename.replace('.png', '.py')
        code_path = os.path.join(
            self.config['outputs']['visualizations_dir'],
            code_filename
        )

        if self.config['outputs']['save_code']:
            with open(code_path, 'w') as f:
                f.write(code)
            logger.info(f"Saved code to: {code_path}")

        # Modify code to use correct output path and data path
        modified_code = code.replace('output.png', output_path)

        # Fix data path to use absolute path
        data_absolute_path = os.path.abspath(self.config['dataset']['path'])
        modified_code = modified_code.replace('data/titanic.csv', data_absolute_path)
        modified_code = modified_code.replace("'data/titanic.csv'", f"'{data_absolute_path}'")
        modified_code = modified_code.replace('"data/titanic.csv"', f'"{data_absolute_path}"')

        # Create a temporary script
        temp_script = f"temp_viz_script_{attempt}.py"

        with open(temp_script, 'w') as f:
            f.write(modified_code)

        # Execute the script
        result = {
            'attempt': attempt,
            'timestamp': timestamp,
            'code_path': code_path,
            'output_path': output_path,
            'success': False,
            'error': None,
            'stdout': '',
            'stderr': ''
        }

        try:
            logger.info(f"Executing visualization code (Attempt {attempt})...")

            process = subprocess.run(
                [sys.executable, temp_script],
                capture_output=True,
                text=True,
                timeout=60  # 60 second timeout
            )

            result['stdout'] = process.stdout
            result['stderr'] = process.stderr

            if process.returncode == 0 and os.path.exists(output_path):
                result['success'] = True
                logger.info(f"✓ Visualization generated successfully: {output_path}")
            else:
                result['error'] = f"Return code: {process.returncode}, stderr: {process.stderr}"
                logger.error(f"✗ Execution failed: {result['error']}")

        except subprocess.TimeoutExpired:
            result['error'] = "Execution timeout (>60s)"
            logger.error(f"✗ Execution timeout")

        except Exception as e:
            result['error'] = str(e)
            logger.error(f"✗ Execution error: {e}")

        finally:
            # Cleanup temporary script
            if os.path.exists(temp_script):
                os.remove(temp_script)

        return result

    def run_single_iteration(
        self,
        attempt: int,
        dataset_name: str = "titanic"
    ) -> Dict:
        """
        Run a single iteration of the pipeline

        Args:
            attempt: Attempt number (1-3)
            dataset_name: Dataset to use

        Returns:
            dict: Results from this iteration
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Starting Attempt {attempt}/{self.config['model']['max_retries']}")
        logger.info(f"{'='*60}\n")

        iteration_result = {
            'attempt': attempt,
            'dataset': dataset_name,
            'model': self.config['model']['name'],
            'timestamp': datetime.now().isoformat()
        }

        try:
            # Get the prompt
            if dataset_name == "titanic":
                prompt = get_titanic_prompt()
            else:
                prompt = get_dataset_prompt(dataset_name)

            # Call API
            api_type = self.config['model']['api_type']

            if api_type == 'ollama':
                raw_response = self.call_ollama_api(prompt)
            elif api_type == 'openai':
                raw_response = self.call_openai_compatible_api(prompt)
            else:
                raise ValueError(f"Unsupported API type: {api_type}")

            iteration_result['raw_response'] = raw_response

            # Extract code
            code = self.extract_code_from_response(raw_response)
            iteration_result['extracted_code'] = code

            # Execute code
            execution_result = self.execute_visualization_code(
                code,
                attempt,
                self.config['model']['name'],
                dataset_name
            )
            iteration_result['execution'] = execution_result

            # Calculate metrics if visualization was successful
            if execution_result['success']:
                logger.info("Calculating metrics...")

                data_path = self.config['dataset']['path']
                metrics = calculate_metrics_for_visualization(
                    execution_result['output_path'],
                    code,
                    data_path
                )
                iteration_result['metrics'] = metrics

                # Save metrics
                metrics_filename = f"{self.config['model']['name']}_{dataset_name}_attempt{attempt}_metrics.json"
                metrics_path = os.path.join(
                    self.config['outputs']['metrics_dir'],
                    metrics_filename
                )

                with open(metrics_path, 'w') as f:
                    json.dump(metrics, f, indent=2, default=str)

                logger.info(f"Saved metrics to: {metrics_path}")

        except Exception as e:
            logger.error(f"Error in iteration {attempt}: {e}")
            iteration_result['error'] = str(e)

        return iteration_result

    def run_full_pipeline(self, dataset_name: str = "titanic") -> List[Dict]:
        """
        Run the full pipeline with all attempts

        Args:
            dataset_name: Dataset to use

        Returns:
            list: Results from all attempts
        """
        logger.info(f"\n{'#'*60}")
        logger.info(f"# AI Visualization Evaluation Pipeline")
        logger.info(f"# Model: {self.config['model']['name']}")
        logger.info(f"# Dataset: {dataset_name}")
        logger.info(f"# Attempts: {self.config['model']['max_retries']}")
        logger.info(f"{'#'*60}\n")

        all_results = []

        for attempt in range(1, self.config['model']['max_retries'] + 1):
            result = self.run_single_iteration(attempt, dataset_name)
            all_results.append(result)

            # Save intermediate results
            self.save_results(all_results)

        # Generate summary report
        self.generate_summary_report(all_results)

        logger.info(f"\n{'='*60}")
        logger.info(f"Pipeline completed! Results saved to outputs/")
        logger.info(f"{'='*60}\n")

        return all_results

    def save_results(self, results: List[Dict]):
        """Save all results to JSON file"""
        results_path = os.path.join(
            self.config['outputs']['logs_dir'],
            f"pipeline_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        logger.info(f"Saved results to: {results_path}")

    def generate_summary_report(self, results: List[Dict]):
        """Generate a summary report of all attempts"""
        report_path = os.path.join(
            self.config['outputs']['logs_dir'],
            f"summary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        with open(report_path, 'w') as f:
            f.write("="*60 + "\n")
            f.write("AI Visualization Evaluation - Summary Report\n")
            f.write("="*60 + "\n\n")

            f.write(f"Model: {self.config['model']['name']}\n")
            f.write(f"Dataset: {self.config['dataset']['name']}\n")
            f.write(f"Total Attempts: {len(results)}\n\n")

            successful_attempts = sum(1 for r in results if r.get('execution', {}).get('success', False))
            f.write(f"Successful Attempts: {successful_attempts}/{len(results)}\n\n")

            f.write("-"*60 + "\n")
            f.write("Attempt Details:\n")
            f.write("-"*60 + "\n\n")

            for result in results:
                attempt = result['attempt']
                success = result.get('execution', {}).get('success', False)
                f.write(f"Attempt {attempt}:\n")
                f.write(f"  Success: {'✓' if success else '✗'}\n")

                if success:
                    metrics = result.get('metrics', {})
                    if metrics:
                        f.write(f"  Visual Entropy: {metrics.get('visual_entropy', 'N/A')}\n")

                        color_de = metrics.get('color_delta_e', {})
                        if color_de:
                            f.write(f"  Mean Color ΔE: {color_de.get('mean_delta_e', 'N/A')}\n")
                            f.write(f"  Distinguishability: {color_de.get('distinguishability_ratio', 0)*100:.1f}%\n")

                        code_acc = metrics.get('code_accuracy', {})
                        if code_acc:
                            f.write(f"  Code Accuracy: {code_acc.get('accuracy_score', 'N/A')}%\n")
                else:
                    error = result.get('execution', {}).get('error', 'Unknown error')
                    f.write(f"  Error: {error}\n")

                f.write("\n")

        logger.info(f"Generated summary report: {report_path}")


def main():
    """Main entry point"""
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Initialize pipeline
    pipeline = VisualizationPipeline("../config/config.yaml")

    # Run the pipeline
    results = pipeline.run_full_pipeline(dataset_name="titanic")

    return results


if __name__ == "__main__":
    main()
