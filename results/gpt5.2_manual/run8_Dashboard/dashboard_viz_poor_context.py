'''
Without the Context-Rich prompt, the model struggled. 

Prompt = 
The Titanic dataset contains passenger information from the RMS Titanic disaster of 1912. 
This is a sociodemographic dataset with approximately 891 passenger records. 
Create a comprehensive dashboard visualization showing multiple different insights about survival patterns in the data. 
Provide ONLY the Python code wrapped in triple backticks.
'''

'''
Failure 1 (Hallucination): FileNotFoundError: '/mnt/data/titanic.csv'

What it proves: Without context, the model defaults to its internal training environment paths instead of your actual project structure.

Failure 2 (Schema Error): KeyError: 'sex'

What it proves: The model "hallucinated" that the column name was Sex (Capitalized). 
In our specific dataset, it is sex (lowercase). Because I didn't give it the schema in the prompt, it guessed wrong and crashed.

Now we need to manually fix the code to force it to generate the graph. 
We want to see how bad the dashboard looks after we fix the bugs.

Fix the Path: Change /mnt/data/titanic.csv → 'data/titanic.csv'

Fix the Columns using "Find & Replace"): The model capitalized everything. We need to change them to lowercase.

df['sex'] → df['sex']

df['survived'] → df['survived']

df['pclass'] → df['pclass']

df['age'] → df['age']

df['fare'] → df['fare']

df['embarked'] → df['embarked']

Failure #3 : 
The model tried to be "smart" by using df.get("Sibsp", 0) (which means "if you can't find Sibsp, just give me 0"). 
But because it couldn't find "Sibsp" (capitalized), it returned the integer 0. 
Then it tried to run .fillna() on a single number, which crashed Python.

We need to fix the capitalization for the Family Size columns too.

'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv("data/titanic.csv")

# Normalize common Titanic column name variants
col_map = {
    "PassengerId": "PassengerId",
    "survived": "survived",
    "pclass": "pclass",
    "Name": "Name",
    "sex": "sex",
    "age": "age",
    "sibsp": "sibsp",
    "parch": "parch",
    "Ticket": "Ticket",
    "fare": "fare",
    "Cabin": "Cabin",
    "embarked": "embarked",
}
# keep only known columns if extra exist
for k in list(col_map.keys()):
    if k not in df.columns:
        col_map.pop(k, None)

# Basic derived fields
df["sex"] = df["sex"].astype(str).str.lower().str.strip()
df["embarked"] = df.get("embarked", pd.Series([np.nan] * len(df))).astype(str).replace("nan", np.nan)
df["pclass"] = pd.to_numeric(df["pclass"], errors="coerce")
df["survived"] = pd.to_numeric(df["survived"], errors="coerce")

df["FamilySize"] = (
    pd.to_numeric(df.get("sibsp", 0), errors="coerce").fillna(0).astype(int)
    + pd.to_numeric(df.get("parch", 0), errors="coerce").fillna(0).astype(int)
    + 1
)

df["IsAlone"] = (df["FamilySize"] == 1).astype(int)

# age bins (keep NaN as separate category later)
age_bins = [-0.1, 12, 18, 30, 45, 60, 80, 120]
age_labels = ["Child (0-12)", "Teen (13-18)", "Young (19-30)", "Adult (31-45)", "Mid (46-60)", "Senior (61-80)", "80+"]

df["ageBin"] = pd.cut(df["age"], bins=age_bins, labels=age_labels)

# fare bins by quartile (with NaN handling)
fare = pd.to_numeric(df.get("fare", np.nan), errors="coerce")
if fare.notna().sum() > 0:
    df["fareBin"] = pd.qcut(fare, q=4, labels=["Low", "Mid-Low", "Mid-High", "High"], duplicates="drop")
else:
    df["fareBin"] = np.nan

# Helper for survival rate
def survival_rate(group: pd.Series) -> float:
    s = pd.to_numeric(group, errors="coerce").dropna()
    return float(s.mean()) if len(s) else np.nan

# -----------------------------
# Aggregations
# -----------------------------
# Survival by sex
sex_surv = df.groupby("sex")["survived"].mean().sort_index()

# Survival by Class
class_surv = df.groupby("pclass")["survived"].mean().sort_index()

# Survival by embarked
emb_surv = df.groupby("embarked")["survived"].mean().sort_index()

# Survival by ageBin (include Missing)
age_surv = (
    df.assign(ageBinFilled=df["ageBin"].astype(object).where(df["ageBin"].notna(), "Missing"))
      .groupby("ageBinFilled")["survived"].mean()
)
# preserve a nice order
age_order = age_labels + ["Missing"]
age_surv = age_surv.reindex([x for x in age_order if x in age_surv.index])

# Survival by fareBin (include Missing)
fare_surv = (
    df.assign(fareBinFilled=df["fareBin"].astype(object).where(df["fareBin"].notna(), "Missing"))
      .groupby("fareBinFilled")["survived"].mean()
)
fare_order = ["Low", "Mid-Low", "Mid-High", "High", "Missing"]
fare_surv = fare_surv.reindex([x for x in fare_order if x in fare_surv.index])

# Heatmap-like matrix: survival rate by sex x pclass
pivot = df.pivot_table(index="sex", columns="pclass", values="survived", aggfunc="mean")

# Count by class & survival (for stacked bars)
counts = (
    df.groupby(["pclass", "survived"])
      .size()
      .unstack(fill_value=0)
      .rename(columns={0: "Died", 1: "survived"})
      .sort_index()
)

# Family size survival curve
fam_surv = df.groupby("FamilySize")["survived"].mean().sort_index()
fam_cnt = df.groupby("FamilySize").size().sort_index()

# KPI-like summary
n_total = len(df)
n_surv = int(df["survived"].sum(skipna=True)) if df["survived"].notna().any() else 0
overall_rate = df["survived"].mean(skipna=True)
median_age = pd.to_numeric(df["age"], errors="coerce").median()
median_fare = pd.to_numeric(df["fare"], errors="coerce").median()

# -----------------------------
# Dashboard Figure
# -----------------------------
plt.close("all")
fig = plt.figure(figsize=(18, 11), constrained_layout=True)
gs = gridspec.GridSpec(3, 4, figure=fig, height_ratios=[1.0, 1.15, 1.15])

# Title
fig.suptitle("Titanic Survival Dashboard (RMS Titanic, 1912) — Survival Patterns & Socio-demographics", fontsize=16, y=1.02)

# (0,0) KPI Box / Summary table
ax0 = fig.add_subplot(gs[0, 0])
ax0.axis("off")
kpi_rows = [
    ["Passengers", f"{n_total:,}"],
    ["Survivors", f"{n_surv:,}"],
    ["Overall Survival Rate", f"{overall_rate:.1%}" if pd.notna(overall_rate) else "N/A"],
    ["Median age", f"{median_age:.1f}" if pd.notna(median_age) else "N/A"],
    ["Median fare", f"{median_fare:.2f}" if pd.notna(median_fare) else "N/A"],
]
tbl = ax0.table(cellText=kpi_rows, colLabels=["Metric", "Value"], cellLoc="left", loc="center")
tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1, 1.4)
ax0.set_title("Key Stats", fontsize=12, pad=8)

# (0,1) Survival rate by sex
ax1 = fig.add_subplot(gs[0, 1])
ax1.bar(sex_surv.index.astype(str), sex_surv.values)
ax1.set_ylim(0, 1)
ax1.set_title("Survival Rate by sex", fontsize=12)
ax1.set_ylabel("Survival Rate")
for i, v in enumerate(sex_surv.values):
    if pd.notna(v):
        ax1.text(i, v + 0.03, f"{v:.0%}", ha="center", va="bottom", fontsize=10)
ax1.grid(axis="y", alpha=0.3)

# (0,2) Survival rate by Class
ax2 = fig.add_subplot(gs[0, 2])
ax2.bar(class_surv.index.astype(int).astype(str), class_surv.values)
ax2.set_ylim(0, 1)
ax2.set_title("Survival Rate by Passenger Class", fontsize=12)
ax2.set_xlabel("pclass (1 = Upper, 3 = Lower)")
ax2.set_ylabel("Survival Rate")
for i, v in enumerate(class_surv.values):
    if pd.notna(v):
        ax2.text(i, v + 0.03, f"{v:.0%}", ha="center", va="bottom", fontsize=10)
ax2.grid(axis="y", alpha=0.3)

# (0,3) Heatmap-like survival by sex x Class
ax3 = fig.add_subplot(gs[0, 3])
ax3.set_title("Survival Rate: sex × Class", fontsize=12)
im = ax3.imshow(pivot.values, aspect="auto")
ax3.set_yticks(range(pivot.shape[0]))
ax3.set_yticklabels(pivot.index.astype(str))
ax3.set_xticks(range(pivot.shape[1]))
ax3.set_xticklabels([str(int(c)) for c in pivot.columns])
ax3.set_xlabel("pclass")
ax3.set_ylabel("sex")
for i in range(pivot.shape[0]):
    for j in range(pivot.shape[1]):
        val = pivot.values[i, j]
        ax3.text(j, i, "N/A" if pd.isna(val) else f"{val:.0%}", ha="center", va="center", fontsize=10)
cbar = fig.colorbar(im, ax=ax3, fraction=0.046, pad=0.04)
cbar.set_label("Survival Rate")

# (1,0:2) age distribution by survival (hist)
ax4 = fig.add_subplot(gs[1, 0:2])
ax4.set_title("age Distribution by Survival", fontsize=12)
age_survived = pd.to_numeric(df.loc[df["survived"] == 1, "age"], errors="coerce").dropna()
age_died = pd.to_numeric(df.loc[df["survived"] == 0, "age"], errors="coerce").dropna()
bins = np.arange(0, 81, 5)
if len(age_died):
    ax4.hist(age_died, bins=bins, alpha=0.6, label="Died")
if len(age_survived):
    ax4.hist(age_survived, bins=bins, alpha=0.6, label="survived")
ax4.set_xlabel("age")
ax4.set_ylabel("Passengers")
ax4.legend()
ax4.grid(axis="y", alpha=0.3)

# (1,2) Survival rate by age Bin
ax5 = fig.add_subplot(gs[1, 2])
ax5.set_title("Survival Rate by age Group", fontsize=12)
ax5.bar(age_surv.index.astype(str), age_surv.values)
ax5.set_ylim(0, 1)
ax5.tick_params(axis="x", rotation=45, labelsize=9)
ax5.set_ylabel("Survival Rate")
for i, v in enumerate(age_surv.values):
    if pd.notna(v):
        ax5.text(i, v + 0.03, f"{v:.0%}", ha="center", va="bottom", fontsize=9)
ax5.grid(axis="y", alpha=0.3)

# (1,3) Survival by embarked
ax6 = fig.add_subplot(gs[1, 3])
ax6.set_title("Survival Rate by Embarkation Port", fontsize=12)
ax6.bar(emb_surv.index.astype(str), emb_surv.values)
ax6.set_ylim(0, 1)
ax6.set_xlabel("embarked (C/Cherbourg, Q/Queenstown, S/Southampton)")
ax6.set_ylabel("Survival Rate")
for i, v in enumerate(emb_surv.values):
    if pd.notna(v):
        ax6.text(i, v + 0.03, f"{v:.0%}", ha="center", va="bottom", fontsize=10)
ax6.grid(axis="y", alpha=0.3)

# (2,0:2) Class counts stacked by survival
ax7 = fig.add_subplot(gs[2, 0:2])
ax7.set_title("Passenger Counts by Class and Survival", fontsize=12)
x = np.arange(len(counts.index))
died = counts.get("Died", pd.Series([0]*len(x), index=counts.index)).values
surv = counts.get("survived", pd.Series([0]*len(x), index=counts.index)).values
ax7.bar(x, died, label="Died")
ax7.bar(x, surv, bottom=died, label="survived")
ax7.set_xticks(x)
ax7.set_xticklabels([str(int(i)) for i in counts.index])
ax7.set_xlabel("pclass")
ax7.set_ylabel("Passengers")
ax7.legend()
ax7.grid(axis="y", alpha=0.3)

# (2,2) Survival rate by fare quartile
ax8 = fig.add_subplot(gs[2, 2])
ax8.set_title("Survival Rate by fare (Quartiles)", fontsize=12)
ax8.bar(fare_surv.index.astype(str), fare_surv.values)
ax8.set_ylim(0, 1)
ax8.set_xlabel("fare Bin")
ax8.set_ylabel("Survival Rate")
for i, v in enumerate(fare_surv.values):
    if pd.notna(v):
        ax8.text(i, v + 0.03, f"{v:.0%}", ha="center", va="bottom", fontsize=10)
ax8.grid(axis="y", alpha=0.3)

# (2,3) Survival by Family size (line + annotation of counts)
ax9 = fig.add_subplot(gs[2, 3])
ax9.set_title("Survival Rate by Family Size", fontsize=12)
ax9.plot(fam_surv.index.values, fam_surv.values, marker="o")
ax9.set_ylim(0, 1)
ax9.set_xlabel("Family Size (sibsp + parch + 1)")
ax9.set_ylabel("Survival Rate")
ax9.grid(axis="y", alpha=0.3)
# annotate with counts for context (small, unobtrusive)
for fs, rate in zip(fam_surv.index.values, fam_surv.values):
    cnt = int(fam_cnt.loc[fs]) if fs in fam_cnt.index else 0
    if pd.notna(rate):
        ax9.text(fs, rate + 0.03, f"n={cnt}", ha="center", va="bottom", fontsize=8)

# Render
# plt.show()   POPUP WINDOW. EDIT :

# plt.tight_layout()
plt.savefig('outputs/gpt5.2_manual/run8_dashboard_poor.png', dpi=300)
print("Dashboard saved successfully!")
