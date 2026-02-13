'''
Prompt (Rich Context):
You are an expert data scientist and visualization specialist.
Dataset: Titanic (data/titanic.csv); schema provided with lowercase columns (survived, pclass, sex, age, ...).
Technical: Load from data/titanic.csv, save as output.png (DPI 300), use matplotlib/seaborn/plotly.
Task: Create a visualization showing survival rates across passenger classes (1st, 2nd, 3rd);
  show counts and survival percentage, bar/grouped bar chart, title "Titanic Survival Rates by Passenger Class".
Provide ONLY the Python code wrapped in triple backticks.

'''

# =========================
# MANUAL FIXES APPLIED (DOCUMENTED)
# Code/execution:
#   - No path or output changes needed; code already used data/titanic.csv, output.png, plt.close().
# =========================


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11

# Load data
df = pd.read_csv('data/titanic.csv')

# Calculate survival statistics by passenger class
survival_stats = df.groupby(['pclass', 'survived']).size().unstack(fill_value=0)
survival_pct = df.groupby('pclass')['survived'].agg(['sum', 'count'])
survival_pct['percentage'] = (survival_pct['sum'] / survival_pct['count']) * 100

# Create figure
fig, ax = plt.subplots(figsize=(12, 7))

# Set positions for bars
x = np.arange(len(survival_stats.index))
width = 0.35

# Colorblind-friendly colors
color_died = '#d55e00'  # Orange-red for died
color_survived = '#009e73'  # Teal for survived

# Create grouped bars
bars1 = ax.bar(x - width/2, survival_stats[0], width, label='Did Not Survive', 
               color=color_died, edgecolor='black', linewidth=0.7)
bars2 = ax.bar(x + width/2, survival_stats[1], width, label='Survived', 
               color=color_survived, edgecolor='black', linewidth=0.7)

# Add count labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

# Add survival percentage labels above each class
for i, (idx, row) in enumerate(survival_pct.iterrows()):
    pct = row['percentage']
    total = row['count']
    # Position text above the tallest bar for each class
    max_height = max(survival_stats.loc[idx, 0], survival_stats.loc[idx, 1])
    ax.text(i, max_height + 15, f'{pct:.1f}% survived',
            ha='center', va='bottom', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                     edgecolor='gray', alpha=0.8))

# Customize plot
ax.set_xlabel('Passenger Class', fontsize=13, fontweight='bold')
ax.set_ylabel('Number of Passengers', fontsize=13, fontweight='bold')
ax.set_title('Titanic Survival Rates by Passenger Class', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(['1st Class', '2nd Class', '3rd Class'], fontsize=12)
ax.legend(fontsize=12, loc='upper right', framealpha=0.9)
ax.grid(axis='y', alpha=0.3)
ax.set_axisbelow(True)

# Add subtle background for each class
for i in range(len(x)):
    ax.axvspan(i - 0.4, i + 0.4, alpha=0.05, color='gray', zorder=0)

# Adjust layout
plt.tight_layout()

# Save figure
plt.savefig('output.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print("Visualization saved as 'output.png'")
print("\nSurvival Statistics by Class:")
print(survival_pct)