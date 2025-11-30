# AI Visualization Evaluation Pipeline - Quick Start Guide

## What We Built

A comprehensive research pipeline for evaluating AI models' ability to generate data visualizations, based on your research papers.

### Key Features

1. **12 Different Test Prompts**
   - Common base prompt describing Titanic dataset
   - 12 specific visualization tasks (survival by class, gender analysis, age distribution, etc.)
   - Each prompt has expected insights for accuracy measurement

2. **Comprehensive Metrics** (from your research paper)
   - **Fidelity Score**: Data accuracy measurement
   - **Color ΔE**: Color distinguishability (threshold: ΔE > 3)
   - **Visual Entropy**: Complexity measurement
   - **Code Accuracy**: Technical correctness
   - **Task Completion Time**: Efficiency measure
   - **Accuracy/Error Rate**: Insight extraction correctness
   - **Expert Quality Rating**: Template for professional assessment
   - **User Satisfaction**: Template for user feedback

3. **3-Attempt System**
   - Each visualization task gets 3 independent attempts
   - Results saved as: `{model}_{dataset}_attempt{1-3}_{timestamp}.png`
   - Metrics calculated for each attempt

4. **Open Source Model Support**
   - Uses Ollama for local, free inference
   - Can be configured for any open-source model (LLaMA, CodeLLaMA, Phi, etc.)
   - Also supports OpenAI-compatible APIs

## Installation & Setup

### Step 1: Install Ollama (Recommended)

```bash
# Visit https://ollama.ai and install for your OS

# Pull LLaMA 3.2 model
ollama pull llama3.2

# Start Ollama server
ollama serve
```

### Step 2: Install Python Dependencies

```bash
cd /scratch/bds9746/viz_evaluation_pipeline
pip install -r requirements.txt
```

### Step 3: Download Dataset

```bash
python download_data.py
```

## Usage

### Option 1: Quick Start Script

```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

### Option 2: Manual Execution

```bash
cd src
python pipeline.py
```

### Option 3: Test Specific Prompts

```python
from prompts import get_prompt, get_all_prompt_ids

# See all available prompts
print(get_all_prompt_ids())

# Get a specific prompt
prompt = get_prompt("02_gender_survival")
print(prompt)
```

## Pipeline Flow

```
1. Load Configuration
   ↓
2. For each of 3 attempts:
   ├─ Call AI model API with prompt
   ├─ Extract Python code from response
   ├─ Execute code to generate visualization
   ├─ Save visualization as: {model}_{dataset}_attempt{N}_{timestamp}.png
   ├─ Calculate all metrics
   └─ Save metrics as JSON
   ↓
3. Generate Summary Report
```

## Output Structure

After running the pipeline, you'll have:

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

## Available Test Prompts

| ID | Prompt Name | Focus |
|----|-------------|-------|
| 01 | Survival Rate by Passenger Class | Class-based survival disparity |
| 02 | Gender-Based Survival Analysis | "Women and children first" policy |
| 03 | Age Distribution and Survival | Age vs. survival patterns |
| 04 | Fare Price and Survival Correlation | Economic factors |
| 05 | Family Size Impact on Survival | Optimal family size |
| 06 | Port of Embarkation and Survival | Geographic patterns |
| 07 | Multi-Factor Survival Heatmap | Correlation analysis |
| 08 | Comprehensive Titanic Dashboard | Multi-panel overview |
| 09 | Class-Gender Interaction Effect | Interaction effects |
| 10 | Survival Decision Tree Visualization | Hierarchical patterns |
| 11 | Missing Data Pattern Analysis | Data quality analysis |
| 12 | Fare Distribution Across Classes | Price stratification |

## Customization

### Using Different Models

Edit `config/config.yaml`:

```yaml
model:
  name: "codellama:34b"  # or llama3.1:70b, phi3, etc.
  api_type: "ollama"
  api_base: "http://localhost:11434"
```

### Testing Specific Prompts

Modify [pipeline.py](src/pipeline.py:200) to use a specific prompt:

```python
# In pipeline.py, modify get_prompt call:
from prompts import get_prompt

# Use a specific prompt
prompt = get_prompt("08_comprehensive_dashboard")
```

### Running Multiple Prompts

Create a loop in the pipeline to test all 12 prompts:

```python
from prompts import get_all_prompt_ids

for prompt_id in get_all_prompt_ids():
    pipeline.run_full_pipeline(prompt_id=prompt_id)
```

## Metrics Explained

### Automated Metrics

**Fidelity Score** (0-100%, higher = better)
- Compares statistical properties of visualization vs. original data
- Checks mean, std, min, max for accuracy

**Color ΔE** (ΔE > 3 = distinguishable)
- Uses CIE2000 formula for color difference
- Reports: min, max, mean, % of distinguishable color pairs

**Visual Entropy** (0-10+, moderate = good)
- Measures visual complexity using color entropy + edge density
- 2-4: Simple, 4-6: Moderate, >6: Complex

**Code Accuracy** (0-100%)
- Checks: syntax validity, imports, visualization creation, file saving

**Task Completion Time** (seconds)
- Measures time from API call to visualization completion

### Human Feedback Metrics (Templates Provided)

**Expert Quality Rating** (1-5 scale)
- Clarity, appropriateness, completeness, aesthetics, accuracy

**User Satisfaction Score** (1-5 scale)
- Ease of understanding, usefulness, trustworthiness, likelihood to use

## Example Metrics Output

```json
{
  "image_path": "outputs/visualizations/llama3.2_titanic_attempt1.png",
  "timestamp": "2025-01-30T14:30:22",
  "color_delta_e": {
    "mean_delta_e": 18.3,
    "distinguishability_ratio": 0.95,
    "distinguishable_pairs": 42,
    "total_pairs": 45
  },
  "visual_entropy": 4.52,
  "code_accuracy": {
    "syntax_valid": true,
    "accuracy_score": 100.0
  },
  "task_completion_time": {
    "completion_time_seconds": 45.2,
    "completion_time_minutes": 0.75
  }
}
```

## Research Applications

This pipeline is designed for:

1. **Model Comparison**
   - Test multiple models (LLaMA, CodeLLaMA, GPT, Claude, etc.)
   - Compare metrics across models
   - Identify best-performing models for visualization

2. **Prompt Engineering**
   - Test different prompt formulations
   - Measure impact of prompt details on quality
   - Optimize prompts for better visualizations

3. **Consistency Analysis**
   - 3 attempts show model consistency/variability
   - Measure reliability of AI-generated visualizations
   - Identify when models produce inconsistent results

4. **Quality Benchmarking**
   - Establish baseline metrics for AI visualization quality
   - Compare against human-created visualizations
   - Track improvements over time

## Troubleshooting

**Issue**: API connection failed
**Solution**: Make sure Ollama is running (`ollama serve`)

**Issue**: Model not found
**Solution**: Pull the model first (`ollama pull llama3.2`)

**Issue**: Code execution timeout
**Solution**: Increase timeout in [pipeline.py](src/pipeline.py:300) (default: 60s)

**Issue**: Missing dependencies
**Solution**: `pip install -r requirements.txt`

## Next Steps

1. **Run the pipeline** with default settings
2. **Examine outputs** in `outputs/` directory
3. **Review metrics** to understand model performance
4. **Try different prompts** from the 12 available
5. **Test different models** by changing config
6. **Add your own prompts** by editing `src/prompts.py`
7. **Compare models** by running pipeline with multiple models

## File Reference

| File | Purpose |
|------|---------|
| [config/config.yaml](config/config.yaml) | Pipeline configuration |
| [src/pipeline.py](src/pipeline.py) | Main pipeline orchestrator |
| [src/prompts.py](src/prompts.py) | 12 test prompts + base prompt |
| [src/metrics.py](src/metrics.py) | All metric calculations |
| [download_data.py](download_data.py) | Dataset download script |
| [run_pipeline.sh](run_pipeline.sh) | Quick start script |

## Support

For issues or questions:
1. Check the [README.md](README.md) for detailed documentation
2. Review your research papers for metric definitions
3. Examine the code comments in source files

---

**Happy Researching!**
