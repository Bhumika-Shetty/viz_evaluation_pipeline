'''
Prompt :
The Titanic dataset contains passenger information from the RMS Titanic disaster of 1912.
Create a multi-panel dashboard showing 4-6 different aspects of the Titanic data.
Provide ONLY the Python code wrapped in triple backticks.

'''

# =========================
# MANUAL FIXES APPLIED (DOCUMENTED)
# Model output issues:
#   - Used df = pd.read_csv('/mnt/user-data/uploads/titanic.csv') (path not valid in repo)
#   - Saved to '/mnt/user-data/outputs/titanic_dashboard.png' (path not valid; grader requires 'output.png')
#   - Used plt.show() and did not close figure (evaluation expects saved file only)
#
# Minimal fixes (no visual/logic changes intended):
#   1) Input path portability:
#        pd.read_csv('/mnt/user-data/uploads/titanic.csv')  ->  pd.read_csv('data/titanic.csv')
#   2) Output capture for evaluation:
#        plt.savefig('/mnt/user-data/outputs/titanic_dashboard.png', ...)  ->  plt.savefig('output.png', dpi=300, bbox_inches='tight')
#   3) Removed plt.show(), added plt.close()
# =========================


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
df = pd.read_csv('data/titanic.csv')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (18, 12)

# Create subplots
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Titanic Dataset Dashboard', fontsize=20, fontweight='bold', y=0.995)

# 1. Survival Rate by Passenger Class
survival_by_class = df.groupby('pclass')['survived'].agg(['sum', 'count'])
survival_by_class['rate'] = survival_by_class['sum'] / survival_by_class['count'] * 100
ax1 = axes[0, 0]
bars = ax1.bar(['1st Class', '2nd Class', '3rd Class'], survival_by_class['rate'], 
               color=['#2ecc71', '#3498db', '#e74c3c'], alpha=0.7, edgecolor='black')
ax1.set_ylabel('Survival Rate (%)', fontsize=11, fontweight='bold')
ax1.set_title('Survival Rate by Passenger Class', fontsize=13, fontweight='bold', pad=10)
ax1.set_ylim(0, 100)
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')

# 2. Age Distribution by Survival Status
ax2 = axes[0, 1]
survived_ages = df[df['survived'] == 1]['age'].dropna()
died_ages = df[df['survived'] == 0]['age'].dropna()
ax2.hist([died_ages, survived_ages], bins=20, label=['Died', 'Survived'], 
         color=['#e74c3c', '#2ecc71'], alpha=0.7, edgecolor='black')
ax2.set_xlabel('Age', fontsize=11, fontweight='bold')
ax2.set_ylabel('Frequency', fontsize=11, fontweight='bold')
ax2.set_title('Age Distribution by Survival Status', fontsize=13, fontweight='bold', pad=10)
ax2.legend(frameon=True, fancybox=True, shadow=True)

# 3. Survival Rate by Sex
ax3 = axes[0, 2]
survival_by_sex = df.groupby('sex')['survived'].agg(['sum', 'count'])
survival_by_sex['rate'] = survival_by_sex['sum'] / survival_by_sex['count'] * 100
colors = ['#3498db', '#e91e63']
bars = ax3.bar(survival_by_sex.index, survival_by_sex['rate'], 
               color=colors, alpha=0.7, edgecolor='black')
ax3.set_ylabel('Survival Rate (%)', fontsize=11, fontweight='bold')
ax3.set_title('Survival Rate by Sex', fontsize=13, fontweight='bold', pad=10)
ax3.set_ylim(0, 100)
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')

# 4. Fare Distribution by Class
ax4 = axes[1, 0]
fare_by_class = [df[df['pclass'] == i]['fare'].dropna() for i in [1, 2, 3]]
bp = ax4.boxplot(fare_by_class, labels=['1st Class', '2nd Class', '3rd Class'],
                  patch_artist=True, showmeans=True)
colors = ['#2ecc71', '#3498db', '#e74c3c']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax4.set_ylabel('Fare ($)', fontsize=11, fontweight='bold')
ax4.set_title('Fare Distribution by Passenger Class', fontsize=13, fontweight='bold', pad=10)
ax4.grid(True, alpha=0.3)

# 5. Embarkation Port Distribution
ax5 = axes[1, 1]
embark_counts = df['embark_town'].value_counts()
colors_pie = ['#3498db', '#e74c3c', '#f39c12']
wedges, texts, autotexts = ax5.pie(embark_counts, labels=embark_counts.index, 
                                     autopct='%1.1f%%', startangle=90,
                                     colors=colors_pie, explode=(0.05, 0.05, 0.05))
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(10)
for text in texts:
    text.set_fontsize(11)
    text.set_fontweight('bold')
ax5.set_title('Passenger Distribution by Embarkation Port', fontsize=13, fontweight='bold', pad=10)

# 6. Family Size vs Survival
ax6 = axes[1, 2]
df['family_size'] = df['sibsp'] + df['parch']
family_survival = df.groupby('family_size')['survived'].agg(['sum', 'count'])
family_survival['rate'] = family_survival['sum'] / family_survival['count'] * 100
ax6.plot(family_survival.index, family_survival['rate'], marker='o', 
         linewidth=2.5, markersize=8, color='#9b59b6')
ax6.fill_between(family_survival.index, family_survival['rate'], alpha=0.3, color='#9b59b6')
ax6.set_xlabel('Family Size (Siblings/Spouse + Parents/Children)', fontsize=11, fontweight='bold')
ax6.set_ylabel('Survival Rate (%)', fontsize=11, fontweight='bold')
ax6.set_title('Survival Rate by Family Size', fontsize=13, fontweight='bold', pad=10)
ax6.grid(True, alpha=0.3)
ax6.set_ylim(0, 100)

plt.tight_layout()
plt.savefig('output.png', dpi=300, bbox_inches='tight')
plt.close()

print("Dashboard created successfully!")
print(f"\nDataset Summary:")
print(f"Total passengers: {len(df)}")
print(f"Survivors: {df['survived'].sum()} ({df['survived'].mean()*100:.1f}%)")
print(f"Non-survivors: {len(df) - df['survived'].sum()} ({(1-df['survived'].mean())*100:.1f}%)")
