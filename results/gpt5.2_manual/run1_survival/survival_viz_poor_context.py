'''
Without the Context-Rich prompt, the model struggled. 
It likely tried to guess the file location or column names and failed twice before finally getting it right. 

The model "hallucinated" the file path. 
It used /mnt/data/titanic.csv (which only exists in its own cloud computer), but our file is at data/titanic.csv.

Prompt = 
The Titanic dataset contains passenger information from the RMS Titanic disaster of 1912. 
This is a sociodemographic dataset with approximately 891 passenger records. 
Create a visualization showing survival rates across different passenger classes (1st, 2nd, 3rd). 
Provide ONLY the Python code wrapped in triple backticks.
'''

import pandas as pd
import matplotlib.pyplot as plt

# Load the Titanic dataset
# df = pd.read_csv('/mnt/data/titanic.csv')   # have to remove /mnt/
df = pd.read_csv('data/titanic.csv')

# Calculate survival rates by passenger class
survival_rates = df.groupby('pclass')['survived'].mean()

# Create the visualization
plt.figure()
survival_rates.plot(kind='bar')
plt.xlabel('Passenger Class')
plt.ylabel('Survival Rate')
plt.title('Survival Rates by Passenger Class on the Titanic')
# plt.show() 

plt.savefig('outputs/gpt5.2_manual/run2_context_poor.png')
