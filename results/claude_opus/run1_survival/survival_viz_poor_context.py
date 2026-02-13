'''
Prompt : 
The Titanic dataset contains passenger information from the RMS Titanic disaster of 1912.
This is a sociodemographic dataset with approximately 891 passenger records.
Create a visualization showing survival rates across different passenger classes (1st, 2nd, 3rd).
Provide ONLY the Python code wrapped in triple backticks.

'''

# =========================
# MANUAL FIXES APPLIED (DOCUMENTED)
# Model output issues:
#   - Used df = pd.read_csv('/mnt/user-data/uploads/titanic.csv') (path not valid in repo)
#   - Saved to 'survival_by_class.png' (grader requires 'output.png')
#   - Used plt.show() and did not close figure (evaluation expects saved file only)
#   - Used column names 'Pclass' and 'Survived' (repo data/titanic.csv has lowercase 'pclass', 'survived')
#
# Minimal fixes (no visual/logic changes intended):
#   1) Input path portability:
#        pd.read_csv('/mnt/user-data/uploads/titanic.csv')  ->  pd.read_csv('data/titanic.csv')
#   2) Output capture for evaluation:
#        plt.savefig('survival_by_class.png', dpi=150)  ->  plt.savefig('output.png', dpi=300, bbox_inches='tight')
#   3) Removed plt.show(), added plt.close()
#   4) Column names to match repo CSV (KeyError: 'Pclass'):
#        groupby("Pclass")["Survived"]  ->  groupby("pclass")["survived"]
# =========================


import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/titanic.csv')

survival_rates = df.groupby("pclass")["survived"].mean() * 100

fig, ax = plt.subplots(figsize=(8, 5))
colors = ["#2ecc71", "#3498db", "#e74c3c"]
bars = ax.bar(
    [f"{c} Class" for c in ["1st", "2nd", "3rd"]],
    survival_rates.values,
    color=colors,
    edgecolor="white",
    width=0.6,
)

for bar, rate in zip(bars, survival_rates.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
            f"{rate:.1f}%", ha="center", va="bottom", fontsize=13, fontweight="bold")

ax.set_title("Titanic Survival Rate by Passenger Class", fontsize=15, fontweight="bold", pad=15)
ax.set_ylabel("Survival Rate (%)", fontsize=12)
ax.set_ylim(0, 80)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig('output.png', dpi=300, bbox_inches='tight')
plt.close()
