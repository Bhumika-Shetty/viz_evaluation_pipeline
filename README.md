# AI Visualization Evaluation Pipeline

A comprehensive pipeline for evaluating AI models' performance in data visualization tasks, based on the research paper "Evaluating the Performance of AI Models in Data Visualization."

## Overview

This pipeline:
1. **Calls an AI model API** to generate data visualization code
2. **Executes the code 3 times** (giving the model 3 chances to produce results)
3. **Saves visualizations** with proper naming (`model_dataset_attempt{N}_timestamp.png`)
4. **Calculates evaluation metrics** as defined in the research paper
5. **Generates comprehensive reports** with all results

## Research Background

This implementation is based on the evaluation framework proposed in the research paper which evaluates AI models using:

### Automated Metrics (No Human Feedback Required)

1. **Fidelity Score**: Measures how truthfully data is represented
   - Formula: `(Accurate Data Points / Total Points) × 100`
   - Higher = Better

2. **Color ΔE (Delta E)**: Ensures color distinguishability
   - Formula: `√((L₁-L₂)² + (a₁-a₂)² + (b₁-b₂)²)`
   - Threshold: ΔE > 3 = distinguishable colors

3. **Visual Entropy**: Measures complexity/randomness of visual elements
   - Formula: `H(X) = -Σ pᵢ × log₂(pᵢ)`
   - Captures variety in colors, shapes, patterns

4. **Code Generation Accuracy**: Technical correctness measure
   - Checks syntax, imports, visualization creation, file saving

## Project Structure

```
viz_evaluation_pipeline/
├── config/
│   └── config.yaml              # Configuration file
├── data/
│   └── titanic.csv              # Titanic dataset
├── src/
│   ├── pipeline.py              # Main pipeline orchestrator
│   ├── prompts.py               # Detailed visualization prompts
│   └── metrics.py               # Metric calculation functions
├── outputs/
│   ├── visualizations/          # Generated visualizations and code
│   ├── metrics/                 # Calculated metrics (JSON)
│   └── logs/                    # Pipeline logs and reports
├── download_data.py             # Dataset download script
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed and running (for local models)
  - OR access to OpenAI-compatible API

### Step 1: Install Python Dependencies

```bash
cd viz_evaluation_pipeline
pip install -r requirements.txt
```

### Step 2: Install and Run Ollama (Recommended)

This pipeline uses Ollama for local, free, open-source model inference.

1. **Install Ollama**: Visit [https://ollama.ai/](https://ollama.ai/) and follow installation instructions

2. **Pull a model** (LLaMA 3.2 recommended):
   ```bash
   ollama pull llama3.2
   ```

3. **Start Ollama server**:
   ```bash
   ollama serve
   ```

   The server will run on `http://localhost:11434` by default.

#### Alternative Models:
```bash
# Larger, more capable models
ollama pull llama3.1:70b
ollama pull codellama:34b

# Smaller, faster models
ollama pull llama3.2:1b
ollama pull phi3
```

### Step 3: Download Dataset

```bash
python download_data.py
```

This will download the Titanic dataset to the `data/` directory.

## Configuration

Edit `config/config.yaml` to customize the pipeline:

```yaml
model:
  name: "llama3.2"                    # Model name
  api_type: "ollama"                  # "ollama" or "openai"
  api_base: "http://localhost:11434"  # API endpoint
  temperature: 0.7                    # Generation temperature
  max_retries: 3                      # Number of attempts

dataset:
  name: "titanic"
  path: "data/titanic.csv"

outputs:
  visualizations_dir: "outputs/visualizations"
  metrics_dir: "outputs/metrics"
  logs_dir: "outputs/logs"
  save_code: true
  save_images: true

metrics:
  calculate_fidelity: true
  calculate_color_delta_e: true
  calculate_visual_entropy: true
  calculate_code_accuracy: true
```

## Usage

### Run the Full Pipeline

```bash
cd src
python pipeline.py
```

### What Happens:

1. **Attempt 1**: Model generates visualization code → Executes → Calculates metrics → Saves as `llama3.2_titanic_attempt1_TIMESTAMP.png`

2. **Attempt 2**: Fresh generation (independent of attempt 1) → Executes → Calculates metrics → Saves as `llama3.2_titanic_attempt2_TIMESTAMP.png`

3. **Attempt 3**: Fresh generation → Executes → Calculates metrics → Saves as `llama3.2_titanic_attempt3_TIMESTAMP.png`

4. **Summary Report**: Generated in `outputs/logs/summary_report_TIMESTAMP.txt`

### Output Files

After running, you'll find:

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

## Understanding the Metrics

### Example Metrics Output

```json
{
  "image_path": "outputs/visualizations/llama3.2_titanic_attempt1.png",
  "timestamp": "2025-01-30T14:30:22",
  "color_delta_e": {
    "min_delta_e": 5.2,
    "max_delta_e": 45.8,
    "mean_delta_e": 18.3,
    "distinguishability_ratio": 0.95,
    "distinguishable_pairs": 42,
    "total_pairs": 45
  },
  "visual_entropy": 4.52,
  "code_accuracy": {
    "syntax_valid": true,
    "has_imports": true,
    "has_visualization": true,
    "has_save": true,
    "accuracy_score": 100.0
  }
}
```

### Interpreting Results

- **Color ΔE**:
  - Mean > 10: Good color separation
  - Distinguishability ratio > 0.8: Most colors are distinguishable

- **Visual Entropy**:
  - 2-4: Simple, clean visualization
  - 4-6: Moderate complexity
  - > 6: High complexity (may be cluttered)

- **Code Accuracy**:
  - 100%: All checks passed
  - < 100%: Missing some elements

## The Visualization Prompt

The pipeline uses a highly detailed prompt that includes:

- **Dataset context**: Background information about Titanic dataset
- **Schema description**: All columns with data types and meanings
- **Task description**: What insights to reveal (survival patterns)
- **Technical requirements**: Python libraries, code structure, file saving
- **Design principles**: Clarity, accessibility, fidelity, interpretability
- **Visual guidance**: Suggested chart types, elements to include
- **Statistical considerations**: Handling missing data, showing distributions

View the full prompt in `src/prompts.py`.

## Customization

### Using Different Models

**With Ollama:**
```yaml
# In config/config.yaml
model:
  name: "codellama:34b"  # Any Ollama model
```

**With OpenAI API:**
```yaml
model:
  name: "gpt-4"
  api_type: "openai"
  api_base: "https://api.openai.com/v1"
```

Then set environment variable:
```bash
export OPENAI_API_KEY="your-api-key"
```

### Adding New Datasets

1. Add dataset to `data/` directory
2. Update `config/config.yaml`:
   ```yaml
   dataset:
     name: "your_dataset"
     path: "data/your_dataset.csv"
   ```
3. (Optional) Create custom prompt in `src/prompts.py`

## Research Context

This pipeline implements the methodology from:

**"Evaluating the Performance of AI Models in Data Visualization"**

The research evaluates models like ChatGPT, Gemini, Claude using datasets like Titanic, Iris, Customer Segments, and Credit Fraud.

Key research gaps addressed:
- Lack of quantitative evaluation frameworks
- No multi-run consistency testing
- Missing composite metrics (combining objective + subjective)
- Need for automated quality assessment

## Troubleshooting

### Issue: "Connection refused" when calling API

**Solution**: Make sure Ollama is running:
```bash
ollama serve
```

### Issue: "Model not found"

**Solution**: Pull the model first:
```bash
ollama pull llama3.2
```

### Issue: Code execution fails

**Check**:
- Python dependencies are installed
- Generated code has correct syntax
- Dataset path is correct in config

### Issue: No visualization generated

**Check**:
- Code saves to 'output.png' or the pipeline modifies the path
- Execution timeout (increase in `pipeline.py` if needed)
- Check stderr output in logs

## Contributing

Contributions are welcome! Areas for improvement:

- [ ] Add support for more AI model APIs (Anthropic, Google, etc.)
- [ ] Implement human-feedback metrics (SUS score, Interpretability)
- [ ] Add more datasets (Iris, Customer Segments, Credit Fraud)
- [ ] Create comparison reports across multiple models
- [ ] Implement automated ground truth validation

## License

This project is for research and educational purposes.

## Citation

If you use this pipeline in your research, please cite:

```
AI Visualization Evaluation Pipeline
Based on: "Evaluating the Performance of AI Models in Data Visualization"
```

## Contact

For questions or issues, please open an issue on GitHub.

---

**Happy Evaluating!**
