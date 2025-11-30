# Complete Setup Instructions

## Everything in /scratch/bds9746 - Nothing in Home Directory

This guide ensures ALL installations, environments, and data stay in `/scratch/bds9746`.

---

## Step 1: Set Up Python Virtual Environment

```bash
# Navigate to the project
cd /scratch/bds9746/viz_evaluation_pipeline

# Create virtual environment in the project directory
python3 -m venv /scratch/bds9746/viz_evaluation_pipeline/venv

# Activate the virtual environment
source /scratch/bds9746/viz_evaluation_pipeline/venv/bin/activate

# Upgrade pip (optional but recommended)
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

**Verify installation:**
```bash
which python  # Should show: /scratch/bds9746/viz_evaluation_pipeline/venv/bin/python
pip list      # Should show installed packages
```

---

## Step 2: Install Ollama (Two Options)

### Option A: Install Ollama in /scratch/bds9746 (Recommended)

If you don't have admin rights or want everything local:

```bash
# Create Ollama directory in scratch
mkdir -p /scratch/bds9746/ollama

# Download Ollama binary
cd /scratch/bds9746/ollama
curl -L https://ollama.ai/download/ollama-linux-amd64 -o ollama
chmod +x ollama

# Set Ollama data directory to scratch
export OLLAMA_MODELS=/scratch/bds9746/ollama/models
mkdir -p $OLLAMA_MODELS

# Start Ollama server in background
nohup /scratch/bds9746/ollama/ollama serve > /scratch/bds9746/ollama/server.log 2>&1 &

# Save the PID for later
echo $! > /scratch/bds9746/ollama/ollama.pid

# Wait a few seconds for server to start
sleep 5

# Verify Ollama is running
curl http://localhost:11434/api/tags
```

**Pull a model:**
```bash
# Use the local ollama binary
/scratch/bds9746/ollama/ollama pull llama3.2

# Or for a smaller/faster model:
/scratch/bds9746/ollama/ollama pull llama3.2:1b
```

**Stop Ollama when done:**
```bash
# Kill using the saved PID
kill $(cat /scratch/bds9746/ollama/ollama.pid)
```

### Option B: System-wide Ollama Installation

If you have admin/sudo access:

```bash
# Download and install
curl -fsSL https://ollama.ai/install.sh | sh

# But still set models directory to scratch
export OLLAMA_MODELS=/scratch/bds9746/ollama/models
mkdir -p $OLLAMA_MODELS

# Start server
ollama serve &

# Pull model
ollama pull llama3.2
```

---

## Step 3: Download Titanic Dataset

```bash
# Make sure virtual environment is activated
source /scratch/bds9746/viz_evaluation_pipeline/venv/bin/activate

# Navigate to project
cd /scratch/bds9746/viz_evaluation_pipeline

# Run download script
python download_data.py
```

**Expected output:**
```
Downloading Titanic dataset...
✓ Titanic dataset saved to: data/titanic.csv
  Shape: (891, 15)
  Columns: survived, pclass, sex, age, ...
```

---

## Step 4: Configure Environment Variables (Persistent)

Create a setup script that you can source:

```bash
# Create environment setup script
cat > /scratch/bds9746/viz_evaluation_pipeline/setup_env.sh << 'EOF'
#!/bin/bash

# Python virtual environment
source /scratch/bds9746/viz_evaluation_pipeline/venv/bin/activate

# Ollama settings
export OLLAMA_MODELS=/scratch/bds9746/ollama/models
export OLLAMA_HOST=http://localhost:11434

# Project directory
export VIZ_PIPELINE_ROOT=/scratch/bds9746/viz_evaluation_pipeline

echo "✓ Environment activated"
echo "  Python: $(which python)"
echo "  Ollama models: $OLLAMA_MODELS"
echo "  Project root: $VIZ_PIPELINE_ROOT"
EOF

chmod +x /scratch/bds9746/viz_evaluation_pipeline/setup_env.sh
```

**Usage:**
```bash
# In any new terminal session:
source /scratch/bds9746/viz_evaluation_pipeline/setup_env.sh
```

---

## Step 5: Verify Everything Works

```bash
# Activate environment
source /scratch/bds9746/viz_evaluation_pipeline/setup_env.sh

# Check Python packages
python -c "import pandas, matplotlib, seaborn, colormath; print('✓ All packages installed')"

# Check Ollama
curl http://localhost:11434/api/tags

# Check dataset
ls -lh /scratch/bds9746/viz_evaluation_pipeline/data/titanic.csv

# Check Ollama models
/scratch/bds9746/ollama/ollama list
```

---

## Step 6: Run the Pipeline

```bash
# Activate environment
source /scratch/bds9746/viz_evaluation_pipeline/setup_env.sh

# Navigate to project
cd /scratch/bds9746/viz_evaluation_pipeline

# Run pipeline
cd src
python pipeline.py
```

---

## Complete Startup Script (For Future Sessions)

Save this as `/scratch/bds9746/viz_evaluation_pipeline/start_pipeline.sh`:

```bash
#!/bin/bash

echo "======================================================================"
echo "Starting AI Visualization Evaluation Pipeline"
echo "======================================================================"
echo ""

# 1. Activate Python environment
echo "1. Activating Python environment..."
source /scratch/bds9746/viz_evaluation_pipeline/venv/bin/activate
echo "   ✓ Python: $(which python)"
echo ""

# 2. Set Ollama environment
echo "2. Setting Ollama environment..."
export OLLAMA_MODELS=/scratch/bds9746/ollama/models
export OLLAMA_HOST=http://localhost:11434
echo "   ✓ Ollama models: $OLLAMA_MODELS"
echo ""

# 3. Check if Ollama is running
echo "3. Checking Ollama server..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "   ✓ Ollama is running"
else
    echo "   ✗ Ollama is not running. Starting..."
    nohup /scratch/bds9746/ollama/ollama serve > /scratch/bds9746/ollama/server.log 2>&1 &
    echo $! > /scratch/bds9746/ollama/ollama.pid
    sleep 5
    echo "   ✓ Ollama started (PID: $(cat /scratch/bds9746/ollama/ollama.pid))"
fi
echo ""

# 4. Check dataset
echo "4. Checking dataset..."
if [ -f "/scratch/bds9746/viz_evaluation_pipeline/data/titanic.csv" ]; then
    echo "   ✓ Dataset found"
else
    echo "   ✗ Dataset not found. Downloading..."
    cd /scratch/bds9746/viz_evaluation_pipeline
    python download_data.py
fi
echo ""

# 5. Run pipeline
echo "5. Running pipeline..."
echo "======================================================================"
cd /scratch/bds9746/viz_evaluation_pipeline/src
python pipeline.py

echo ""
echo "======================================================================"
echo "Pipeline Complete!"
echo "======================================================================"
echo ""
echo "Results location: /scratch/bds9746/viz_evaluation_pipeline/outputs/"
echo ""
```

Make it executable:
```bash
chmod +x /scratch/bds9746/viz_evaluation_pipeline/start_pipeline.sh
```

---

## Quick Reference

### Directory Structure (Everything in /scratch/bds9746)

```
/scratch/bds9746/
├── ollama/                          # Ollama installation
│   ├── ollama                       # Binary
│   ├── models/                      # Downloaded models
│   ├── server.log                   # Server logs
│   └── ollama.pid                   # Process ID
│
└── viz_evaluation_pipeline/         # Project
    ├── venv/                        # Python virtual environment
    ├── data/                        # Datasets
    ├── outputs/                     # Results
    ├── src/                         # Source code
    ├── config/                      # Configuration
    ├── setup_env.sh                 # Environment setup
    └── start_pipeline.sh            # Complete startup script
```

### Common Commands

**Start everything:**
```bash
/scratch/bds9746/viz_evaluation_pipeline/start_pipeline.sh
```

**Just activate environment:**
```bash
source /scratch/bds9746/viz_evaluation_pipeline/setup_env.sh
```

**Check Ollama status:**
```bash
curl http://localhost:11434/api/tags
/scratch/bds9746/ollama/ollama list
```

**Stop Ollama:**
```bash
kill $(cat /scratch/bds9746/ollama/ollama.pid)
```

**View Ollama logs:**
```bash
tail -f /scratch/bds9746/ollama/server.log
```

---

## Troubleshooting

### Issue: "python3: command not found"
**Solution:** Load Python module first:
```bash
module load python/3.9  # or appropriate version
```

### Issue: "curl: command not found"
**Solution:** Use wget instead:
```bash
wget https://ollama.ai/download/ollama-linux-amd64 -O ollama
```

### Issue: "Permission denied" when running ollama
**Solution:** Make sure it's executable:
```bash
chmod +x /scratch/bds9746/ollama/ollama
```

### Issue: Ollama server won't start
**Solution:** Check if port 11434 is already in use:
```bash
lsof -i :11434
# If something is using it, kill it or use a different port
```

### Issue: Out of disk space
**Solution:** Check disk usage:
```bash
du -sh /scratch/bds9746/*
# Clean up old outputs or use smaller models
```

### Issue: Model download is slow
**Solution:** Use smaller models:
```bash
# Instead of llama3.2 (full size)
/scratch/bds9746/ollama/ollama pull llama3.2:1b  # 1 billion params, ~1GB
```

---

## Disk Space Requirements

- **Python venv**: ~500 MB
- **Python packages**: ~300 MB
- **Ollama binary**: ~50 MB
- **LLaMA 3.2 model**: ~2 GB
- **LLaMA 3.2:1b model**: ~1 GB (smaller alternative)
- **Titanic dataset**: ~60 KB
- **Output files**: ~10-50 MB per run

**Total minimum**: ~3 GB
**Recommended**: ~5 GB free space

---

## Verification Checklist

Before running the pipeline, verify:

- [ ] Python virtual environment created in `/scratch/bds9746/viz_evaluation_pipeline/venv`
- [ ] All packages installed (`pip list` shows pandas, matplotlib, etc.)
- [ ] Ollama binary in `/scratch/bds9746/ollama/ollama`
- [ ] Ollama models directory at `/scratch/bds9746/ollama/models`
- [ ] At least one model downloaded (`ollama list` shows llama3.2)
- [ ] Ollama server running (curl test passes)
- [ ] Titanic dataset at `/scratch/bds9746/viz_evaluation_pipeline/data/titanic.csv`
- [ ] No installations in home directory (`~/.ollama`, `~/.local`, etc. should not exist)

---

## Next Steps

After setup is complete:

1. Run the pipeline: `/scratch/bds9746/viz_evaluation_pipeline/start_pipeline.sh`
2. Check outputs: `ls /scratch/bds9746/viz_evaluation_pipeline/outputs/`
3. Review metrics: `cat /scratch/bds9746/viz_evaluation_pipeline/outputs/logs/summary_report_*.txt`
4. Test different prompts (see [QUICKSTART.md](QUICKSTART.md))

---

**Everything is self-contained in `/scratch/bds9746` - no home directory pollution!**
