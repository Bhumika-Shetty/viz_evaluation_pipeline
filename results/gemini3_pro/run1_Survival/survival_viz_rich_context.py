'''
Prompt : 
You are an expert data scientist and visualization specialist.

## Dataset Context:

The Titanic dataset contains passenger information from the RMS Titanic disaster of 1912.
This is a sociodemographic dataset with approximately 891 passenger records.

## Dataset Schema (IMPORTANT: All column names are lowercase):

- **survived**: Survival status (0 = No, 1 = Yes) - TARGET VARIABLE
- **pclass**: Passenger class (1 = 1st, 2 = 2nd, 3 = 3rd) - Socioeconomic proxy
- **sex**: Gender (male/female)
- **age**: Age in years (float, some missing values ~20%)
- **sibsp**: Number of siblings/spouses aboard (integer)
- **parch**: Number of parents/children aboard (integer)
- **fare**: Passenger fare (float)
- **embarked**: Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)
- **class**: Passenger class text (First, Second, Third)
- **who**: Person category (man, woman, child)
- **adult_male**: Boolean for adult male
- **deck**: Deck number (many missing values ~77%)
- **embark_town**: Full embarkation city name
- **alive**: Survival text (yes/no)
- **alone**: Boolean if passenger was alone

## Technical Requirements:

- Use Python with matplotlib, seaborn, or plotly
- Load data from 'data/titanic.csv'
- Handle missing values appropriately
- Save the final visualization as 'output.png' with high DPI (300)
- Include all necessary imports
- Make the code fully executable

## Design Principles:

- **Clarity**: Use clear, readable labels and titles
- **Color Accessibility**: Use colorblind-friendly palettes
- **Data Fidelity**: Accurately represent data without distortion
- **Interpretability**: Include legends, axis labels, and annotations

## Your Task: Survival Rate by Passenger Class

Create a visualization showing survival rates across different passenger classes (1st, 2nd, 3rd).

**Specific Requirements:**

- Show both the count of survivors and survival percentage for each class
- Use a bar chart or grouped bar 

'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
# Adjust the path if 'data/' subdirectory is not present in your local environment
try:
    df = pd.read_csv('data/titanic.csv')
except FileNotFoundError:
    df = pd.read_csv('titanic.csv')

# --- Data Preparation ---

# Map survival status to readable labels for the legend
df['Survival Status'] = df['survived'].map({0: 'Not Survived', 1: 'Survived'})

# Calculate counts for each class and survival status
survival_counts = df.groupby(['pclass', 'Survival Status']).size().reset_index(name='Count')

# Calculate total passengers per class to compute percentages
class_totals = df.groupby('pclass').size().reset_index(name='Total')

# Merge to get a complete dataset with totals
plot_data = pd.merge(survival_counts, class_totals, on='pclass')

# --- Visualization ---

# Set a clean visual style
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

# Use a colorblind-friendly palette
palette = sns.color_palette("viridis", n_colors=2)

# Create the grouped bar chart
ax = sns.barplot(
    data=plot_data,
    x='pclass',
    y='Count',
    hue='Survival Status',
    palette=palette
)

# --- Formatting & Annotations ---

# Set titles and labels
plt.title('Titanic Survival Rates by Passenger Class', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Passenger Class', fontsize=12)
plt.ylabel('Number of Passengers', fontsize=12)
plt.legend(title='Survival Status')

# Customize X-axis tick labels
ax.set_xticklabels(['1st Class', '2nd Class', '3rd Class'])

# Annotate bars with Count and Percentage
# We map the x-coordinate (0, 1, 2) to the passenger class (1, 2, 3) to retrieve totals
totals_map = df['pclass'].value_counts().sort_index().to_dict()

for p in ax.patches:
    height = p.get_height()
    if pd.isna(height) or height == 0:
        continue
        
    # Determine the class based on the bar's x-position
    # Seaborn places categorical bars at integer ticks (0, 1, 2, ...)
    center_x = p.get_x() + p.get_width() / 2
    class_idx = int(round(center_x))
    pclass = class_idx + 1  # 0 -> 1st Class, 1 -> 2nd Class, etc.
    
    # Calculate percentage
    total = totals_map.get(pclass, 1)
    percentage = (height / total) * 100
    
    # Create label text
    label = f"{int(height)}\n({percentage:.1f}%)"
    
    # Place annotation
    ax.annotate(
        label,
        (center_x, height),
        ha='center',
        va='bottom',
        fontsize=10,
        fontweight='medium',
        xytext=(0, 5),
        textcoords='offset points'
    )

# Save the output
plt.tight_layout()
plt.savefig('output.png', dpi=300)

# Display (optional, for interactive environments)
plt.show()
