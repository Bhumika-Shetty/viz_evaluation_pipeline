"""
Prompt templates for AI visualization generation

Structure:
- BASE_PROMPT: Common dataset description
- 10+ TEST_PROMPTS: Different specific visualization tasks
"""

# ============================================================================
# BASE PROMPT - Common Dataset Description
# ============================================================================

TITANIC_BASE_PROMPT = """
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
"""

# ============================================================================
# TEST PROMPTS - 12 Different Visualization Tasks
# ============================================================================

TEST_PROMPTS = {
    "01_survival_by_class": {
        "name": "Survival Rate by Passenger Class",
        "task": """
Create a visualization showing survival rates across different passenger classes (1st, 2nd, 3rd).

**Specific Requirements:**
- Show both the count of survivors and survival percentage for each class
- Use a bar chart or grouped bar chart
- Include clear labeling showing the stark differences between classes
- Add a title: "Titanic Survival Rates by Passenger Class"
- Use distinct colors for survived vs. not survived

**Expected Insights:**
- 1st class passengers had the highest survival rate (~63%)
- 3rd class passengers had the lowest survival rate (~24%)
- Clear class-based disparity in survival
""",
        "expected_insights": [
            "first class highest survival",
            "third class lowest survival",
            "class disparity"
        ]
    },

    "02_gender_survival": {
        "name": "Gender-Based Survival Analysis",
        "task": """
Create a visualization comparing survival rates between male and female passengers.

**Specific Requirements:**
- Show survival counts and percentages for both genders
- Consider using a side-by-side bar chart or pie charts
- Highlight the dramatic gender difference
- Add a title: "Women and Children First: Survival by Gender"
- Use gender-appropriate or neutral colors

**Expected Insights:**
- Females had much higher survival rate (~74%) than males (~19%)
- "Women and children first" policy was clearly followed
- Gender was a major factor in survival
""",
        "expected_insights": [
            "female higher survival",
            "male lower survival",
            "women and children first"
        ]
    },

    "03_age_distribution": {
        "name": "Age Distribution and Survival",
        "task": """
Create a visualization showing the relationship between age and survival.

**Specific Requirements:**
- Use histograms, violin plots, or box plots
- Show age distributions separately for survivors and non-survivors
- Handle missing age values (either exclude or impute)
- Add a title: "Age Distribution: Survivors vs. Non-Survivors"
- Include median/mean age markers

**Expected Insights:**
- Children (age < 16) had higher survival rates
- Young adults (20-40) made up the largest group
- Age distribution differs between survivors and non-survivors
""",
        "expected_insights": [
            "children higher survival",
            "age distribution differs",
            "young adults largest group"
        ]
    },

    "04_fare_vs_survival": {
        "name": "Fare Price and Survival Correlation",
        "task": """
Create a visualization exploring the relationship between ticket fare and survival.

**Specific Requirements:**
- Use scatter plot, box plot, or violin plot
- Show fare distributions for survivors vs. non-survivors
- Handle extreme outliers appropriately
- Add a title: "Does Money Buy Survival? Fare vs. Survival Rate"
- Consider log scale if fare distribution is very skewed

**Expected Insights:**
- Higher fares correlate with higher survival rates
- First class (expensive) tickets had better survival
- Fare is a proxy for socioeconomic status
""",
        "expected_insights": [
            "higher fare higher survival",
            "fare correlates with class",
            "economic disparity"
        ]
    },

    "05_family_size": {
        "name": "Family Size Impact on Survival",
        "task": """
Create a visualization analyzing how family size (SibSp + Parch) affected survival.

**Specific Requirements:**
- Create a new feature: FamilySize = SibSp + Parch + 1 (including the person)
- Show survival rate by family size categories (alone, small family, large family)
- Use a line plot or bar chart
- Add a title: "Was Traveling Alone or With Family Safer?"
- Mark optimal family size for survival

**Expected Insights:**
- Passengers with small families (2-4 people) had better survival
- Solo travelers and very large families had lower survival
- Sweet spot exists around family size of 2-4
""",
        "expected_insights": [
            "small family better survival",
            "solo travelers lower survival",
            "optimal family size exists"
        ]
    },

    "06_embarkation_analysis": {
        "name": "Port of Embarkation and Survival",
        "task": """
Create a visualization comparing survival rates across different embarkation ports.

**Specific Requirements:**
- Show survival rates for Cherbourg (C), Queenstown (Q), and Southampton (S)
- Use a grouped bar chart or stacked bar chart
- Include both counts and percentages
- Add a title: "Survival Rates by Port of Embarkation"
- Use a map or icons to represent the ports

**Expected Insights:**
- Cherbourg had the highest survival rate (~55%)
- Southampton had the lowest survival rate (~34%)
- Embarkation port correlates with class (1st class mostly from Cherbourg)
""",
        "expected_insights": [
            "cherbourg highest survival",
            "southampton lowest survival",
            "port correlates with class"
        ]
    },

    "07_multi_factor_heatmap": {
        "name": "Multi-Factor Survival Heatmap",
        "task": """
Create a correlation heatmap showing relationships between all numerical features and survival.

**Specific Requirements:**
- Include: Survived, Pclass, Age, SibSp, Parch, Fare
- Use a heatmap with correlation coefficients
- Add annotations showing correlation values
- Add a title: "Feature Correlations with Survival"
- Use a diverging colormap (e.g., RdBu or coolwarm)

**Expected Insights:**
- Pclass has strong negative correlation with survival
- Fare has positive correlation with survival
- Age, SibSp, Parch have weaker correlations
""",
        "expected_insights": [
            "class strong correlation",
            "fare positive correlation",
            "age weaker correlation"
        ]
    },

    "08_comprehensive_dashboard": {
        "name": "Comprehensive Titanic Dashboard",
        "task": """
Create a multi-panel dashboard showing 4-6 different aspects of the Titanic data.

**Specific Requirements:**
- Use subplots to create a dashboard layout (2x3 or 3x2)
- Include: survival by class, by gender, age distribution, fare distribution, family size, embarkation
- Make it publication-ready with consistent styling
- Add a main title: "Titanic Disaster: Comprehensive Survival Analysis"
- Ensure all subplots are properly labeled

**Expected Insights:**
- Comprehensive view of all major factors affecting survival
- Visual story of the disaster
- Multiple patterns visible at once
""",
        "expected_insights": [
            "class gender age factors visible",
            "comprehensive overview",
            "multiple patterns"
        ]
    },

    "09_class_gender_interaction": {
        "name": "Class-Gender Interaction Effect",
        "task": """
Create a visualization showing the interaction between passenger class and gender on survival.

**Specific Requirements:**
- Show survival rates for all combinations (1st-Male, 1st-Female, 2nd-Male, etc.)
- Use a grouped bar chart or faceted plots
- Clearly show that class matters more for men than women
- Add a title: "Survival by Class and Gender: An Interaction Effect"
- Use different colors for gender and different patterns/positions for class

**Expected Insights:**
- Almost all 1st class females survived (~97%)
- 1st class males had better survival than 3rd class females
- Class × gender interaction exists
""",
        "expected_insights": [
            "first class females highest",
            "interaction effect exists",
            "class matters for males"
        ]
    },

    "10_survival_decision_tree": {
        "name": "Survival Decision Tree Visualization",
        "task": """
Create a visual representation of survival patterns that mimics a decision tree.

**Specific Requirements:**
- Show hierarchical decision patterns (e.g., Sex → Class → Age)
- Use a tree-like structure or nested charts
- Show survival rates at each decision node
- Add a title: "Survival Decision Patterns: Who Lived and Who Died?"
- Make it visually intuitive

**Expected Insights:**
- Primary split: Gender (Female = high survival)
- Secondary split: Class (for males especially)
- Tertiary split: Age (children priority)
""",
        "expected_insights": [
            "gender primary factor",
            "class secondary for males",
            "age matters for edge cases"
        ]
    },

    "11_missing_data_analysis": {
        "name": "Missing Data Pattern Analysis",
        "task": """
Create a visualization showing patterns in missing data across the dataset.

**Specific Requirements:**
- Show which features have missing values (Age, Cabin, Embarked)
- Visualize the percentage of missing data per feature
- Optionally show if missingness correlates with survival
- Add a title: "Missing Data Patterns in Titanic Dataset"
- Use a bar chart or heatmap

**Expected Insights:**
- Cabin has ~77% missing data
- Age has ~20% missing data
- Missing cabin data correlates with lower class
""",
        "expected_insights": [
            "cabin most missing",
            "age some missing",
            "missingness not random"
        ]
    },

    "12_fare_distribution_by_class": {
        "name": "Fare Distribution Across Classes",
        "task": """
Create a visualization showing how fares were distributed within each passenger class.

**Specific Requirements:**
- Use violin plots, box plots, or overlapping histograms
- Show all three classes side by side
- Handle outliers appropriately
- Add a title: "Ticket Fare Distribution by Passenger Class"
- Show median and quartiles

**Expected Insights:**
- Large overlap between 2nd and 3rd class fares
- 1st class has high variability in fares
- Clear price stratification by class
""",
        "expected_insights": [
            "first class high variability",
            "clear price stratification",
            "some overlap between classes"
        ]
    }
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_prompt(prompt_id: str) -> str:
    """
    Get a complete prompt by combining base prompt with specific task

    Args:
        prompt_id: ID of the test prompt (e.g., "01_survival_by_class")

    Returns:
        str: Complete formatted prompt
    """
    if prompt_id not in TEST_PROMPTS:
        raise ValueError(f"Unknown prompt ID: {prompt_id}. Available: {list(TEST_PROMPTS.keys())}")

    task_info = TEST_PROMPTS[prompt_id]

    full_prompt = f"""
You are an expert data scientist and visualization specialist.

{TITANIC_BASE_PROMPT}

## Your Task: {task_info['name']}

{task_info['task']}

## Output Format:
Provide ONLY the Python code wrapped in triple backticks. The code should:
1. Be fully executable
2. Create the visualization
3. Save it as 'output.png'
4. Print a brief summary of key findings

Example structure:
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
df = pd.read_csv('data/titanic.csv')

# Data preprocessing
# ... your code here ...

# Create visualization
# ... your visualization code here ...

# Save figure
plt.tight_layout()
plt.savefig('output.png', dpi=300, bbox_inches='tight')
plt.close()

# Print summary
print("Key Findings:")
print("1. ...")
print("2. ...")
```

Now, generate the Python code for this visualization:
"""

    return full_prompt


def get_all_prompt_ids() -> list:
    """Get list of all available prompt IDs"""
    return list(TEST_PROMPTS.keys())


def get_prompt_info(prompt_id: str) -> dict:
    """Get metadata about a specific prompt"""
    if prompt_id not in TEST_PROMPTS:
        raise ValueError(f"Unknown prompt ID: {prompt_id}")
    return TEST_PROMPTS[prompt_id]


def get_expected_insights(prompt_id: str) -> list:
    """Get expected insights for a specific prompt (for accuracy metric)"""
    if prompt_id not in TEST_PROMPTS:
        raise ValueError(f"Unknown prompt ID: {prompt_id}")
    return TEST_PROMPTS[prompt_id].get('expected_insights', [])


# Backwards compatibility
def get_titanic_prompt():
    """Returns the first test prompt for backwards compatibility"""
    return get_prompt("01_survival_by_class")


def get_dataset_prompt(dataset_name: str, dataset_info: dict = None):
    """
    Get prompt for a specific dataset

    Args:
        dataset_name: Name of the dataset
        dataset_info: Optional dictionary with dataset-specific information

    Returns:
        str: Formatted prompt for the dataset
    """
    if dataset_name.lower() == "titanic":
        return get_prompt("01_survival_by_class")
    else:
        return f"""
        Create a comprehensive data visualization for the {dataset_name} dataset.

        Your visualization should reveal the main patterns, correlations, and insights in the data.

        Provide executable Python code that:
        1. Loads the data from 'data/{dataset_name}.csv'
        2. Creates an insightful visualization
        3. Saves the result as 'output.png' with DPI=300

        Use matplotlib, seaborn, or plotly and follow best practices for data visualization.
        """


if __name__ == "__main__":
    # Display all available prompts
    print("="*70)
    print("AVAILABLE VISUALIZATION PROMPTS")
    print("="*70)
    print()

    for prompt_id in get_all_prompt_ids():
        info = get_prompt_info(prompt_id)
        print(f"{prompt_id}: {info['name']}")

    print()
    print(f"Total: {len(TEST_PROMPTS)} prompts available")
    print()
    print("="*70)
