#!/bin/bash

# One-Time Initial Setup Script
# Sets up EVERYTHING from scratch in /scratch/bds9746
# Run this once, then use start_pipeline.sh for future runs

echo "======================================================================"
echo "AI Visualization Evaluation Pipeline - Initial Setup"
echo "======================================================================"
echo ""
echo "This script will set up everything in /scratch/bds9746"
echo "No files will be created in your home directory"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Setup cancelled."
    exit 1
fi
echo ""

cd /scratch/bds9746/viz_evaluation_pipeline

# Step 1: Create Python Virtual Environment
echo "======================================================================"
echo "Step 1: Creating Python Virtual Environment"
echo "======================================================================"
echo ""

if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping..."
else
    echo "Creating virtual environment in /scratch/bds9746/viz_evaluation_pipeline/venv"
    python3 -m venv venv

    if [ $? -eq 0 ]; then
        echo "✓ Virtual environment created"
    else
        echo "✗ Failed to create virtual environment"
        echo "Make sure Python 3 is installed: python3 --version"
        exit 1
    fi
fi
echo ""

# Activate virtual environment
source venv/bin/activate
echo "✓ Virtual environment activated"
echo "  Python location: $(which python)"
echo ""

# Step 2: Install Python Dependencies
echo "======================================================================"
echo "Step 2: Installing Python Dependencies"
echo "======================================================================"
echo ""

echo "Upgrading pip..."
pip install --upgrade pip -q

echo "Installing required packages..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ All Python packages installed"
    echo ""
    echo "Installed packages:"
    pip list | grep -E "pandas|numpy|matplotlib|seaborn|plotly|Pillow|colormath|requests|PyYAML"
else
    echo "✗ Failed to install packages"
    exit 1
fi
echo ""

# Step 3: Set up Ollama
echo "======================================================================"
echo "Step 3: Setting up Ollama"
echo "======================================================================"
echo ""

# Create Ollama directory
mkdir -p /scratch/bds9746/ollama
export OLLAMA_MODELS=/scratch/bds9746/ollama/models
mkdir -p $OLLAMA_MODELS

echo "Ollama directory: /scratch/bds9746/ollama"
echo "Models directory: $OLLAMA_MODELS"
echo ""

# Check if Ollama binary exists
if [ -f "/scratch/bds9746/ollama/ollama" ]; then
    echo "✓ Ollama binary already exists"
else
    echo "Downloading Ollama binary..."

    # Try curl first
    if command -v curl &> /dev/null; then
        curl -L https://ollama.ai/download/ollama-linux-amd64 -o /scratch/bds9746/ollama/ollama
    # Fallback to wget
    elif command -v wget &> /dev/null; then
        wget https://ollama.ai/download/ollama-linux-amd64 -O /scratch/bds9746/ollama/ollama
    else
        echo "✗ Neither curl nor wget available. Please download manually:"
        echo "  URL: https://ollama.ai/download/ollama-linux-amd64"
        echo "  Save to: /scratch/bds9746/ollama/ollama"
        exit 1
    fi

    if [ $? -eq 0 ]; then
        chmod +x /scratch/bds9746/ollama/ollama
        echo "✓ Ollama binary downloaded and made executable"
    else
        echo "✗ Failed to download Ollama"
        exit 1
    fi
fi
echo ""

# Step 4: Start Ollama Server
echo "======================================================================"
echo "Step 4: Starting Ollama Server"
echo "======================================================================"
echo ""

# Check if already running
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✓ Ollama server already running"
else
    echo "Starting Ollama server..."
    nohup /scratch/bds9746/ollama/ollama serve > /scratch/bds9746/ollama/server.log 2>&1 &
    echo $! > /scratch/bds9746/ollama/ollama.pid

    sleep 5

    # Verify
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "✓ Ollama server started (PID: $(cat /scratch/bds9746/ollama/ollama.pid))"
    else
        echo "✗ Failed to start Ollama server"
        echo "Check logs: cat /scratch/bds9746/ollama/server.log"
        exit 1
    fi
fi
echo ""

# Step 5: Download AI Model
echo "======================================================================"
echo "Step 5: Downloading AI Model"
echo "======================================================================"
echo ""

echo "Available models:"
echo "  1. llama3.2 (default, ~2GB, good quality)"
echo "  2. llama3.2:1b (smaller, ~1GB, faster)"
echo "  3. codellama (optimized for code, ~4GB)"
echo ""
read -p "Which model to download? (1/2/3) [1]: " MODEL_CHOICE
MODEL_CHOICE=${MODEL_CHOICE:-1}

case $MODEL_CHOICE in
    1)
        MODEL_NAME="llama3.2"
        ;;
    2)
        MODEL_NAME="llama3.2:1b"
        ;;
    3)
        MODEL_NAME="codellama"
        ;;
    *)
        MODEL_NAME="llama3.2"
        ;;
esac

echo ""
echo "Downloading model: $MODEL_NAME"
echo "This may take several minutes depending on your connection..."
echo ""

/scratch/bds9746/ollama/ollama pull $MODEL_NAME

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Model downloaded successfully"

    # Update config to use this model
    sed -i "s/name: \"llama3.2\"/name: \"$MODEL_NAME\"/" config/config.yaml
    echo "✓ Updated config to use $MODEL_NAME"
else
    echo "✗ Failed to download model"
    exit 1
fi
echo ""

# Verify model
echo "Installed models:"
/scratch/bds9746/ollama/ollama list
echo ""

# Step 6: Download Dataset
echo "======================================================================"
echo "Step 6: Downloading Titanic Dataset"
echo "======================================================================"
echo ""

python download_data.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Dataset downloaded successfully"
else
    echo "✗ Failed to download dataset"
    exit 1
fi
echo ""

# Step 7: Create Output Directories
echo "======================================================================"
echo "Step 7: Creating Output Directories"
echo "======================================================================"
echo ""

mkdir -p outputs/visualizations
mkdir -p outputs/metrics
mkdir -p outputs/logs

echo "✓ Output directories created:"
echo "  - outputs/visualizations/"
echo "  - outputs/metrics/"
echo "  - outputs/logs/"
echo ""

# Step 8: Make Scripts Executable
echo "======================================================================"
echo "Step 8: Making Scripts Executable"
echo "======================================================================"
echo ""

chmod +x setup_env.sh
chmod +x start_pipeline.sh
chmod +x run_pipeline.sh

echo "✓ Scripts made executable"
echo ""

# Step 9: Verify Installation
echo "======================================================================"
echo "Step 9: Verification"
echo "======================================================================"
echo ""

echo "Checking installation..."
echo ""

# Check Python
echo "✓ Python: $(python --version)"

# Check packages
echo -n "✓ Pandas: "
python -c "import pandas; print(pandas.__version__)"

echo -n "✓ Matplotlib: "
python -c "import matplotlib; print(matplotlib.__version__)"

echo -n "✓ Seaborn: "
python -c "import seaborn; print(seaborn.__version__)"

# Check Ollama
echo "✓ Ollama: $(curl -s http://localhost:11434/api/tags | grep -o 'models' | head -1 || echo 'running')"

# Check dataset
if [ -f "data/titanic.csv" ]; then
    ROWS=$(wc -l < data/titanic.csv)
    echo "✓ Dataset: $ROWS rows"
fi

# Check disk space
DISK_USAGE=$(du -sh /scratch/bds9746/viz_evaluation_pipeline 2>/dev/null | cut -f1)
echo "✓ Disk usage: $DISK_USAGE"

echo ""

# Final Summary
echo "======================================================================"
echo "Setup Complete!"
echo "======================================================================"
echo ""
echo "Installation Summary:"
echo "  ✓ Virtual environment: /scratch/bds9746/viz_evaluation_pipeline/venv"
echo "  ✓ Python packages: installed"
echo "  ✓ Ollama binary: /scratch/bds9746/ollama/ollama"
echo "  ✓ Ollama models: /scratch/bds9746/ollama/models"
echo "  ✓ AI model: $MODEL_NAME"
echo "  ✓ Ollama server: running (PID: $(cat /scratch/bds9746/ollama/ollama.pid 2>/dev/null || echo 'N/A'))"
echo "  ✓ Dataset: data/titanic.csv"
echo "  ✓ Total size: $DISK_USAGE"
echo ""
echo "Everything is installed in /scratch/bds9746"
echo "Nothing was installed in your home directory"
echo ""
echo "======================================================================"
echo "Next Steps"
echo "======================================================================"
echo ""
echo "1. To run the pipeline now:"
echo "   ./start_pipeline.sh"
echo ""
echo "2. For future sessions, first activate the environment:"
echo "   source setup_env.sh"
echo "   Then run:"
echo "   ./start_pipeline.sh"
echo ""
echo "3. To test specific prompts, see QUICKSTART.md"
echo ""
echo "4. To view available prompts:"
echo "   cd src && python prompts.py"
echo ""
echo "======================================================================"
echo ""

# Ask if user wants to run pipeline now
read -p "Run the pipeline now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    ./start_pipeline.sh
fi
