'''
Prompt (parity, verbatim):
Prompt :
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
'''

# =========================
# MANUAL FIXES APPLIED (DOCUMENTED) — FAIR / MINIMAL EXECUTABILITY FIXES
#
# Why fixes were needed:
# The raw Llama (good-context) dashboard code was NOT directly runnable / gradable in our local repo:
#
#  1) Dependency hallucination:
#     - Raw code imported SciPy: `from scipy import stats`, but SciPy is not installed -> crash.
#     - Fix: removed SciPy dependency and replaced the Q-Q plot with a standard, library-free histogram/KDE-style plot.
#
#  2) Dataset path + filename assumption:
#     - Raw code attempted: pd.read_csv('titanic_data.csv')
#     - Our dataset is located at: data/titanic.csv
#     - Fix: pd.read_csv('titanic_data.csv') -> pd.read_csv('data/titanic.csv')
#
#  3) Schema mismatch (case + wrong columns):
#     - Raw code referenced 'Survived', 'Sex', 'Age', 'Fare', 'SibSp', 'Parch', 'Embarked'
#     - Our dataset uses lowercase: survived, sex, age, fare, sibsp, parch, embarked
#     - Fix: updated all column references accordingly.
#
#  4) Logic/semantic issues in raw plots:
#     - "Survival by Class" plot used overall survived counts and mislabeled as by class.
#     - "Survival by Gender" plotted counts of sex, not survival by sex.
#     - Embarkation and family-size bars used fixed 2-color lists that don't match category counts.
#     - Fix: replaced panels with correct, dataset-derived summaries aligned to the prompt:
#         (a) Survival by class (rate)
#         (b) Survival by gender (rate)
#         (c) Age distribution split by survival
#         (d) Fare distribution split by survival
#         (e) Survival rate by family size
#         (f) Survival rate by embarkation
#
#  5) No saved artifact for grading:
#     - Raw code ended with plt.show().
#     - Our evaluation requires a saved PNG artifact for metrics.
#     - Fix: save figure as 'llama_dashboard_rich_output.png' (dpi=300) and close.
#
# Notes on fairness / publishability:
# - We did NOT install missing packages to "help" the model; we removed unnecessary/hallucinated deps.
# - We limited fixes to executability (deps/path/schema/save) and to correcting panels that were not
#   satisfying the stated dashboard requirements (i.e., the raw code was not implementing the prompt).
# - All changes are documented here so the evaluation is auditable.
# =========================

import os
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset (manual fix: correct filename/path)
df = pd.read_csv('data/titanic.csv')

# Handle missing values (age is commonly missing)
if 'age' in df.columns:
    df['age'] = df['age'].fillna(df['age'].median())

# Derived feature: family size (sibsp + parch + self)
df['family_size'] = df['sibsp'] + df['parch'] + 1

# Create a 3x2 dashboard (allowed by prompt: 2x3 or 3x2; this is 3x2)
fig, axes = plt.subplots(3, 2, figsize=(14, 16))
fig.suptitle('Titanic Disaster: Comprehensive Survival Analysis', fontsize=18, fontweight='bold')

# -----------------------------
# Panel 1: Survival Rate by Class
# -----------------------------
survival_by_class = df.groupby('pclass')['survived'].mean().sort_index()
axes[0, 0].bar(survival_by_class.index.astype(str), survival_by_class.values)
axes[0, 0].set_title('Survival Rate by Class')
axes[0, 0].set_xlabel('Passenger Class')
axes[0, 0].set_ylabel('Survival Rate')
axes[0, 0].set_ylim(0, 1)

# -----------------------------
# Panel 2: Survival Rate by Gender
# -----------------------------
survival_by_sex = df.groupby('sex')['survived'].mean().reindex(['male', 'female'])
axes[0, 1].bar(survival_by_sex.index.astype(str), survival_by_sex.values)
axes[0, 1].set_title('Survival Rate by Gender')
axes[0, 1].set_xlabel('Gender')
axes[0, 1].set_ylabel('Survival Rate')
axes[0, 1].set_ylim(0, 1)

# -----------------------------
# Panel 3: Age Distribution by Survival (hist overlay)
# (SciPy Q-Q plot removed; replaced with standard distribution plot)
# -----------------------------
died_age = df[df['survived'] == 0]['age'].dropna()
surv_age = df[df['survived'] == 1]['age'].dropna()
axes[1, 0].hist(died_age, bins=20, alpha=0.6, edgecolor='black', label='Died')
axes[1, 0].hist(surv_age, bins=20, alpha=0.6, edgecolor='black', label='Survived')
axes[1, 0].set_title('Age Distribution by Survival')
axes[1, 0].set_xlabel('Age')
axes[1, 0].set_ylabel('Count')
axes[1, 0].legend()

# -----------------------------
# Panel 4: Fare Distribution by Survival (hist overlay, clipped for readability)
# -----------------------------
died_fare = df[df['survived'] == 0]['fare'].dropna()
surv_fare = df[df['survived'] == 1]['fare'].dropna()

# Clip extreme fares to improve readability without changing correctness too much
fare_clip = df['fare'].quantile(0.98) if 'fare' in df.columns else None
if fare_clip is not None:
    died_fare = died_fare[died_fare <= fare_clip]
    surv_fare = surv_fare[surv_fare <= fare_clip]

axes[1, 1].hist(died_fare, bins=20, alpha=0.6, edgecolor='black', label='Died')
axes[1, 1].hist(surv_fare, bins=20, alpha=0.6, edgecolor='black', label='Survived')
axes[1, 1].set_title('Fare Distribution by Survival')
axes[1, 1].set_xlabel('Fare')
axes[1, 1].set_ylabel('Count')
axes[1, 1].legend()

# -----------------------------
# Panel 5: Survival Rate by Family Size (bucket 7+)
# -----------------------------
tmp = df.copy()
tmp['family_bucket'] = tmp['family_size'].apply(lambda x: x if x <= 6 else 7)
survival_by_family = tmp.groupby('family_bucket')['survived'].mean().sort_index()
x_labels = [str(int(x)) if x < 7 else "7+" for x in survival_by_family.index]
axes[2, 0].bar(x_labels, survival_by_family.values)
axes[2, 0].set_title('Survival Rate by Family Size')
axes[2, 0].set_xlabel('Family Size')
axes[2, 0].set_ylabel('Survival Rate')
axes[2, 0].set_ylim(0, 1)

# -----------------------------
# Panel 6: Survival Rate by Embarkation
# -----------------------------
# Use embarked codes directly; fill missing as 'Unknown' to avoid dropping.
embark = df[['embarked', 'survived']].copy()
embark['embarked'] = embark['embarked'].fillna('Unknown')
survival_by_embarked = embark.groupby('embarked')['survived'].mean()

# Keep common order if present
order = [c for c in ['C', 'Q', 'S', 'Unknown'] if c in survival_by_embarked.index]
survival_by_embarked = survival_by_embarked.reindex(order)

axes[2, 1].bar(survival_by_embarked.index.astype(str), survival_by_embarked.values)
axes[2, 1].set_title('Survival Rate by Embarkation')
axes[2, 1].set_xlabel('Embarked')
axes[2, 1].set_ylabel('Survival Rate')
axes[2, 1].set_ylim(0, 1)

# Layout so plots do not overlap
plt.tight_layout(rect=[0, 0.03, 1, 0.94])

# Save artifact next to this script for consistent file management
out_path = os.path.join(os.path.dirname(__file__), "llama_dashboard_rich_output.png")
plt.savefig(out_path, dpi=300)
plt.close()
