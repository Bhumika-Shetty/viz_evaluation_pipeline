# Quick Reference Cheat Sheet

## First Time Setup (Run Once)

```bash
cd /scratch/bds9746/viz_evaluation_pipeline
./initial_setup.sh
```

This will:
- ✅ Create Python virtual environment in `/scratch/bds9746/viz_evaluation_pipeline/venv`
- ✅ Install all Python packages
- ✅ Download Ollama to `/scratch/bds9746/ollama/`
- ✅ Download AI model (you choose: llama3.2, llama3.2:1b, or codellama)
- ✅ Download Titanic dataset
- ✅ Everything stays in `/scratch/bds9746` (nothing in home directory!)

---

## Running the Pipeline (After Setup)

### Option 1: Complete Startup Script (Recommended)
```bash
cd /scratch/bds9746/viz_evaluation_pipeline
./start_pipeline.sh
```

This handles:
- Activating Python environment
- Starting Ollama if needed
- Checking dataset
- Running the pipeline
- Showing results

### Option 2: Manual Steps
```bash
# Activate environment
source /scratch/bds9746/viz_evaluation_pipeline/setup_env.sh

# Start Ollama (if not running)
nohup /scratch/bds9746/ollama/ollama serve > /scratch/bds9746/ollama/server.log 2>&1 &

# Run pipeline
cd /scratch/bds9746/viz_evaluation_pipeline/src
python pipeline.py
```

---

## Common Commands

### Check Ollama Status
```bash
curl http://localhost:11434/api/tags
```

### List Downloaded Models
```bash
/scratch/bds9746/ollama/ollama list
```

### Download Different Model
```bash
/scratch/bds9746/ollama/ollama pull llama3.2:1b  # Smaller, faster
/scratch/bds9746/ollama/ollama pull codellama    # Code-focused
```

### Stop Ollama
```bash
kill $(cat /scratch/bds9746/ollama/ollama.pid)
```

### View Ollama Logs
```bash
tail -f /scratch/bds9746/ollama/server.log
```

### Activate Python Environment Only
```bash
source /scratch/bds9746/viz_evaluation_pipeline/venv/bin/activate
```

### View Available Prompts
```bash
cd /scratch/bds9746/viz_evaluation_pipeline/src
python prompts.py
```

---

## File Locations

| What | Where |
|------|-------|
| Project | `/scratch/bds9746/viz_evaluation_pipeline/` |
| Python venv | `/scratch/bds9746/viz_evaluation_pipeline/venv/` |
| Ollama binary | `/scratch/bds9746/ollama/ollama` |
| AI models | `/scratch/bds9746/ollama/models/` |
| Dataset | `/scratch/bds9746/viz_evaluation_pipeline/data/titanic.csv` |
| Results | `/scratch/bds9746/viz_evaluation_pipeline/outputs/` |
| Visualizations | `/scratch/bds9746/viz_evaluation_pipeline/outputs/visualizations/` |
| Metrics | `/scratch/bds9746/viz_evaluation_pipeline/outputs/metrics/` |
| Reports | `/scratch/bds9746/viz_evaluation_pipeline/outputs/logs/` |

---

## Pipeline Configuration

Edit `config/config.yaml` to change:
- Model name
- Number of retries (default: 3)
- API endpoint
- Output directories

---

## Testing Different Prompts

```python
# In Python (with venv activated)
from prompts import get_prompt, get_all_prompt_ids

# See all 12 available prompts
print(get_all_prompt_ids())

# Get a specific prompt
prompt = get_prompt("08_comprehensive_dashboard")
print(prompt)

# Get expected insights for a prompt
from prompts import get_expected_insights
insights = get_expected_insights("02_gender_survival")
```

---

## Disk Space

### Check Usage
```bash
du -sh /scratch/bds9746/viz_evaluation_pipeline
du -sh /scratch/bds9746/ollama
```

### Clean Old Outputs
```bash
rm -rf /scratch/bds9746/viz_evaluation_pipeline/outputs/*
```

### Model Sizes
- llama3.2: ~2 GB
- llama3.2:1b: ~1 GB (recommended for testing)
- codellama: ~4 GB

---

## Troubleshooting

### "Virtual environment not found"
```bash
cd /scratch/bds9746/viz_evaluation_pipeline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### "Ollama not running"
```bash
# Start Ollama
nohup /scratch/bds9746/ollama/ollama serve > /scratch/bds9746/ollama/server.log 2>&1 &
echo $! > /scratch/bds9746/ollama/ollama.pid
```

### "Model not found"
```bash
# Download model
/scratch/bds9746/ollama/ollama pull llama3.2:1b
```

### "Dataset not found"
```bash
cd /scratch/bds9746/viz_evaluation_pipeline
python download_data.py
```

### Check What's Wrong
```bash
# Check Python
which python
python --version

# Check packages
pip list | grep pandas

# Check Ollama
curl http://localhost:11434/api/tags

# Check dataset
ls -lh /scratch/bds9746/viz_evaluation_pipeline/data/

# Check Ollama logs
tail -20 /scratch/bds9746/ollama/server.log
```

---

## Expected Output

After a successful run:
```
outputs/
├── visualizations/
│   ├── llama3.2_titanic_attempt1_20250130_143022.png
│   ├── llama3.2_titanic_attempt1_20250130_143022.py
│   ├── llama3.2_titanic_attempt2_20250130_143145.png
│   ├── llama3.2_titanic_attempt2_20250130_143145.py
│   ├── llama3.2_titanic_attempt3_20250130_143312.png
│   └── llama3.2_titanic_attempt3_20250130_143312.py
├── metrics/
│   ├── llama3.2_titanic_attempt1_metrics.json
│   ├── llama3.2_titanic_attempt2_metrics.json
│   └── llama3.2_titanic_attempt3_metrics.json
└── logs/
    ├── pipeline_results_20250130_143312.json
    └── summary_report_20250130_143312.txt
```

---

## Documentation Files

| File | Purpose |
|------|---------|
| `CHEATSHEET.md` | This file - quick commands |
| `SETUP_INSTRUCTIONS.md` | Detailed setup guide |
| `QUICKSTART.md` | Quick start guide |
| `README.md` | Full documentation |
| `PROJECT_OVERVIEW.md` | Complete project overview |

---

## One-Liners

```bash
# Complete first-time setup
cd /scratch/bds9746/viz_evaluation_pipeline && ./initial_setup.sh

# Run pipeline (after setup)
cd /scratch/bds9746/viz_evaluation_pipeline && ./start_pipeline.sh

# View latest results
cat /scratch/bds9746/viz_evaluation_pipeline/outputs/logs/summary_report_*.txt | tail -50

# List all generated visualizations
ls -lht /scratch/bds9746/viz_evaluation_pipeline/outputs/visualizations/*.png

# Check disk usage
du -sh /scratch/bds9746/{viz_evaluation_pipeline,ollama}
```

---

**Everything is in `/scratch/bds9746` - No home directory files!**
