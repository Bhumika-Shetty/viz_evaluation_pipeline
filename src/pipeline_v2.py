"""
Enhanced Pipeline - Runs all 12 prompts, 3 times each

This version:
- Runs all 12 test prompts
- 3 attempts per prompt
- Better file organization
- Clearer naming with prompt IDs
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
import time

# Import local modules
from .prompts import get_prompt, get_all_prompt_ids, get_prompt_info, get_expected_insights
from .metrics import calculate_metrics_for_visualization

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EnhancedVisualizationPipeline:
    """Enhanced pipeline that runs all prompts"""

    def __init__(self, config_path: str = "../config/config.yaml"):
        """Initialize the pipeline"""
        self.config = self.load_config(config_path)

        # Use absolute paths from project root
        self.project_root = Path(__file__).parent.parent.absolute()
        self.setup_directories()

    def load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            raise

    def setup_directories(self):
        """Create output directories in project root"""
        # Create base outputs directory
        base_dir = self.project_root / 'outputs'
        base_dir.mkdir(parents=True, exist_ok=True)

        # Create logs directory
        logs_dir = base_dir / 'logs'
        logs_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created: {logs_dir}")

    def setup_prompt_directory(self, prompt_id: str):
        """Create directories for a specific prompt"""
        prompt_dir = self.project_root / 'outputs' / f"prompt_{prompt_id}"

        subdirs = ['visualizations', 'code', 'metrics']
        for subdir in subdirs:
            full_path = prompt_dir / subdir
            full_path.mkdir(parents=True, exist_ok=True)

        return prompt_dir

    def call_api(self, prompt: str) -> str:
        """Call AI model API (OpenAI-compatible)"""
        try:
            import openai

            client = openai.OpenAI(
                base_url=self.config['model']['api_base'],
                api_key=os.getenv('OPENAI_API_KEY')
            )

            response = client.chat.completions.create(
                model=self.config['model']['name'],
                messages=[
                    {"role": "system", "content": "You are an expert data visualization specialist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config['model']['temperature']
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"API call failed: {e}")
            raise

    def extract_code(self, response: str) -> str:
        """Extract Python code from API response"""
        # Look for code blocks
        patterns = [
            r'```python\n(.*?)```',
            r'```\n(.*?)```'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, response, re.DOTALL)
            if matches:
                return matches[0].strip()

        # Fallback: if contains Python imports
        if 'import ' in response:
            return response.strip()

        logger.warning("Could not extract code block")
        return response

    def execute_code(
        self,
        code: str,
        prompt_id: str,
        attempt: int
    ) -> Dict:
        """Execute visualization code and save result"""

        # Setup prompt-specific directories
        prompt_dir = self.setup_prompt_directory(prompt_id)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_name = self.config['model']['name'].replace('/', '_')

        # File naming: model_attemptN_timestamp
        base_name = f"{model_name}_attempt{attempt}_{timestamp}"

        output_png = prompt_dir / f"visualizations/{base_name}.png"
        output_py = prompt_dir / f"code/{base_name}.py"

        # Save original code
        with open(output_py, 'w') as f:
            f.write(code)

        # Modify code to use absolute paths
        data_path = str(self.project_root / self.config['dataset']['path'])
        modified_code = code
        modified_code = modified_code.replace('data/titanic.csv', data_path)
        modified_code = modified_code.replace("'data/titanic.csv'", f"'{data_path}'")
        modified_code = modified_code.replace('"data/titanic.csv"', f'"{data_path}"')
        modified_code = modified_code.replace('output.png', str(output_png))

        # Execute
        temp_script = f"temp_{prompt_id}_{attempt}.py"

        try:
            with open(temp_script, 'w') as f:
                f.write(modified_code)

            result = subprocess.run(
                [sys.executable, temp_script],
                capture_output=True,
                text=True,
                timeout=60
            )

            success = result.returncode == 0 and output_png.exists()

            return {
                'success': success,
                'output_png': str(output_png),
                'output_py': str(output_py),
                'stdout': result.stdout,
                'stderr': result.stderr,
                'error': None if success else result.stderr
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            if os.path.exists(temp_script):
                os.remove(temp_script)

    def run_single_visualization(
        self,
        prompt_id: str,
        attempt: int
    ) -> Dict:
        """Run one visualization (one prompt, one attempt)"""

        prompt_info = get_prompt_info(prompt_id)
        logger.info(f"\n{'='*70}")
        logger.info(f"Prompt: {prompt_id} - {prompt_info['name']}")
        logger.info(f"Attempt: {attempt}/3")
        logger.info(f"{'='*70}")

        result = {
            'prompt_id': prompt_id,
            'prompt_name': prompt_info['name'],
            'attempt': attempt,
            'timestamp': datetime.now().isoformat()
        }

        try:
            # Get prompt
            prompt = get_prompt(prompt_id)

            # Call API
            start_time = time.time()
            raw_response = self.call_api(prompt)
            end_time = time.time()

            # Extract code
            code = self.extract_code(raw_response)

            # Execute
            exec_result = self.execute_code(code, prompt_id, attempt)
            result['execution'] = exec_result
            result['api_time_seconds'] = end_time - start_time

            if exec_result['success']:
                logger.info(f"✓ Visualization created: {exec_result['output_png']}")

                # Calculate metrics
                try:
                    metrics = calculate_metrics_for_visualization(
                        exec_result['output_png'],
                        code,
                        str(self.project_root / self.config['dataset']['path'])
                    )
                    result['metrics'] = metrics

                    # Save metrics in prompt-specific directory
                    model_name = self.config['model']['name'].replace('/', '_')
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    prompt_dir = self.project_root / 'outputs' / f"prompt_{prompt_id}"
                    metrics_file = prompt_dir / f"metrics/{model_name}_attempt{attempt}_{timestamp}.json"

                    with open(metrics_file, 'w') as f:
                        json.dump(metrics, f, indent=2, default=str)

                    logger.info(f"✓ Metrics saved: {metrics_file}")

                except Exception as e:
                    logger.error(f"Metrics calculation failed: {e}")
                    result['metrics_error'] = str(e)
            else:
                logger.error(f"✗ Execution failed: {exec_result.get('error', 'Unknown error')}")

        except Exception as e:
            logger.error(f"Error in visualization: {e}")
            result['error'] = str(e)

        return result

    def run_all_prompts(self) -> List[Dict]:
        """Run all 12 prompts, 3 times each"""

        prompt_ids = get_all_prompt_ids()
        max_retries = self.config['model']['max_retries']

        logger.info(f"\n{'#'*70}")
        logger.info(f"# ENHANCED AI VISUALIZATION EVALUATION PIPELINE")
        logger.info(f"# Model: {self.config['model']['name']}")
        logger.info(f"# Total Prompts: {len(prompt_ids)}")
        logger.info(f"# Attempts per Prompt: {max_retries}")
        logger.info(f"# Total Visualizations: {len(prompt_ids) * max_retries}")
        logger.info(f"{'#'*70}\n")

        all_results = []

        for i, prompt_id in enumerate(prompt_ids, 1):
            logger.info(f"\n{'*'*70}")
            logger.info(f"* PROMPT {i}/{len(prompt_ids)}: {prompt_id}")
            logger.info(f"{'*'*70}")

            for attempt in range(1, max_retries + 1):
                result = self.run_single_visualization(prompt_id, attempt)
                all_results.append(result)

                # Save intermediate results
                self.save_results(all_results)

        # Generate final report
        self.generate_report(all_results)

        return all_results

    def save_results(self, results: List[Dict]):
        """Save results to JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = self.project_root / f"outputs/logs/pipeline_results_{timestamp}.json"

        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

    def generate_report(self, results: List[Dict]):
        """Generate summary report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.project_root / f"outputs/logs/summary_report_{timestamp}.txt"

        with open(report_file, 'w') as f:
            f.write("="*70 + "\n")
            f.write("AI VISUALIZATION EVALUATION - COMPLETE REPORT\n")
            f.write("="*70 + "\n\n")

            f.write(f"Model: {self.config['model']['name']}\n")
            f.write(f"Dataset: {self.config['dataset']['name']}\n")
            f.write(f"Total Prompts: {len(get_all_prompt_ids())}\n")
            f.write(f"Attempts per Prompt: {self.config['model']['max_retries']}\n")
            f.write(f"Total Runs: {len(results)}\n\n")

            # Success statistics
            successful = sum(1 for r in results if r.get('execution', {}).get('success', False))
            f.write(f"Successful Visualizations: {successful}/{len(results)} ({successful/len(results)*100:.1f}%)\n\n")

            # Group by prompt
            f.write("-"*70 + "\n")
            f.write("RESULTS BY PROMPT\n")
            f.write("-"*70 + "\n\n")

            by_prompt = {}
            for r in results:
                pid = r['prompt_id']
                if pid not in by_prompt:
                    by_prompt[pid] = []
                by_prompt[pid].append(r)

            for prompt_id, prompt_results in by_prompt.items():
                prompt_info = get_prompt_info(prompt_id)
                f.write(f"\n{prompt_id}: {prompt_info['name']}\n")

                prompt_success = sum(1 for r in prompt_results if r.get('execution', {}).get('success', False))
                f.write(f"  Success Rate: {prompt_success}/{len(prompt_results)}\n")

                for r in prompt_results:
                    success = r.get('execution', {}).get('success', False)
                    f.write(f"    Attempt {r['attempt']}: {'✓' if success else '✗'}\n")

                    if success and 'metrics' in r:
                        m = r['metrics']
                        if 'visual_entropy' in m:
                            f.write(f"      Visual Entropy: {m['visual_entropy']:.3f}\n")
                        if 'color_delta_e' in m and m['color_delta_e']:
                            f.write(f"      Mean Color ΔE: {m['color_delta_e'].get('mean_delta_e', 'N/A')}\n")

        logger.info(f"\n{'='*70}")
        logger.info(f"✓ PIPELINE COMPLETE!")
        logger.info(f"✓ Report saved: {report_file}")
        logger.info(f"✓ Results: {successful}/{len(results)} visualizations created")
        logger.info(f"{'='*70}\n")


def main():
    """Main entry point"""
    pipeline = EnhancedVisualizationPipeline()
    results = pipeline.run_all_prompts()
    return results


if __name__ == "__main__":
    main()
