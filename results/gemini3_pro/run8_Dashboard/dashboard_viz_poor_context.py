''' 
Prompt : 

The Titanic dataset contains passenger information from the RMS Titanic disaster of 1912.
This is a sociodemographic dataset with approximately 891 passenger records.

Create a comprehensive dashboard visualization showing multiple different insights about survival patterns in the data.
'''
# =========================
# MANUAL FIXES APPLIED (DOCUMENTED)
# Reason: model assumed 'titanic.csv' in repo root; our dataset is in 'data/titanic.csv'
# Fix: pd.read_csv('titanic.csv') -> pd.read_csv('data/titanic.csv')
# =========================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
# df = pd.read_csv('titanic.csv')  # change
df = pd.read_csv('data/titanic.csv')

# Preprocessing: Map survival values for clear labels and calculate family size
df['Survival_Status'] = df['survived'].map({0: 'Died', 1: 'Survived'})
df['Family_Size'] = df['sibsp'] + df['parch'] + 1

# Set the visual style
sns.set(style="whitegrid", palette="muted")

# Initialize the dashboard figure
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Titanic Passenger Survival Dashboard', fontsize=24, weight='bold')

# 1. Overall Survival Rate (Pie Chart)
status_counts = df['Survival_Status'].value_counts()
axes[0, 0].pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', 
               startangle=90, colors=['#ff9999','#66b3ff'], explode=(0.05, 0))
axes[0, 0].set_title('Overall Survival Rate', fontsize=16)

# 2. Survival Rate by Gender (Bar Plot)
sns.barplot(x='sex', y='survived', data=df, ax=axes[0, 1], palette='pastel')
axes[0, 1].set_title('Survival Rate by Gender', fontsize=16)
axes[0, 1].set_ylim(0, 1)
axes[0, 1].set_ylabel('Survival Probability')

# 3. Survival Rate by Class (Bar Plot)
sns.barplot(x='pclass', y='survived', data=df, ax=axes[0, 2], palette='viridis')
axes[0, 2].set_title('Survival Rate by Class', fontsize=16)
axes[0, 2].set_ylim(0, 1)
axes[0, 2].set_ylabel('Survival Probability')

# 4. Age Distribution by Survival (Histogram/KDE)
sns.histplot(data=df, x='age', hue='Survival_Status', kde=True, element="step", 
             stat="density", common_norm=False, ax=axes[1, 0], palette='husl')
axes[1, 0].set_title('Age Distribution by Survival', fontsize=16)

# 5. Survival Rate by Family Size (Bar Plot)
sns.barplot(x='Family_Size', y='survived', data=df, ax=axes[1, 1], palette='magma')
axes[1, 1].set_title('Survival Rate by Family Size', fontsize=16)
axes[1, 1].set_ylabel('Survival Probability')

# 6. Fare Distribution by Class (Box Plot)
sns.boxplot(x='pclass', y='fare', hue='Survival_Status', data=df, ax=axes[1, 2], palette='coolwarm', showfliers=False)
axes[1, 2].set_title('Fare Distribution by Class & Survival (No Outliers)', fontsize=16)

# Final Layout Adjustments
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Save the dashboard
plt.savefig('titanic_dashboard.png')
# plt.show()