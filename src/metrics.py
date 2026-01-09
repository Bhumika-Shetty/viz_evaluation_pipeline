"""
Metrics for evaluating AI-generated visualizations

Based on the research paper:
"Evaluating the Performance of AI Models in Data Visualization"

Metrics implemented:
1. Fidelity Score - Data integrity measurement
2. Color ΔE (Delta E) - Color distinguishability
3. Visual Entropy - Visual complexity measurement
4. Code Generation Accuracy - Technical correctness
5. Task Completion Time - Efficiency measure
6. Accuracy/Error Rate - Insight extraction correctness
7. Expert Quality Rating - Professional assessment (1-5 scale)
8. User Satisfaction Score - Overall satisfaction (1-5 scale)
"""

import numpy as np
import pandas as pd
from PIL import Image
from typing import Dict, List, Tuple, Optional
from collections import Counter
import matplotlib.colors as mcolors
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import logging

# Fix for NumPy 2.0+ compatibility (asscalar was removed)
if not hasattr(np, 'asscalar'):
    def _asscalar(a):
        """Replacement for deprecated numpy.asscalar"""
        return a.item() if hasattr(a, 'item') else float(a)
    np.asscalar = _asscalar

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VisualizationMetrics:
    """Class to calculate various metrics for visualization evaluation"""

    def __init__(self, image_path: str, original_data_path: str = None):
        """
        Initialize metrics calculator

        Args:
            image_path: Path to the generated visualization image
            original_data_path: Path to the original dataset (for fidelity check)
        """
        self.image_path = image_path
        self.original_data_path = original_data_path
        self.image = None
        self.original_data = None

        try:
            self.image = Image.open(image_path)
            logger.info(f"Loaded image: {image_path}")
        except Exception as e:
            logger.error(f"Error loading image: {e}")

        if original_data_path:
            try:
                self.original_data = pd.read_csv(original_data_path)
                logger.info(f"Loaded original data: {original_data_path}")
            except Exception as e:
                logger.error(f"Error loading data: {e}")

    def calculate_fidelity_score(self, generated_data: pd.DataFrame = None) -> float:
        """
        Calculate Fidelity Score - measures how truthfully data is represented

        Fidelity = (Accurate Data Points / Total Points) × 100

        Args:
            generated_data: DataFrame extracted from visualization (if available)

        Returns:
            float: Fidelity score (0-100, higher is better)
        """
        if self.original_data is None or generated_data is None:
            logger.warning("Cannot calculate fidelity without original and generated data")
            return None

        try:
            # Compare summary statistics
            orig_stats = self.original_data.describe()
            gen_stats = generated_data.describe()

            # Calculate percentage of matching statistical properties
            matches = 0
            total_checks = 0

            for col in orig_stats.columns:
                if col in gen_stats.columns:
                    for stat in ['mean', 'std', 'min', 'max']:
                        total_checks += 1
                        orig_val = orig_stats.loc[stat, col]
                        gen_val = gen_stats.loc[stat, col]

                        # Allow 5% tolerance
                        if abs(orig_val - gen_val) / (abs(orig_val) + 1e-10) < 0.05:
                            matches += 1

            fidelity_score = (matches / total_checks * 100) if total_checks > 0 else 0
            logger.info(f"Fidelity Score: {fidelity_score:.2f}%")
            return fidelity_score

        except Exception as e:
            logger.error(f"Error calculating fidelity score: {e}")
            return None

    def extract_dominant_colors(self, n_colors: int = 10) -> List[Tuple[int, int, int]]:
        """
        Extract dominant colors from the visualization image

        Args:
            n_colors: Number of dominant colors to extract

        Returns:
            List of RGB tuples
        """
        if self.image is None:
            return []

        # Convert image to RGB if needed
        img_rgb = self.image.convert('RGB')

        # Resize for faster processing
        img_small = img_rgb.resize((150, 150))

        # Get all pixels
        pixels = list(img_small.getdata())

        # Count color frequencies
        color_counts = Counter(pixels)

        # Get most common colors (excluding white and near-white backgrounds)
        dominant_colors = []
        for color, count in color_counts.most_common(n_colors * 3):
            # Skip very light colors (likely background)
            if sum(color) < 700:  # Not too close to white (255, 255, 255)
                dominant_colors.append(color)
                if len(dominant_colors) >= n_colors:
                    break

        return dominant_colors

    def calculate_color_delta_e(self, colors: List[Tuple[int, int, int]] = None) -> Dict:
        """
        Calculate Color ΔE (Delta E) - color distinguishability metric

        ΔE = √((L₁-L₂)² + (a₁-a₂)² + (b₁-b₂)²)
        Using CIE2000 formula for better perceptual accuracy

        ΔE > 3 = distinguishable colors (research threshold)

        Args:
            colors: List of RGB color tuples. If None, extracts from image

        Returns:
            dict: Statistics about color distinguishability
        """
        if colors is None:
            colors = self.extract_dominant_colors()

        if len(colors) < 2:
            logger.warning("Need at least 2 colors to calculate Delta E")
            return {
                'min_delta_e': None,
                'max_delta_e': None,
                'mean_delta_e': None,
                'distinguishable_pairs': 0,
                'total_pairs': 0,
                'distinguishability_ratio': 0
            }

        delta_e_values = []

        # Convert RGB to Lab color space and calculate pairwise Delta E
        for i in range(len(colors)):
            for j in range(i + 1, len(colors)):
                rgb1 = sRGBColor(colors[i][0] / 255, colors[i][1] / 255, colors[i][2] / 255)
                rgb2 = sRGBColor(colors[j][0] / 255, colors[j][1] / 255, colors[j][2] / 255)

                lab1 = convert_color(rgb1, LabColor)
                lab2 = convert_color(rgb2, LabColor)

                delta_e = delta_e_cie2000(lab1, lab2)
                delta_e_values.append(delta_e)

        # Calculate statistics
        distinguishable_pairs = sum(1 for de in delta_e_values if de > 3)
        total_pairs = len(delta_e_values)

        result = {
            'min_delta_e': min(delta_e_values) if delta_e_values else None,
            'max_delta_e': max(delta_e_values) if delta_e_values else None,
            'mean_delta_e': np.mean(delta_e_values) if delta_e_values else None,
            'median_delta_e': np.median(delta_e_values) if delta_e_values else None,
            'distinguishable_pairs': distinguishable_pairs,
            'total_pairs': total_pairs,
            'distinguishability_ratio': distinguishable_pairs / total_pairs if total_pairs > 0 else 0,
            'all_delta_e_values': delta_e_values
        }

        logger.info(f"Color ΔE Analysis:")
        logger.info(f"  Mean ΔE: {result['mean_delta_e']:.2f}")
        logger.info(f"  Distinguishable pairs: {distinguishable_pairs}/{total_pairs} ({result['distinguishability_ratio']*100:.1f}%)")

        return result

    def calculate_visual_entropy(self) -> float:
        """
        Calculate Visual Entropy - measures complexity/randomness of visual elements

        H(X) = -Σ pᵢ × log₂(pᵢ)
        where pᵢ = (Number of elements of type i) / (Total number of visual elements)

        Measures how many different colors, shapes, patterns, and densities are used

        Returns:
            float: Visual entropy value (higher = more complex/varied)
        """
        if self.image is None:
            logger.warning("No image available for entropy calculation")
            return None

        try:
            # Convert to RGB
            img_rgb = self.image.convert('RGB')
            img_array = np.array(img_rgb)

            # Calculate color entropy (primary component)
            # Quantize colors to reduce noise
            img_quantized = img_array // 32  # Reduce to 8 levels per channel

            # Flatten and count unique colors
            pixels = img_quantized.reshape(-1, 3)
            unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)

            # Calculate probabilities
            total_pixels = len(pixels)
            probabilities = counts / total_pixels

            # Calculate Shannon entropy
            entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))

            # Additional complexity measures

            # Edge density (measure of visual complexity)
            gray = np.array(self.image.convert('L'))
            edges_h = np.abs(np.diff(gray, axis=0))
            edges_v = np.abs(np.diff(gray, axis=1))
            edge_density = (edges_h.mean() + edges_v.mean()) / 2

            # Normalize edge density to 0-1 range
            edge_density_norm = min(edge_density / 50, 1.0)

            # Combined visual entropy (weighted)
            visual_entropy = 0.7 * entropy + 0.3 * edge_density_norm * 10

            logger.info(f"Visual Entropy: {visual_entropy:.3f}")
            logger.info(f"  Color entropy: {entropy:.3f}")
            logger.info(f"  Edge density: {edge_density:.3f}")

            return visual_entropy

        except Exception as e:
            logger.error(f"Error calculating visual entropy: {e}")
            return None

    def calculate_code_accuracy(self, code: str) -> Dict:
        """
        Calculate Code Generation Accuracy

        Checks:
        - Syntax validity
        - Imports completeness
        - Execution success

        Args:
            code: Generated Python code

        Returns:
            dict: Code quality metrics
        """
        import ast
        import sys
        from io import StringIO

        result = {
            'syntax_valid': False,
            'has_imports': False,
            'has_visualization': False,
            'has_save': False,
            'execution_success': False,
            'error_message': None
        }

        # Check syntax
        try:
            ast.parse(code)
            result['syntax_valid'] = True
        except SyntaxError as e:
            result['error_message'] = f"Syntax error: {str(e)}"
            return result

        # Check for imports
        if any(imp in code for imp in ['import matplotlib', 'import seaborn', 'import plotly', 'import pandas']):
            result['has_imports'] = True

        # Check for visualization creation
        if any(viz in code for viz in ['plt.', 'sns.', 'px.', 'go.', 'Figure']):
            result['has_visualization'] = True

        # Check for save operation
        if any(save in code for save in ['savefig', 'write_image', 'to_file']):
            result['has_save'] = True

        # Calculate overall accuracy score
        checks_passed = sum([
            result['syntax_valid'],
            result['has_imports'],
            result['has_visualization'],
            result['has_save']
        ])

        result['accuracy_score'] = (checks_passed / 4) * 100

        logger.info(f"Code Accuracy: {result['accuracy_score']:.1f}%")

                # --- Runtime execution evidence (manual workflow friendly) ---
        # In UI/manual evaluation, we cannot safely execute arbitrary code here.
        # Instead, treat "execution_success" as: the expected output image exists and is non-empty.
        # Because models were queried via UI and code execution occurred locally, runtime success was verified by the existence of a non-empty output image file rather than sandbox execution within the evaluator.
        try:
            import os
            if self.image_path and os.path.isfile(self.image_path) and os.path.getsize(self.image_path) > 0:
                result['execution_success'] = True
            else:
                result['execution_success'] = False
                # Only add a message if nothing else already explains failure
                if result['error_message'] is None:
                    result['error_message'] = "Output image missing/empty; cannot confirm runtime execution."
        except Exception as e:
            result['execution_success'] = False
            if result['error_message'] is None:
                result['error_message'] = f"Execution verification failed: {e}"

        return result

    def calculate_task_completion_time(self, start_time: float, end_time: float) -> Dict:
        """
        Calculate Task Completion Time

        Args:
            start_time: Start timestamp
            end_time: End timestamp

        Returns:
            dict: Time metrics
        """
        completion_time = end_time - start_time

        result = {
            'completion_time_seconds': completion_time,
            'completion_time_minutes': completion_time / 60,
            'start_time': start_time,
            'end_time': end_time
        }

        logger.info(f"Task Completion Time: {completion_time:.2f} seconds ({completion_time/60:.2f} minutes)")

        return result

    def calculate_accuracy_error_rate(
        self,
        expected_insights: List[str],
        extracted_insights: List[str]
    ) -> Dict:
        """
        Calculate Accuracy/Error Rate - Percentage of correct insights extracted

        Args:
            expected_insights: List of expected insights from the data
            extracted_insights: List of insights extracted from visualization

        Returns:
            dict: Accuracy metrics
        """
        if not expected_insights:
            return {'accuracy': None, 'error_rate': None, 'correct_insights': 0}

        # Calculate how many expected insights were found
        correct_insights = sum(
            1 for insight in expected_insights
            if any(insight.lower() in extracted.lower() for extracted in extracted_insights)
        )

        accuracy = (correct_insights / len(expected_insights)) * 100
        error_rate = 100 - accuracy

        result = {
            'accuracy_percentage': accuracy,
            'error_rate_percentage': error_rate,
            'correct_insights': correct_insights,
            'total_expected_insights': len(expected_insights),
            'total_extracted_insights': len(extracted_insights)
        }

        logger.info(f"Accuracy: {accuracy:.1f}%, Error Rate: {error_rate:.1f}%")

        return result

    def get_expert_quality_rating_template(self) -> Dict:
        """
        Get template for Expert Quality Rating

        This is a manual assessment that requires human expert input.
        Returns a template that can be filled out.

        Returns:
            dict: Rating template (1-5 scale)
        """
        template = {
            'rating_instructions': 'Rate on a scale of 1-5 (1=Very Poor, 5=Excellent)',
            'clarity': None,  # How clearly does it communicate insights?
            'appropriateness': None,  # Is the chart type appropriate for the data?
            'completeness': None,  # Does it show all relevant patterns?
            'aesthetics': None,  # Is it visually appealing and professional?
            'accuracy': None,  # Is the data represented accurately?
            'overall_quality': None,  # Overall assessment
            'comments': ''
        }

        return template

    def get_user_satisfaction_template(self) -> Dict:
        """
        Get template for User Satisfaction Score

        This requires human user feedback.
        Returns a template that can be filled out.

        Returns:
            dict: Satisfaction template (1-5 scale)
        """
        template = {
            'rating_instructions': 'Rate on a scale of 1-5 (1=Very Dissatisfied, 5=Very Satisfied)',
            'ease_of_understanding': None,  # How easy was it to understand?
            'usefulness': None,  # How useful is this visualization?
            'trustworthiness': None,  # How much do you trust this visualization?
            'likelihood_to_use': None,  # Would you use this in your work?
            'overall_satisfaction': None,  # Overall satisfaction
            'comments': ''
        }

        return template

    def calculate_all_metrics(
        self,
        generated_code: str = None,
        start_time: float = None,
        end_time: float = None,
        expected_insights: List[str] = None,
        extracted_insights: List[str] = None
    ) -> Dict:
        """
        Calculate all available metrics

        Args:
            generated_code: The Python code that generated the visualization
            start_time: Start timestamp for task completion time
            end_time: End timestamp for task completion time
            expected_insights: List of expected insights for accuracy calculation
            extracted_insights: List of extracted insights for accuracy calculation

        Returns:
            dict: All metrics combined
        """
        metrics = {
            'image_path': self.image_path,
            'timestamp': pd.Timestamp.now().isoformat()
        }

        # Calculate Color Delta E
        color_metrics = self.calculate_color_delta_e()
        metrics['color_delta_e'] = color_metrics

        # Calculate Visual Entropy
        visual_entropy = self.calculate_visual_entropy()
        metrics['visual_entropy'] = visual_entropy

        # Calculate Code Accuracy if code is provided
        if generated_code:
            code_metrics = self.calculate_code_accuracy(generated_code)
            metrics['code_accuracy'] = code_metrics

        # Calculate Task Completion Time if provided
        if start_time and end_time:
            time_metrics = self.calculate_task_completion_time(start_time, end_time)
            metrics['task_completion_time'] = time_metrics

        # Calculate Accuracy/Error Rate if insights provided
        if expected_insights and extracted_insights:
            accuracy_metrics = self.calculate_accuracy_error_rate(
                expected_insights,
                extracted_insights
            )
            metrics['accuracy_error_rate'] = accuracy_metrics

        # Add templates for human feedback metrics
        metrics['expert_quality_rating_template'] = self.get_expert_quality_rating_template()
        metrics['user_satisfaction_template'] = self.get_user_satisfaction_template()

        # Calculate Fidelity Score (placeholder - requires extracted data)
        metrics['fidelity_score'] = None  # Will be calculated if data is available

        return metrics


def calculate_metrics_for_visualization(
    image_path: str,
    code: str = None,
    original_data_path: str = None
) -> Dict:
    """
    Convenience function to calculate all metrics for a visualization

    Args:
        image_path: Path to the generated visualization
        code: The generated code
        original_data_path: Path to original dataset

    Returns:
        dict: All calculated metrics
    """
    calculator = VisualizationMetrics(image_path, original_data_path)
    return calculator.calculate_all_metrics(code)
