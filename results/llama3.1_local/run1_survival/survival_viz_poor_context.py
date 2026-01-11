'''
The Titanic dataset contains passenger information from the RMS Titanic disaster of 1912.
Dataset is located at 'data/titanic.csv'.

Create a visualization showing survival rates across different passenger classes.

Provide ONLY the Python code wrapped in triple backticks.

'''
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
# FIX: Ensure path is correct
df = pd.read_csv('data/titanic.csv')

# FIX: Changed 'Pclass' -> 'pclass' and 'Survived' -> 'survived' (Schema Error Fix)
# Group by 'pclass' and calculate survival rates
survival_rates = df.groupby('pclass')['survived'].mean().reset_index()

# Create a bar chart to visualize the survival rates
plt.figure(figsize=(8,6))
plt.bar(survival_rates['pclass'], survival_rates['survived'])

plt.xlabel('Passenger Class')
plt.ylabel('Survival Rate')
plt.title('Survival Rates Across Different Passenger Classes')
plt.xticks([1, 2, 3], ['First Class', 'Second Class', 'Third Class'])

# FIX: Changed plt.show() to savefig so we can grade it
plt.savefig('llama_survival_bad.png')
print("Success: Generated llama_survival_bad.png")