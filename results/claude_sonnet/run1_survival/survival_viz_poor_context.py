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
#   - Used column names 'Pclass' and 'Survived' (repo data/titanic.csv has lowercase 'pclass', 'survived')
#   - Used plt.show() and did not save/close figure (grader requires output.png)
#
# Minimal fixes (no visual/logic changes intended):
#   1) Input path portability:
#        pd.read_csv('/mnt/user-data/uploads/titanic.csv')  ->  pd.read_csv('data/titanic.csv')
#   2) Column names to match repo CSV (KeyError: 'Pclass'):
#        groupby('Pclass')['Survived']  ->  groupby('pclass')['survived']
#   3) Output capture for evaluation:
#        plt.show()  ->  plt.savefig('output.png', dpi=300, bbox_inches='tight') + plt.close()
# =========================


import pandas as pd
import matplotlib.pyplot as plt

# Load the Titanic dataset
df = pd.read_csv('data/titanic.csv')

# Calculate survival rates by passenger class
survival_by_class = df.groupby('pclass')['survived'].agg(['sum', 'count'])
survival_by_class['survival_rate'] = (survival_by_class['sum'] / survival_by_class['count']) * 100

# Create visualization
plt.figure(figsize=(10, 6))
classes = ['1st Class', '2nd Class', '3rd Class']
plt.bar(classes, survival_by_class['survival_rate'], color=['gold', 'silver', '#CD7F32'], edgecolor='black', linewidth=1.5)
plt.xlabel('Passenger Class', fontsize=12, fontweight='bold')
plt.ylabel('Survival Rate (%)', fontsize=12, fontweight='bold')
plt.title('Titanic Survival Rates by Passenger Class', fontsize=14, fontweight='bold')
plt.ylim(0, 100)
for i, v in enumerate(survival_by_class['survival_rate']):
    plt.text(i, v + 2, f'{v:.1f}%', ha='center', fontsize=11, fontweight='bold')
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig('output.png', dpi=300, bbox_inches='tight')
plt.close()
