"""
Prompt:

You are an expert data scientist.

## Dataset Context:
(Use the same Titanic context as before...)

## Your Task: Comprehensive Titanic Dashboard

Create a multi-panel dashboard showing 4-6 different aspects of the Titanic data.

**Specific Requirements:**
- Use subplots to create a dashboard layout (2x3 or 3x2)
- Include: survival by class, by gender, age distribution, fare distribution, family size, embarkation
- Make it publication-ready with consistent styling
- Add a main title: "Titanic Disaster: Comprehensive Survival Analysis"
- Ensure all subplots are properly labeled

**Expected Insights:**
- Comprehensive view of all major factors affecting survival
- Visual story of the disaster
- Multiple patterns visible at once

## Output Format:
Provide ONLY the Python code wrapped in triple backticks.
"""

# =========================
# MANUAL FIXES APPLIED (DOCUMENTED)
#
# Context:
# - Model output was obtained via Gemini 3 Pro UI (manual workflow).
#
# Issues observed when running raw model code locally:
#  1) Dataset path assumption:
#     - Raw: pd.read_csv('titanic.csv')
#     - Repo uses: data/titanic.csv
#     - Fix: pd.read_csv('titanic.csv') -> pd.read_csv('data/titanic.csv')
#
#  2) No saved image for grading:
#     - Raw ended with plt.show() only (no saved PNG)
#     - Fix: save figure to PNG and close:
#         plt.savefig('titanic_dashboard.png', dpi=300, bbox_inches='tight'); plt.close()
#
#  3) Runtime crash (seaborn palette key mismatch):
#     - Error: ValueError about palette dict missing keys {'0','1'} or {0,1} depending on plot
#     - Cause: seaborn treats categorical levels as strings in some plots and ints in others
#     - Fix: enforce consistent categorical type for 'survived' by casting to string once:
#         df['survived'] = df['survived'].astype(str)
#       and use palette/labels with string keys {'0','1'} for all hue-based plots.
#
#  4) Survival-rate (mean) plot requires numeric y:
#     - After casting survived to str for palette consistency, barplot mean won't work.
#     - Fix: add numeric helper column survived_num for Plot 5 only:
#         df['survived_num'] = df['survived'].astype(int)
#
# Notes:
# - No changes were made to the dashboard structure (2x3), plot types, or intended insights.
# - Changes are strictly to ensure local executability + image generation + seaborn compatibility.
# =========================

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load the dataset (manual fix: path)
df = pd.read_csv('data/titanic.csv')

# Manual fix: enforce consistent categorical type for seaborn palette mapping
df['survived'] = df['survived'].astype(str)

# Manual fix: numeric helper for survival-rate (mean) computation in Plot 5
df['survived_num'] = df['survived'].astype(int)

# Preprocessing: Create Family Size feature (SibSp + Parch + Self)
df['family_size'] = df['sibsp'] + df['parch'] + 1

# Set the aesthetic style
sns.set_theme(style="whitegrid")

# Create a figure and a 2x3 grid of subplots
fig, axes = plt.subplots(2, 3, figsize=(20, 12))
fig.suptitle(
    'Titanic Disaster: Comprehensive Survival Analysis',
    fontsize=24,
    fontweight='bold',
    y=0.98
)

# Define a consistent color palette for survival (string keys to match df['survived'] dtype)
survival_palette = {'0': "#e74c3c", '1': "#2ecc71"}  # Red for Died, Green for Survived
labels = {'0': 'Did Not Survive', '1': 'Survived'}

# --- Plot 1: Survival by Pclass (Countplot) ---
sns.countplot(data=df, x='pclass', hue='survived', palette=survival_palette, ax=axes[0, 0])
axes[0, 0].set_title('Survival Count by Passenger Class', fontsize=14)
axes[0, 0].set_xlabel('Passenger Class')
axes[0, 0].set_ylabel('Count')
axes[0, 0].legend(title='Status', labels=[labels['0'], labels['1']])

# --- Plot 2: Survival by Gender (Countplot) ---
sns.countplot(data=df, x='sex', hue='survived', palette=survival_palette, ax=axes[0, 1])
axes[0, 1].set_title('Survival Count by Gender', fontsize=14)
axes[0, 1].set_xlabel('Gender')
axes[0, 1].set_ylabel('Count')
axes[0, 1].legend(title='Status', labels=[labels['0'], labels['1']])

# --- Plot 3: Age Distribution (KDE Plot) ---
sns.kdeplot(
    data=df,
    x='age',
    hue='survived',
    fill=True,
    palette=survival_palette,
    alpha=0.5,
    ax=axes[0, 2]
)
axes[0, 2].set_title('Age Distribution by Survival Status', fontsize=14)
axes[0, 2].set_xlabel('Age (Years)')
axes[0, 2].set_ylabel('Density')
# Keep legend consistent with palette keys; note: seaborn legend order may vary
axes[0, 2].legend(title='Status', labels=[labels['1'], labels['0']])

# --- Plot 4: Fare Distribution (Box Plot) ---
sns.boxplot(
    data=df,
    x='survived',
    y='fare',
    palette=survival_palette,
    ax=axes[1, 0],
    showfliers=False
)
axes[1, 0].set_title('Fare Distribution by Survival (Outliers Removed)', fontsize=14)
axes[1, 0].set_xlabel('Survival Status')
axes[1, 0].set_xticklabels([labels['0'], labels['1']])
axes[1, 0].set_ylabel('Fare (£)')

# --- Plot 5: Survival Rate by Family Size (Bar Plot) ---
# Use numeric helper column to compute mean survival rate
sns.barplot(
    data=df,
    x='family_size',
    y='survived_num',
    palette="viridis",
    errorbar=None,
    ax=axes[1, 1]
)
axes[1, 1].set_title('Survival Rate by Family Size', fontsize=14)
axes[1, 1].set_xlabel('Family Size (SibSp + Parch + 1)')
axes[1, 1].set_ylabel('Survival Probability')
axes[1, 1].axhline(y=df['survived_num'].mean(), color='grey', linestyle='--', label='Global Average')
axes[1, 1].legend()

# --- Plot 6: Survival by Embarkation Town (Countplot) ---
sns.countplot(data=df, x='embark_town', hue='survived', palette=survival_palette, ax=axes[1, 2])
axes[1, 2].set_title('Survival Count by Embarkation Town', fontsize=14)
axes[1, 2].set_xlabel('Embarkation Town')
axes[1, 2].set_ylabel('Count')
axes[1, 2].legend(title='Status', labels=[labels['0'], labels['1']])

# Adjust layout to prevent overlap
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Manual fix: save image for grading (instead of plt.show())
plt.savefig('titanic_dashboard.png', dpi=300)
plt.close()
