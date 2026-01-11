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
#   - Used df = pd.read_csv('titanic.csv') (file not present in repo root)
#   - Used plt.show() and did not save an image (grader requires an output .png)
#
# Minimal fixes (no visual/logic changes intended):
#   1) Input path portability:
#        pd.read_csv('titanic.csv')  ->  pd.read_csv('data/titanic.csv')
#   2) Output capture for evaluation:
#        plt.show()  ->  plt.savefig('output.png', dpi=300, bbox_inches='tight') + plt.close()
# =========================


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('data/titanic.csv')

# Create a bar plot showing survival rates by passenger class
plt.figure(figsize=(8, 6))
sns.barplot(x='pclass', y='survived', data=df, palette='viridis', hue='pclass', legend=False)

# Set chart title and labels
plt.title('Survival Rate by Passenger Class')
plt.xlabel('Passenger Class')
plt.ylabel('Survival Rate')
plt.ylim(0, 1)

# Display the plot
plt.tight_layout()
plt.savefig('output.png', dpi=300, bbox_inches='tight')
plt.close()
