"""
AI Visualization Evaluation Pipeline

A comprehensive pipeline for evaluating AI models' performance
in data visualization tasks.
"""

__version__ = "1.0.0"
__author__ = "Research Team"

from .pipeline import VisualizationPipeline
from .metrics import VisualizationMetrics, calculate_metrics_for_visualization
from .prompts import get_titanic_prompt, get_dataset_prompt

__all__ = [
    'VisualizationPipeline',
    'VisualizationMetrics',
    'calculate_metrics_for_visualization',
    'get_titanic_prompt',
    'get_dataset_prompt'
]
