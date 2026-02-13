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
# Model output issues:
#   - Model initially returned a visualization (image) instead of Python code, despite prompt explicitly
#     stating "Provide ONLY the Python code wrapped in triple backticks." User had to manually ask the
#     model to output the Python code.
#
# Code/execution:
#   - No path or output changes needed; code already used data/titanic.csv, output.png, plt.close().
# =========================


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# Load data
df = pd.read_csv('data/titanic.csv')

# Compute stats per class
classes = [1, 2, 3]
class_labels = ['1st Class', '2nd Class', '3rd Class']
survived_counts = []
died_counts = []
survival_rates = []

for c in classes:
    sub = df[df['pclass'] == c]
    s = sub['survived'].sum()
    d = len(sub) - s
    survived_counts.append(s)
    died_counts.append(d)
    survival_rates.append(s / len(sub) * 100)

# --- Plot ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1]})
fig.patch.set_facecolor('#FAFAFA')
for ax in (ax1, ax2):
    ax.set_facecolor('#FAFAFA')

x = np.arange(len(classes))
width = 0.38

# Colors: teal for survived, coral-red for not survived (colorblind-friendly)
c_surv = '#2a9d8f'
c_died = '#e76f51'

# Left panel: grouped bar chart (counts)
bars_d = ax1.bar(x - width/2, died_counts, width, label='Did Not Survive', color=c_died,
                 edgecolor='white', linewidth=0.8, zorder=3)
bars_s = ax1.bar(x + width/2, survived_counts, width, label='Survived', color=c_surv,
                 edgecolor='white', linewidth=0.8, zorder=3)

for bar in bars_d:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
             f'{int(bar.get_height())}', ha='center', va='bottom', fontsize=12, fontweight='bold', color=c_died)
for bar in bars_s:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
             f'{int(bar.get_height())}', ha='center', va='bottom', fontsize=12, fontweight='bold', color=c_surv)

ax1.set_xticks(x)
ax1.set_xticklabels(class_labels, fontsize=13)
ax1.set_ylabel('Number of Passengers', fontsize=13)
ax1.set_title('Passenger Counts', fontsize=14, fontweight='bold', pad=10)
ax1.legend(fontsize=11, frameon=True, fancybox=True, shadow=False, edgecolor='#cccccc')
ax1.set_ylim(0, max(died_counts) * 1.18)
ax1.grid(axis='y', alpha=0.3, linestyle='--', zorder=0)
ax1.spines[['top', 'right']].set_visible(False)

# Right panel: survival rate bar chart
bars_r = ax2.bar(x, survival_rates, width=0.55, color=[c_surv, '#3bb3a3', '#57c9b9'],
                 edgecolor='white', linewidth=0.8, zorder=3)

# Color gradient darker to lighter for emphasis
bar_colors = ['#1f7a6f', '#2a9d8f', '#5fbfb3']
for bar, col in zip(bars_r, bar_colors):
    bar.set_color(col)

for bar, rate in zip(bars_r, survival_rates):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
             f'{rate:.1f}%', ha='center', va='bottom', fontsize=14, fontweight='bold', color='#264653')

ax2.set_xticks(x)
ax2.set_xticklabels(class_labels, fontsize=13)
ax2.set_ylabel('Survival Rate (%)', fontsize=13)
ax2.set_title('Survival Rate', fontsize=14, fontweight='bold', pad=10)
ax2.set_ylim(0, 100)
ax2.yaxis.set_major_formatter(mticker.PercentFormatter())
ax2.grid(axis='y', alpha=0.3, linestyle='--', zorder=0)
ax2.spines[['top', 'right']].set_visible(False)

# Add a horizontal reference line at 50%
ax2.axhline(y=50, color='#999999', linestyle=':', linewidth=1, alpha=0.6, zorder=1)
ax2.text(2.35, 51, '50%', fontsize=9, color='#999999', va='bottom')

fig.suptitle('Titanic Survival Rates by Passenger Class', fontsize=17, fontweight='bold',
             color='#264653', y=0.98)
fig.text(0.5, 0.01, 'Higher-class passengers had significantly better survival outcomes — '
         '1st class survival was nearly 3× that of 3rd class.',
         ha='center', fontsize=11, color='#555555', style='italic')

plt.tight_layout(rect=[0, 0.04, 1, 0.93])
plt.savefig('output.png', dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()