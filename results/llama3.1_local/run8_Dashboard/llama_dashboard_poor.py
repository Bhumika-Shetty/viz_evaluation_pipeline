'''
Prompt (parity, verbatim):
The Titanic dataset contains passenger information from the RMS Titanic disaster of 1912.
This is a sociodemographic dataset with approximately 891 passenger records.
Create a comprehensive dashboard visualization showing multiple different insights about survival patterns in the data.
Provide ONLY the Python code wrapped in triple backticks.
'''

# =========================
# MANUAL FIXES APPLIED (DOCUMENTED) — FAIR / MINIMAL EXECUTABILITY FIXES
#
# Why fixes were needed:
# The raw Llama (bad-context) dashboard code was NOT directly runnable / gradable in our local repo:
#  1) Dependency hallucination:
#     - Raw code imported scikit-learn (LabelEncoder, train_test_split, RandomForestClassifier, etc.)
#     - Our visualization pipeline does not require ML training, and sklearn wasn't installed -> crash.
#     - Fix: removed ALL sklearn imports + ALL ML training/evaluation code.
#
#  2) Dataset path assumption:
#     - Raw code attempted to read 'titanic.csv' from repo root.
#     - Our dataset lives at 'data/titanic.csv'.
#     - Fix: pd.read_csv('titanic.csv') -> pd.read_csv('data/titanic.csv')
#
#  3) Schema mismatch (case):
#     - Raw code referenced columns like 'Survived', 'Sex', 'Age', 'Fare', 'Embarked', 'Pclass'
#     - Our dataset columns are lowercase: 'survived', 'sex', 'age', 'fare', 'embarked', 'pclass'
#     - Fix: updated column references to lowercase equivalents.
#
#  4) Plot content depended on ML outputs:
#     - Raw code plotted a "Survival vs Age" scatter using y_pred from a trained model.
#     - This is not part of the dashboard task and also required sklearn.
#     - Fix: replaced that panel with a standard, dataset-derived plot:
#         "Survival Rate by Family Size" (family_size = sibsp + parch + 1)
#
#  5) No saved artifact for grading:
#     - Raw code used plt.show() only.
#     - Our evaluation requires a saved PNG artifact for metrics.
#     - Fix: save figure as 'llama_dashboard_poor_output.png' (dpi=300) and close.
#
# Notes on fairness:
# - We did NOT "beautify" or redesign beyond what was necessary to:
#     (a) remove hallucinated deps,
#     (b) bind to correct dataset schema/path,
#     (c) ensure an image artifact is produced for grading.
# - The dashboard structure remains a 2x3 multi-panel view of survival patterns.
# =========================

import os
import pandas as pd
import matplotlib.pyplot as plt

# Load the Titanic dataset (manual fix: correct repo path)
df = pd.read_csv('data/titanic.csv')

# Minimal preprocessing (manual fix: missing values handling)
# Age has missing values in Titanic; fill with median for stable plots.
if 'age' in df.columns:
    df['age'] = df['age'].fillna(df['age'].median())

# Add a simple derived feature for the dashboard (family size)
# family_size = siblings/spouses + parents/children + self
df['family_size'] = df['sibsp'] + df['parch'] + 1

# --- Create dashboard figure ---
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle("Titanic Passenger Survival Dashboard", fontsize=18, fontweight='bold')

# -----------------------------
# Panel 1: Survival Rate by Class
# -----------------------------
survival_by_class = df.groupby('pclass')['survived'].mean().sort_index()
axes[0, 0].bar(survival_by_class.index.astype(str), survival_by_class.values)
axes[0, 0].set_title("Survival Rate by Passenger Class")
axes[0, 0].set_xlabel("Passenger Class")
axes[0, 0].set_ylabel("Survival Rate")
axes[0, 0].set_ylim(0, 1)

# -----------------------------
# Panel 2: Survival Rate by Gender
# -----------------------------
survival_by_sex = df.groupby('sex')['survived'].mean().reindex(['male', 'female'])
axes[0, 1].bar(survival_by_sex.index.astype(str), survival_by_sex.values)
axes[0, 1].set_title("Survival Rate by Gender")
axes[0, 1].set_xlabel("Gender")
axes[0, 1].set_ylabel("Survival Rate")
axes[0, 1].set_ylim(0, 1)

# -----------------------------
# Panel 3: Age Distribution by Survival
# -----------------------------
survived_age = df[df['survived'] == 1]['age'].dropna()
died_age = df[df['survived'] == 0]['age'].dropna()
axes[0, 2].hist(died_age, bins=20, alpha=0.6, edgecolor='black', label='Died')
axes[0, 2].hist(survived_age, bins=20, alpha=0.6, edgecolor='black', label='Survived')
axes[0, 2].set_title("Age Distribution by Survival")
axes[0, 2].set_xlabel("Age")
axes[0, 2].set_ylabel("Count")
axes[0, 2].legend()

# -----------------------------
# Panel 4: Fare Distribution by Survival
# -----------------------------
survived_fare = df[df['survived'] == 1]['fare'].dropna()
died_fare = df[df['survived'] == 0]['fare'].dropna()
axes[1, 0].hist(died_fare, bins=20, alpha=0.6, edgecolor='black', label='Died')
axes[1, 0].hist(survived_fare, bins=20, alpha=0.6, edgecolor='black', label='Survived')
axes[1, 0].set_title("Fare Distribution by Survival")
axes[1, 0].set_xlabel("Fare")
axes[1, 0].set_ylabel("Count")
axes[1, 0].legend()

# -----------------------------
# Panel 5: Embarkation Distribution (Counts)
# -----------------------------
# Use embarked codes (C/Q/S). Fill missing as 'Unknown' to avoid dropping records.
embarked_counts = df['embarked'].fillna('Unknown').value_counts()
# Sort to keep common ordering if present
order = [c for c in ['C', 'Q', 'S', 'Unknown'] if c in embarked_counts.index]
embarked_counts = embarked_counts.reindex(order)
axes[1, 1].bar(embarked_counts.index.astype(str), embarked_counts.values)
axes[1, 1].set_title("Embarkation Port Distribution")
axes[1, 1].set_xlabel("Embarked")
axes[1, 1].set_ylabel("Count")

# -----------------------------
# Panel 6: Survival Rate by Family Size
# -----------------------------
# To keep the plot readable, limit to common family sizes (1–6) and group the rest as "7+"
tmp = df.copy()
tmp['family_size_bucket'] = tmp['family_size'].apply(lambda x: x if x <= 6 else 7)
survival_by_family = tmp.groupby('family_size_bucket')['survived'].mean().sort_index()
x_labels = [str(int(x)) if x < 7 else "7+" for x in survival_by_family.index]
axes[1, 2].bar(x_labels, survival_by_family.values)
axes[1, 2].set_title("Survival Rate by Family Size")
axes[1, 2].set_xlabel("Family Size")
axes[1, 2].set_ylabel("Survival Rate")
axes[1, 2].set_ylim(0, 1)

# Layout + save artifact for grading (manual fix: replace plt.show)
plt.tight_layout(rect=[0, 0.03, 1, 0.93])

# Save next to this script to avoid path confusion when running from repo root
out_path = os.path.join(os.path.dirname(__file__), "llama_dashboard_poor_output.png")
plt.savefig(out_path, dpi=300)
plt.close()
