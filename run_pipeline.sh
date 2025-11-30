#!/bin/bash

# AI Visualization Evaluation Pipeline - Quick Start Script

echo "======================================================================"
echo "AI Visualization Evaluation Pipeline"
echo "======================================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if Ollama is running
echo "Checking if Ollama is running..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✓ Ollama is running"
else
    echo "✗ Ollama is not running"
    echo "Please start Ollama with: ollama serve"
    exit 1
fi

# Check if dataset exists
if [ ! -f "data/titanic.csv" ]; then
    echo ""
    echo "Dataset not found. Downloading..."
    python3 download_data.py
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Run the pipeline
echo ""
echo "======================================================================"
echo "Starting Pipeline..."
echo "======================================================================"
echo ""

cd src
python3 pipeline.py

echo ""
echo "======================================================================"
echo "Pipeline Complete!"
echo "======================================================================"
echo ""
echo "Results saved in outputs/ directory:"
echo "  - Visualizations: outputs/visualizations/"
echo "  - Metrics: outputs/metrics/"
echo "  - Reports: outputs/logs/"
echo ""
