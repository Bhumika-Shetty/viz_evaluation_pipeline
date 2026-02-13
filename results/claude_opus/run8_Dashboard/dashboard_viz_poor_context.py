'''
Prompt :
The Titanic dataset contains passenger information from the RMS Titanic disaster of 1912.
Create a multi-panel dashboard showing 4-6 different aspects of the Titanic data.
Provide ONLY the Python code wrapped in triple backticks.

'''

# =========================
# MANUAL FIXES APPLIED (DOCUMENTED)
# Model output issues:
#   - Model initially returned a visualization (image) instead of Python code, despite prompt explicitly
#     stating "Provide ONLY the Python code wrapped in triple backticks." User had to manually ask the
#     model to output the Python code.
#   - Used df = pd.read_csv('/mnt/user-data/uploads/titanic.csv') (path not valid in repo)
#   - Saved to 'titanic_dashboard.png' (grader requires 'output.png')
#   - Used plt.show() and did not close figure (evaluation expects saved file only)
#
# Minimal fixes (no visual/logic changes intended):
#   1) Input path portability:
#        pd.read_csv('/mnt/user-data/uploads/titanic.csv')  ->  pd.read_csv('data/titanic.csv')
#   2) Output capture for evaluation:
#        plt.savefig('titanic_dashboard.png', dpi=180, ...)  ->  plt.savefig('output.png', dpi=300, bbox_inches='tight', ...)
#   3) Removed plt.show(), added plt.close()
# =========================


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

# Load data
df = pd.read_csv('data/titanic.csv')

# Color palette
COLORS = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B', '#44BBA4']
BG_COLOR = '#F7F7F8'
TEXT_COLOR = '#2B2B2B'
GRID_COLOR = '#E0E0E0'

fig = plt.figure(figsize=(20, 14), facecolor=BG_COLOR)
fig.suptitle('RMS Titanic — Passenger Data Dashboard', fontsize=22, fontweight='bold',
             color=TEXT_COLOR, y=0.98)
fig.text(0.5, 0.955, '1,502 lives lost on April 15, 1912  ·  891 passengers in dataset',
         ha='center', fontsize=11, color='#777777', style='italic')

gs = gridspec.GridSpec(2, 3, hspace=0.35, wspace=0.30,
                       left=0.06, right=0.96, top=0.92, bottom=0.06)

# --- Helper ---
def style_ax(ax, title):
    ax.set_facecolor(BG_COLOR)
    ax.set_title(title, fontsize=13, fontweight='bold', color=TEXT_COLOR, pad=12)
    ax.tick_params(colors=TEXT_COLOR, labelsize=9)
    for spine in ax.spines.values():
        spine.set_color(GRID_COLOR)

# ── Panel 1: Survival Rate by Class ──
ax1 = fig.add_subplot(gs[0, 0])
survival_by_class = df.groupby('class')['survived'].mean() * 100
order = ['First', 'Second', 'Third']
vals = [survival_by_class[c] for c in order]
bars = ax1.bar(order, vals, color=COLORS[:3], edgecolor='white', linewidth=1.2, width=0.6)
for bar, v in zip(bars, vals):
    ax1.text(bar.get_x() + bar.get_width()/2, v + 1.5, f'{v:.1f}%',
             ha='center', fontsize=11, fontweight='bold', color=TEXT_COLOR)
ax1.set_ylim(0, 80)
ax1.set_ylabel('Survival Rate (%)', fontsize=10)
style_ax(ax1, 'Survival Rate by Passenger Class')

# ── Panel 2: Age Distribution by Survival ──
ax2 = fig.add_subplot(gs[0, 1])
age_survived = df[df['survived'] == 1]['age'].dropna()
age_died = df[df['survived'] == 0]['age'].dropna()
bins = np.arange(0, 85, 5)
ax2.hist(age_died, bins=bins, alpha=0.7, color=COLORS[3], label='Did not survive', edgecolor='white')
ax2.hist(age_survived, bins=bins, alpha=0.7, color=COLORS[5], label='Survived', edgecolor='white')
ax2.legend(fontsize=9, framealpha=0.9)
ax2.set_xlabel('Age', fontsize=10)
ax2.set_ylabel('Count', fontsize=10)
style_ax(ax2, 'Age Distribution by Survival')

# ── Panel 3: Gender & Survival ──
ax3 = fig.add_subplot(gs[0, 2])
gender_surv = df.groupby(['sex', 'survived']).size().unstack(fill_value=0)
gender_surv.columns = ['Died', 'Survived']
gender_surv = gender_surv.loc[['female', 'male']]
gender_surv.plot(kind='barh', stacked=True, ax=ax3, color=[COLORS[3], COLORS[5]],
                 edgecolor='white', linewidth=1.2)
ax3.set_xlabel('Number of Passengers', fontsize=10)
ax3.set_yticklabels(['Female', 'Male'], fontsize=11)
ax3.legend(fontsize=9, loc='lower right', framealpha=0.9)
for i, (idx, row) in enumerate(gender_surv.iterrows()):
    total = row.sum()
    surv_pct = row['Survived'] / total * 100
    ax3.text(total + 5, i, f'{surv_pct:.0f}% survived', va='center', fontsize=10, color=TEXT_COLOR)
style_ax(ax3, 'Survival by Gender')

# ── Panel 4: Fare Distribution by Class (box plot) ──
ax4 = fig.add_subplot(gs[1, 0])
fare_data = [df[df['class'] == c]['fare'].dropna().values for c in order]
bp = ax4.boxplot(fare_data, tick_labels=order, patch_artist=True, showfliers=False,
                 medianprops=dict(color=TEXT_COLOR, linewidth=2))
for patch, color in zip(bp['boxes'], COLORS[:3]):
    patch.set_facecolor(color)
    patch.set_alpha(0.75)
ax4.set_ylabel('Fare (£)', fontsize=10)
style_ax(ax4, 'Fare Distribution by Class')

# ── Panel 5: Embarkation Port ──
ax5 = fig.add_subplot(gs[1, 1])
port_counts = df['embark_town'].value_counts()
wedges, texts, autotexts = ax5.pie(
    port_counts, labels=port_counts.index, autopct='%1.1f%%',
    colors=[COLORS[0], COLORS[1], COLORS[2]], startangle=140,
    textprops={'fontsize': 10, 'color': TEXT_COLOR},
    wedgeprops={'edgecolor': 'white', 'linewidth': 2})
for t in autotexts:
    t.set_fontsize(10)
    t.set_fontweight('bold')
style_ax(ax5, 'Embarkation Port Distribution')

# ── Panel 6: Family Size vs Survival ──
ax6 = fig.add_subplot(gs[1, 2])
df['family_size'] = df['sibsp'] + df['parch']
fam_surv = df.groupby('family_size')['survived'].agg(['mean', 'count'])
fam_surv = fam_surv[fam_surv['count'] >= 5]  # filter small groups
ax6.bar(fam_surv.index, fam_surv['mean'] * 100, color=COLORS[0],
        edgecolor='white', linewidth=1.2, width=0.7)
for x, y, n in zip(fam_surv.index, fam_surv['mean'] * 100, fam_surv['count']):
    ax6.text(x, y + 1.5, f'n={n}', ha='center', fontsize=8, color='#777')
ax6.set_xlabel('Family Size (siblings/spouse + parents/children)', fontsize=10)
ax6.set_ylabel('Survival Rate (%)', fontsize=10)
ax6.set_xticks(fam_surv.index)
style_ax(ax6, 'Family Size vs Survival Rate')

plt.savefig('output.png', dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
plt.close()