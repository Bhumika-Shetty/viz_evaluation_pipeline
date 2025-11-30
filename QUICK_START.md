# Quick Start Guide - Prompt-Organized Pipeline

## ✨ What's New?

Each prompt now has its own dedicated folder! This makes it easy to:
- Compare all 3 attempts for a single prompt
- Analyze prompt-specific results
- Keep visualizations, code, and metrics organized

## 📁 New Folder Structure

```
outputs/
├── prompt_01_survival_by_class/
│   ├── visualizations/    # 3 PNG files (attempt 1, 2, 3)
│   ├── code/             # 3 PY files  (attempt 1, 2, 3)
│   └── metrics/          # 3 JSON files (attempt 1, 2, 3)
├── prompt_02_gender_survival/
│   ├── visualizations/
│   ├── code/
│   └── metrics/
├── ... (prompt_03 through prompt_12)
└── logs/
    ├── pipeline_results_TIMESTAMP.json
    └── summary_report_TIMESTAMP.txt
```

## 🚀 Quick Commands

### Run Quick Test (2 prompts)
```bash
cd /scratch/bds9746/viz_evaluation_pipeline
./run_test.sh
```

### Run Full Pipeline (12 prompts)
```bash
cd /scratch/bds9746/viz_evaluation_pipeline
./run_all.sh
```

## 📊 View Results

### See all prompt folders
```bash
ls outputs/
```

### Check results for a specific prompt
```bash
# List all files for prompt 01
ls -R outputs/prompt_01_survival_by_class/

# View just the visualizations
ls outputs/prompt_01_survival_by_class/visualizations/

# View metrics for attempt 1
cat outputs/prompt_01_survival_by_class/metrics/*attempt1*.json | python -m json.tool
```

### Count total visualizations
```bash
find outputs/prompt_*/visualizations -name "*.png" | wc -l
```

### Compare all attempts for one prompt
```bash
# See all 3 attempts side by side
ls -lh outputs/prompt_01_survival_by_class/visualizations/
```

## 🎯 Benefits for Research

### Easy Prompt Comparison
All attempts for one prompt are in the same folder - makes it easy to:
- Compare consistency across 3 attempts
- Analyze metrics for each prompt separately
- Identify which prompts work best

### Clean Organization
```
prompt_01_survival_by_class/
├── visualizations/  ← All images here
├── code/           ← All Python files here
└── metrics/        ← All metric JSONs here
```

No more searching through a flat folder with 100+ files!

### Research Analysis Examples

**Analyze consistency for prompt 01:**
```bash
cat outputs/prompt_01_survival_by_class/metrics/*.json | \
  python -c "import sys, json; metrics = [json.loads(l) for l in sys.stdin if l.strip()]; \
  print('Mean Color ΔE:', sum(m['color_delta_e']['mean_delta_e'] for m in metrics)/len(metrics))"
```

**Compare success rates across prompts:**
```bash
for dir in outputs/prompt_*/; do
  count=$(ls $dir/visualizations/*.png 2>/dev/null | wc -l)
  echo "$(basename $dir): $count/3 successful"
done
```

## 🔍 What Each Prompt Tests

| Prompt ID | Focus Area | Visualization Type |
|-----------|------------|-------------------|
| 01 | Survival by class | Bar chart |
| 02 | Gender survival | Comparative analysis |
| 03 | Age distribution | Histogram/density |
| 04 | Fare vs survival | Scatter/correlation |
| 05 | Family size impact | Grouped analysis |
| 06 | Embarkation patterns | Geographic/categorical |
| 07 | Multi-factor heatmap | Correlation matrix |
| 08 | Comprehensive dashboard | Multi-panel layout |
| 09 | Class-gender interaction | Interaction effects |
| 10 | Decision tree | Hierarchical patterns |
| 11 | Missing data | Data quality analysis |
| 12 | Fare distribution | Box plot/violin |

## 📈 Expected Output

After running `./run_all.sh`:

```
✓ 12 prompt folders created
✓ Each with 3 attempts
✓ Total: 36 visualizations + 36 code files + 36 metric files
✓ Plus 2 summary reports
```

## ⚡ Tips

1. **Start with test**: Run `./run_test.sh` first to verify everything works
2. **Check one prompt**: Navigate to a specific prompt folder to see all attempts together
3. **Compare visually**: Open all PNG files in one prompt folder to compare attempts
4. **Analyze metrics**: Each prompt's metrics are in its own folder for easy analysis

## 🎓 For Your Paper

This structure is perfect for research because:
- ✅ Each prompt is a separate test case
- ✅ 3 attempts measure consistency
- ✅ Easy to generate statistics per prompt
- ✅ Clean structure for figures in paper
- ✅ Organized metrics for quantitative analysis

---

**Ready to run? Start with:**
```bash
cd /scratch/bds9746/viz_evaluation_pipeline
./run_test.sh
```
