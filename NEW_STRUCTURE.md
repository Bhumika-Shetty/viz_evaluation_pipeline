# ✅ IMPROVED PIPELINE - Clear Structure

## What Changed

### ✅ Now Runs ALL 12 Prompts
- **Before**: Only 1 prompt × 3 attempts = 3 visualizations
- **Now**: 12 prompts × 3 attempts = **36 visualizations**

### ✅ Better File Organization
- **Before**: Outputs in `src/outputs/` (confusing)
- **Now**: Organized by prompt in `/scratch/bds9746/viz_evaluation_pipeline/outputs/` (clean)
- **Each prompt**: Gets its own folder with visualizations/, code/, and metrics/ subdirectories

### ✅ Clearer File Organization
- **Before**: All files in one folder
- **Now**: Each prompt has its own folder

Example Structure:
```
outputs/
├── prompt_01_survival_by_class/
│   ├── visualizations/
│   │   ├── llama-3.3-70b-versatile_attempt1_20251130_173000.png
│   │   ├── llama-3.3-70b-versatile_attempt2_20251130_173010.png
│   │   └── llama-3.3-70b-versatile_attempt3_20251130_173020.png
│   ├── code/
│   │   ├── llama-3.3-70b-versatile_attempt1_20251130_173000.py
│   │   ├── llama-3.3-70b-versatile_attempt2_20251130_173010.py
│   │   └── llama-3.3-70b-versatile_attempt3_20251130_173020.py
│   └── metrics/
│       ├── llama-3.3-70b-versatile_attempt1_metrics.json
│       ├── llama-3.3-70b-versatile_attempt2_metrics.json
│       └── llama-3.3-70b-versatile_attempt3_metrics.json
├── prompt_02_gender_survival/
│   ├── visualizations/
│   ├── code/
│   └── metrics/
...
```

---

## 📁 New Directory Structure

```
/scratch/bds9746/viz_evaluation_pipeline/
├── venv/                          # Python environment
├── data/
│   └── titanic.csv               # Dataset
├── config/
│   └── config.yaml               # Configuration
├── src/
│   ├── pipeline_v2.py            # ✨ NEW: Enhanced pipeline (all prompts)
│   ├── pipeline.py               # OLD: Original (1 prompt only)
│   ├── prompts.py                # 12 test prompts
│   └── metrics.py                # Metric calculations
├── outputs/                       # ✨ NEW: Organized by prompt
│   ├── prompt_01_survival_by_class/
│   │   ├── visualizations/       # PNG files for prompt 01
│   │   ├── code/                 # PY files for prompt 01
│   │   └── metrics/              # JSON metrics for prompt 01
│   ├── prompt_02_gender_survival/
│   │   ├── visualizations/
│   │   ├── code/
│   │   └── metrics/
│   ├── ... (prompt_03 through prompt_12)
│   └── logs/                     # Summary reports
├── run_all.sh                    # ✨ NEW: Run all 12 prompts (36 viz)
├── run_test.sh                   # ✨ NEW: Quick test (2 prompts, 6 viz)
└── run.sh                        # OLD: Original (1 prompt, 3 viz)
```

---

## 🚀 How to Use

### Option 1: Quick Test (Recommended First)
**2 prompts × 3 attempts = 6 visualizations (~3 minutes)**

```bash
cd /scratch/bds9746/viz_evaluation_pipeline
./run_test.sh
```

### Option 2: Full Run
**12 prompts × 3 attempts = 36 visualizations (~20-30 minutes)**

```bash
cd /scratch/bds9746/viz_evaluation_pipeline
./run_all.sh
```

### Option 3: Original (Old Way)
**1 prompt × 3 attempts = 3 visualizations (~2 minutes)**

```bash
cd /scratch/bds9746/viz_evaluation_pipeline
./run.sh
```

---

## 📊 The 12 Prompts

Each prompt tests different visualization capabilities:

| ID | Prompt Name | Focus |
|----|-------------|-------|
| 01 | Survival Rate by Passenger Class | Class disparity |
| 02 | Gender-Based Survival Analysis | Gender differences |
| 03 | Age Distribution and Survival | Age patterns |
| 04 | Fare Price and Survival Correlation | Economic factors |
| 05 | Family Size Impact on Survival | Optimal family size |
| 06 | Port of Embarkation and Survival | Geographic patterns |
| 07 | Multi-Factor Survival Heatmap | Correlation analysis |
| 08 | Comprehensive Titanic Dashboard | Multi-panel overview |
| 09 | Class-Gender Interaction Effect | Interaction effects |
| 10 | Survival Decision Tree | Hierarchical patterns |
| 11 | Missing Data Pattern Analysis | Data quality |
| 12 | Fare Distribution Across Classes | Price stratification |

---

## 📁 Output Files (After Full Run)

### Organized by Prompt (12 prompt folders)

Each prompt gets its own folder with all 3 attempts:

```
outputs/
├── prompt_01_survival_by_class/
│   ├── visualizations/
│   │   ├── llama-3.3-70b-versatile_attempt1_TIMESTAMP.png
│   │   ├── llama-3.3-70b-versatile_attempt2_TIMESTAMP.png
│   │   └── llama-3.3-70b-versatile_attempt3_TIMESTAMP.png
│   ├── code/
│   │   ├── llama-3.3-70b-versatile_attempt1_TIMESTAMP.py
│   │   ├── llama-3.3-70b-versatile_attempt2_TIMESTAMP.py
│   │   └── llama-3.3-70b-versatile_attempt3_TIMESTAMP.py
│   └── metrics/
│       ├── llama-3.3-70b-versatile_attempt1_metrics.json
│       ├── llama-3.3-70b-versatile_attempt2_metrics.json
│       └── llama-3.3-70b-versatile_attempt3_metrics.json
│
├── prompt_02_gender_survival/
│   ├── visualizations/ (3 PNG files)
│   ├── code/ (3 PY files)
│   └── metrics/ (3 JSON files)
│
├── prompt_03_age_distribution/
│   └── ... (same structure)
│
... (prompt_04 through prompt_12, each with same structure)
│
└── logs/
    ├── pipeline_results_TIMESTAMP.json     # Complete results
    └── summary_report_TIMESTAMP.txt        # Human-readable summary
```

**Total files: 109 files across 12 prompt folders**
- 12 prompt folders × 3 attempts each:
  - 36 PNG (visualizations)
  - 36 PY (code files)
  - 36 JSON (metrics)
- Plus 2 summary files in logs/

---

## 🎯 View Results

```bash
# See all prompt folders
ls /scratch/bds9746/viz_evaluation_pipeline/outputs/

# View results for a specific prompt (e.g., prompt 01)
ls /scratch/bds9746/viz_evaluation_pipeline/outputs/prompt_01_survival_by_class/

# See all visualizations for prompt 01
ls /scratch/bds9746/viz_evaluation_pipeline/outputs/prompt_01_survival_by_class/visualizations/*.png

# Count total visualizations across all prompts
find /scratch/bds9746/viz_evaluation_pipeline/outputs/prompt_*/visualizations -name "*.png" | wc -l

# View metrics for a specific attempt
cat /scratch/bds9746/viz_evaluation_pipeline/outputs/prompt_01_survival_by_class/metrics/*_attempt1*.json | python -m json.tool

# Read summary report
cat /scratch/bds9746/viz_evaluation_pipeline/outputs/logs/summary_report_*.txt

# Compare all attempts for one prompt
ls -lh /scratch/bds9746/viz_evaluation_pipeline/outputs/prompt_01_survival_by_class/visualizations/
```

---

## 📈 Expected Results

After running `./run_all.sh`:

```
✓ Total Prompts: 12
✓ Attempts per Prompt: 3
✓ Total Visualizations: 36
✓ Success Rate: ~80-100% (varies by prompt)
✓ Time: 20-30 minutes
✓ Output Size: ~10-15 MB
```

---

## 🔧 Comparison: Old vs New

| Feature | Old (`run.sh`) | New (`run_all.sh`) |
|---------|----------------|-------------------|
| Prompts | 1 | 12 |
| Attempts per prompt | 3 | 3 |
| Total visualizations | 3 | 36 |
| Output location | `src/outputs/` | `outputs/` |
| File organization | All in one folder | Organized by prompt |
| File naming | Generic | Clean, timestamped |
| Folder structure | Flat | Hierarchical (prompt/type/) |
| Easy comparison | ❌ No | ✅ Yes - grouped by prompt |
| Time | ~2 min | ~25 min |
| Research value | Limited | Complete |

---

## 💡 Recommendations

1. **Start with test**: Run `./run_test.sh` first to verify everything works
2. **Then full run**: Run `./run_all.sh` for complete results
3. **Review outputs**: Check `outputs/logs/summary_report_*.txt` for overview
4. **Analyze by prompt**: Group results by prompt ID to compare

---

## 🎓 For Your Research

The new structure gives you:

- ✅ **12 different visualization tasks** (comprehensive evaluation)
- ✅ **3 attempts each** (consistency analysis)
- ✅ **Organized by prompt** (each prompt has its own folder)
- ✅ **Separated by type** (visualizations/, code/, metrics/ in each folder)
- ✅ **Easy comparison** (all attempts for one prompt are together)
- ✅ **Clean naming** (timestamp-based, no confusion)
- ✅ **Complete metrics** (Color ΔE, Visual Entropy, Code Accuracy, etc.)
- ✅ **Research-ready structure** (perfect for analysis and comparison)

Perfect for your research paper! 📊
