#!/bin/bash

# Complete startup script for AI Visualization Evaluation Pipeline
# Handles environment activation, Ollama startup, and pipeline execution
# Everything stays in /scratch/bds9746

echo "======================================================================"
echo "AI Visualization Evaluation Pipeline - Complete Startup"
echo "======================================================================"
echo ""

# Navigate to project directory
cd /scratch/bds9746/viz_evaluation_pipeline

# 1. Activate Python environment
echo "1. Activating Python environment..."
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "   ✓ Python: $(which python)"
else
    echo "   ✗ Virtual environment not found!"
    echo ""
    echo "   Please run setup first:"
    echo "   python3 -m venv /scratch/bds9746/viz_evaluation_pipeline/venv"
    echo "   source /scratch/bds9746/viz_evaluation_pipeline/venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi
echo ""

# 2. Set Ollama environment
echo "2. Setting Ollama environment..."
export OLLAMA_MODELS=/scratch/bds9746/ollama/models
export OLLAMA_HOST=http://localhost:11434
mkdir -p $OLLAMA_MODELS
echo "   ✓ Ollama models directory: $OLLAMA_MODELS"
echo ""

# 3. Check if Ollama is running
echo "3. Checking Ollama server..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "   ✓ Ollama is running"
else
    echo "   ✗ Ollama is not running"

    # Check if Ollama binary exists
    if [ -f "/scratch/bds9746/ollama/ollama" ]; then
        echo "   Starting Ollama server..."
        nohup /scratch/bds9746/ollama/ollama serve > /scratch/bds9746/ollama/server.log 2>&1 &
        echo $! > /scratch/bds9746/ollama/ollama.pid
        sleep 5

        # Verify it started
        if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            echo "   ✓ Ollama started (PID: $(cat /scratch/bds9746/ollama/ollama.pid))"
        else
            echo "   ✗ Failed to start Ollama. Check /scratch/bds9746/ollama/server.log"
            exit 1
        fi
    else
        echo "   ✗ Ollama not installed in /scratch/bds9746/ollama/"
        echo ""
        echo "   Please install Ollama first:"
        echo "   mkdir -p /scratch/bds9746/ollama"
        echo "   cd /scratch/bds9746/ollama"
        echo "   curl -L https://ollama.ai/download/ollama-linux-amd64 -o ollama"
        echo "   chmod +x ollama"
        echo "   ./ollama pull llama3.2"
        exit 1
    fi
fi
echo ""

# 4. Check if model is downloaded
echo "4. Checking for AI model..."
if /scratch/bds9746/ollama/ollama list 2>/dev/null | grep -q "llama3.2"; then
    echo "   ✓ Model found: llama3.2"
elif /scratch/bds9746/ollama/ollama list 2>/dev/null | grep -q "llama"; then
    echo "   ✓ LLaMA model found (will use available version)"
else
    echo "   ✗ No LLaMA model found"
    echo ""
    echo "   Please download a model first:"
    echo "   /scratch/bds9746/ollama/ollama pull llama3.2"
    echo "   or for smaller version:"
    echo "   /scratch/bds9746/ollama/ollama pull llama3.2:1b"
    exit 1
fi
echo ""

# 5. Check dataset
echo "5. Checking dataset..."
if [ -f "data/titanic.csv" ]; then
    echo "   ✓ Dataset found: data/titanic.csv"
else
    echo "   ✗ Dataset not found. Downloading..."
    python download_data.py
    if [ $? -eq 0 ]; then
        echo "   ✓ Dataset downloaded successfully"
    else
        echo "   ✗ Failed to download dataset"
        exit 1
    fi
fi
echo ""

# 6. Check dependencies
echo "6. Checking Python dependencies..."
python -c "import pandas, matplotlib, seaborn, colormath, yaml, requests" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✓ All dependencies installed"
else
    echo "   ✗ Missing dependencies"
    echo ""
    echo "   Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "   ✗ Failed to install dependencies"
        exit 1
    fi
    echo "   ✓ Dependencies installed"
fi
echo ""

# 7. Run pipeline
echo "======================================================================"
echo "Starting Pipeline Execution..."
echo "======================================================================"
echo ""

cd src
python pipeline.py

EXIT_CODE=$?

echo ""
echo "======================================================================"
if [ $EXIT_CODE -eq 0 ]; then
    echo "Pipeline Completed Successfully!"
    echo "======================================================================"
    echo ""
    echo "Results location:"
    echo "  Visualizations: /scratch/bds9746/viz_evaluation_pipeline/outputs/visualizations/"
    echo "  Metrics:        /scratch/bds9746/viz_evaluation_pipeline/outputs/metrics/"
    echo "  Reports:        /scratch/bds9746/viz_evaluation_pipeline/outputs/logs/"
    echo ""

    # List generated files
    echo "Generated files:"
    ls -1 ../outputs/visualizations/*.png 2>/dev/null | tail -5
    echo ""
else
    echo "Pipeline Failed (Exit Code: $EXIT_CODE)"
    echo "======================================================================"
    echo ""
    echo "Check logs at: /scratch/bds9746/viz_evaluation_pipeline/outputs/logs/"
    echo ""
fi

# Optionally stop Ollama
read -p "Stop Ollama server? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -f "/scratch/bds9746/ollama/ollama.pid" ]; then
        kill $(cat /scratch/bds9746/ollama/ollama.pid) 2>/dev/null
        rm /scratch/bds9746/ollama/ollama.pid
        echo "✓ Ollama server stopped"
    fi
fi

exit $EXIT_CODE
