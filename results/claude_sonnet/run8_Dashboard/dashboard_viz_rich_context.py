'''
Prompt (Rich Context):
You are an expert data scientist and visualization specialist.
Dataset: Titanic (data/titanic.csv); schema provided with lowercase columns.
Technical: Load from data/titanic.csv, save as output.png (DPI 300), use matplotlib/seaborn/plotly.
Task: Create a multi-panel dashboard (2x3 or 3x2) showing 4-6 aspects: survival by class, gender,
  age distribution, fare distribution, family size, embarkation; title "Titanic Disaster: Comprehensive Survival Analysis".
Provide ONLY the Python code wrapped in triple backticks.

'''

# =========================
# MANUAL FIXES APPLIED (DOCUMENTED)
# Code/execution:
#   - No path or output filename changes needed; code already used data/titanic.csv, output.png.
#   - Added plt.close() after savefig for evaluation (script did not close figure).
# =========================


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Set style and color palette (colorblind-friendly)
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10

# Colorblind-friendly palette
colors = ['#0173B2', '#DE8F05', '#029E73', '#CC78BC', '#CA9161', '#949494']
survival_colors = ['#DE8F05', '#0173B2']  # Orange for died, blue for survived

# Load the data
df = pd.read_csv('data/titanic.csv')

# Create family size feature
df['family_size'] = df['sibsp'] + df['parch']

# Create the dashboard
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Titanic Disaster: Comprehensive Survival Analysis', 
             fontsize=20, fontweight='bold', y=0.995)

# 1. Survival by Class
ax1 = axes[0, 0]
survival_class = df.groupby(['pclass', 'survived']).size().unstack()
survival_class_pct = survival_class.div(survival_class.sum(axis=1), axis=0) * 100
survival_class_pct.plot(kind='bar', ax=ax1, color=survival_colors, width=0.7)
ax1.set_title('Survival Rate by Passenger Class', fontsize=14, fontweight='bold', pad=10)
ax1.set_xlabel('Passenger Class', fontsize=12)
ax1.set_ylabel('Percentage (%)', fontsize=12)
ax1.set_xticklabels(['1st Class', '2nd Class', '3rd Class'], rotation=0)
ax1.legend(['Died', 'Survived'], loc='upper right')
ax1.set_ylim(0, 100)
for container in ax1.containers:
    ax1.bar_label(container, fmt='%.1f%%', padding=3)

# 2. Survival by Gender
ax2 = axes[0, 1]
survival_sex = df.groupby(['sex', 'survived']).size().unstack()
survival_sex_pct = survival_sex.div(survival_sex.sum(axis=1), axis=0) * 100
survival_sex_pct.plot(kind='bar', ax=ax2, color=survival_colors, width=0.6)
ax2.set_title('Survival Rate by Gender', fontsize=14, fontweight='bold', pad=10)
ax2.set_xlabel('Gender', fontsize=12)
ax2.set_ylabel('Percentage (%)', fontsize=12)
ax2.set_xticklabels(['Female', 'Male'], rotation=0)
ax2.legend(['Died', 'Survived'], loc='upper right')
ax2.set_ylim(0, 100)
for container in ax2.containers:
    ax2.bar_label(container, fmt='%.1f%%', padding=3)

# 3. Age Distribution by Survival
ax3 = axes[0, 2]
df_age = df.dropna(subset=['age'])
sns.histplot(data=df_age, x='age', hue='survived', multiple='stack', 
             bins=20, ax=ax3, palette=survival_colors, alpha=0.8)
ax3.set_title('Age Distribution by Survival Status', fontsize=14, fontweight='bold', pad=10)
ax3.set_xlabel('Age (years)', fontsize=12)
ax3.set_ylabel('Count', fontsize=12)
ax3.legend(['Died', 'Survived'], title='Survived')

# 4. Fare Distribution by Survival
ax4 = axes[1, 0]
df_fare = df[df['fare'] < 300]  # Remove outliers for better visualization
sns.violinplot(data=df_fare, x='survived', y='fare', ax=ax4, 
               palette=survival_colors, inner='quartile')
ax4.set_title('Fare Distribution by Survival Status', fontsize=14, fontweight='bold', pad=10)
ax4.set_xlabel('Survival Status', fontsize=12)
ax4.set_ylabel('Fare (£)', fontsize=12)
ax4.set_xticklabels(['Died', 'Survived'])

# 5. Family Size and Survival
ax5 = axes[1, 1]
family_survival = df.groupby(['family_size', 'survived']).size().unstack(fill_value=0)
family_survival_pct = family_survival.div(family_survival.sum(axis=1), axis=0) * 100
family_survival_pct.plot(kind='bar', ax=ax5, color=survival_colors, width=0.7)
ax5.set_title('Survival Rate by Family Size', fontsize=14, fontweight='bold', pad=10)
ax5.set_xlabel('Family Size (Siblings/Spouse + Parents/Children)', fontsize=12)
ax5.set_ylabel('Percentage (%)', fontsize=12)
ax5.legend(['Died', 'Survived'], loc='upper right')
ax5.set_xticklabels(ax5.get_xticklabels(), rotation=0)
ax5.set_ylim(0, 100)

# 6. Embarkation Port and Survival
ax6 = axes[1, 2]
df_embarked = df.dropna(subset=['embarked'])
survival_embarked = df_embarked.groupby(['embarked', 'survived']).size().unstack()
survival_embarked_pct = survival_embarked.div(survival_embarked.sum(axis=1), axis=0) * 100
survival_embarked_pct.plot(kind='bar', ax=ax6, color=survival_colors, width=0.6)
ax6.set_title('Survival Rate by Embarkation Port', fontsize=14, fontweight='bold', pad=10)
ax6.set_xlabel('Port of Embarkation', fontsize=12)
ax6.set_ylabel('Percentage (%)', fontsize=12)
ax6.set_xticklabels(['Cherbourg', 'Queenstown', 'Southampton'], rotation=0)
ax6.legend(['Died', 'Survived'], loc='upper right')
ax6.set_ylim(0, 100)
for container in ax6.containers:
    ax6.bar_label(container, fmt='%.1f%%', padding=3)

# Adjust layout and save
plt.tight_layout()
plt.savefig('output.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("Dashboard saved as 'output.png'")

# Display summary statistics
print("\n=== TITANIC SURVIVAL SUMMARY ===")
print(f"Total Passengers: {len(df)}")
print(f"Overall Survival Rate: {df['survived'].mean()*100:.1f}%")
print(f"\nSurvival by Class:")
print(df.groupby('pclass')['survived'].apply(lambda x: f"{x.mean()*100:.1f}%"))
print(f"\nSurvival by Gender:")
print(df.groupby('sex')['survived'].apply(lambda x: f"{x.mean()*100:.1f}%"))
