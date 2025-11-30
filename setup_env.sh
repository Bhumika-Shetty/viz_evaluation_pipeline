#!/bin/bash

# Environment Setup Script
# Sets up Python virtual environment and Ollama paths
# Everything stays in /scratch/bds9746

# Python virtual environment
if [ -d "/scratch/bds9746/viz_evaluation_pipeline/venv" ]; then
    source /scratch/bds9746/viz_evaluation_pipeline/venv/bin/activate
    echo "✓ Python environment activated"
else
    echo "✗ Virtual environment not found!"
    echo "  Run: python3 -m venv /scratch/bds9746/viz_evaluation_pipeline/venv"
    return 1
fi

# Ollama settings
export OLLAMA_MODELS=/scratch/bds9746/ollama/models
export OLLAMA_HOST=http://localhost:11434

# Project directory
export VIZ_PIPELINE_ROOT=/scratch/bds9746/viz_evaluation_pipeline

echo "  Python: $(which python)"
echo "  Ollama models: $OLLAMA_MODELS"
echo "  Project root: $VIZ_PIPELINE_ROOT"
