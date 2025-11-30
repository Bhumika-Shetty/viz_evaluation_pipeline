# Manual Setup Guide - Step by Step

The automatic installer has an issue with Ollama download. Follow these manual steps instead.

---

## Step 1: Create Python Virtual Environment ✅

```bash
cd /scratch/bds9746/viz_evaluation_pipeline

# Create venv
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install packages
pip install --upgrade pip
pip install -r requirements.txt
```

**Verify:**
```bash
which python  # Should show: .../viz_evaluation_pipeline/venv/bin/python
```

---

## Step 2: Install Ollama (Manual Method)

### Method A: Use Ollama's Official Install Script (Recommended)

```bash
# Create directory
mkdir -p /scratch/bds9746/ollama

# Set models directory BEFORE installing
export OLLAMA_MODELS=/scratch/bds9746/ollama/models

# Download and run official installer
curl -fsSL https://ollama.com/install.sh | OLLAMA_HOME=/scratch/bds9746/ollama sh

# The installer will put the binary in /usr/local/bin/ollama (system-wide)
# But models will go to /scratch/bds9746/ollama/models
```

### Method B: Docker (If available)

```bash
# Pull Ollama Docker image
docker pull ollama/ollama

# Run with volume mounted to scratch
docker run -d \
  --name ollama \
  -v /scratch/bds9746/ollama/models:/root/.ollama/models \
  -p 11434:11434 \
  ollama/ollama
```

### Method C: Manual Binary Download (Alternative)

If the above methods don't work, try this:

```bash
# Create directory
mkdir -p /scratch/bds9746/ollama
cd /scratch/bds9746/ollama

# Try the new download location
curl -L https://github.com/ollama/ollama/releases/latest/download/ollama-linux-amd64 -o ollama

# Make executable
chmod +x ollama

# Test it
./ollama --version
```

---

## Step 3: Start Ollama Server

### If using system installation (Method A):

```bash
# Set models directory
export OLLAMA_MODELS=/scratch/bds9746/ollama/models
mkdir -p $OLLAMA_MODELS

# Start server
OLLAMA_MODELS=/scratch/bds9746/ollama/models ollama serve &

# Or run in background with logs
nohup env OLLAMA_MODELS=/scratch/bds9746/ollama/models ollama serve > /scratch/bds9746/ollama/server.log 2>&1 &
echo $! > /scratch/bds9746/ollama/ollama.pid
```

### If using local binary (Method C):

```bash
# Set models directory
export OLLAMA_MODELS=/scratch/bds9746/ollama/models
mkdir -p $OLLAMA_MODELS

# Start server
nohup /scratch/bds9746/ollama/ollama serve > /scratch/bds9746/ollama/server.log 2>&1 &
echo $! > /scratch/bds9746/ollama/ollama.pid
```

### If using Docker (Method B):

Already running! Skip to Step 4.

**Verify server is running:**
```bash
# Wait a few seconds, then test
sleep 5
curl http://localhost:11434/api/tags
# Should return JSON with models list (empty at first)
```

---

## Step 4: Download AI Model

### Choose a model:

**For testing (recommended):**
```bash
ollama pull llama3.2:1b     # ~1GB, fast
```

**For better quality:**
```bash
ollama pull llama3.2        # ~2GB, good balance
```

**For code generation:**
```bash
ollama pull codellama:7b    # ~4GB, optimized for code
```

**Verify download:**
```bash
ollama list
```

---

## Step 5: Download Dataset

```bash
cd /scratch/bds9746/viz_evaluation_pipeline
source venv/bin/activate
python download_data.py
```

**Verify:**
```bash
ls -lh data/titanic.csv
# Should show ~60KB file
```

---

## Step 6: Update Configuration

Edit the config to use your downloaded model:

```bash
cd /scratch/bds9746/viz_evaluation_pipeline

# If you downloaded llama3.2:1b
sed -i 's/name: "llama3.2"/name: "llama3.2:1b"/' config/config.yaml

# Or edit manually
nano config/config.yaml
# Change the model name to match what you downloaded
```

---

## Step 7: Test the Setup

```bash
cd /scratch/bds9746/viz_evaluation_pipeline

# Activate environment
source venv/bin/activate

# Set Ollama environment
export OLLAMA_MODELS=/scratch/bds9746/ollama/models

# Test Python packages
python -c "import pandas, matplotlib, seaborn; print('✓ Packages OK')"

# Test Ollama
curl http://localhost:11434/api/tags

# Test dataset
python -c "import pandas as pd; df=pd.read_csv('data/titanic.csv'); print(f'✓ Dataset: {len(df)} rows')"

# Test Ollama model
ollama list
```

---

## Step 8: Run the Pipeline

### Create a simple run script:

```bash
cat > /scratch/bds9746/viz_evaluation_pipeline/run.sh << 'EOF'
#!/bin/bash
cd /scratch/bds9746/viz_evaluation_pipeline
source venv/bin/activate
export OLLAMA_MODELS=/scratch/bds9746/ollama/models
export OLLAMA_HOST=http://localhost:11434

echo "Running pipeline..."
cd src
python pipeline.py
EOF

chmod +x run.sh
```

### Run it:

```bash
./run.sh
```

---

## Environment Variables to Set Every Time

Create a file to source in each session:

```bash
cat > /scratch/bds9746/viz_evaluation_pipeline/env.sh << 'EOF'
#!/bin/bash
# Source this file in each new terminal session

# Activate Python
source /scratch/bds9746/viz_evaluation_pipeline/venv/bin/activate

# Set Ollama directories
export OLLAMA_MODELS=/scratch/bds9746/ollama/models
export OLLAMA_HOST=http://localhost:11434

echo "✓ Environment ready"
echo "  Python: $(which python)"
echo "  Ollama models: $OLLAMA_MODELS"
EOF

chmod +x env.sh
```

**Usage in new sessions:**
```bash
source /scratch/bds9746/viz_evaluation_pipeline/env.sh
```

---

## Quick Commands Summary

```bash
# Setup (one time)
cd /scratch/bds9746/viz_evaluation_pipeline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
curl -fsSL https://ollama.com/install.sh | OLLAMA_HOME=/scratch/bds9746/ollama sh
export OLLAMA_MODELS=/scratch/bds9746/ollama/models
mkdir -p $OLLAMA_MODELS
OLLAMA_MODELS=/scratch/bds9746/ollama/models ollama serve &
ollama pull llama3.2:1b
python download_data.py

# Run pipeline (every time)
cd /scratch/bds9746/viz_evaluation_pipeline
source env.sh  # If you created it
./run.sh
```

---

## Troubleshooting

### Ollama install script fails?

Try the pre-compiled binary:
```bash
cd /scratch/bds9746/ollama
wget https://github.com/ollama/ollama/releases/download/v0.1.26/ollama-linux-amd64.tgz
tar xzf ollama-linux-amd64.tgz
chmod +x bin/ollama
ln -s bin/ollama ollama
```

### Can't download models?

Check internet connection and disk space:
```bash
df -h /scratch/bds9746
ping -c 3 ollama.com
```

### Port 11434 already in use?

Find and kill the process:
```bash
lsof -i :11434
kill <PID>
```

### Python packages won't install?

Try installing one at a time:
```bash
pip install pandas numpy matplotlib seaborn plotly Pillow
pip install colormath requests PyYAML openai
```

---

## Verification Checklist

- [ ] Python venv created and activated
- [ ] All packages installed (check with `pip list`)
- [ ] Ollama binary available (check with `which ollama` or `./ollama --version`)
- [ ] Ollama server running (check with `curl http://localhost:11434/api/tags`)
- [ ] AI model downloaded (check with `ollama list`)
- [ ] Dataset downloaded (check with `ls data/titanic.csv`)
- [ ] Environment variables set (`echo $OLLAMA_MODELS`)
- [ ] No files in home directory (check `ls ~/.ollama` - should not exist)

---

**Once everything is verified, run the pipeline with `./run.sh`**
