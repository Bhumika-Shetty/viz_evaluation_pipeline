import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Load data (required path first)
# -----------------------------
data_path = "data/titanic.csv"
fallback_path = "/mnt/data/titanic.csv"

if os.path.exists(data_path):
    df = pd.read_csv(data_path)
elif os.path.exists(fallback_path):
    df = pd.read_csv(fallback_path)
else:
    raise FileNotFoundError("Could not find 'data/titanic.csv' or '/mnt/data/titanic.csv'.")

# -----------------------------
# Basic cleaning / feature engineering
# -----------------------------
df = df.copy()

# Ensure key fields exist and types are sane
df = df.dropna(subset=["survived"])
df["survived"] = df["survived"].astype(int)

# Standardize expected categories
if "pclass" in df.columns:
    df = df.dropna(subset=["pclass"])
    df["pclass"] = df["pclass"].astype(int)
    df = df[df["pclass"].isin([1, 2, 3])]

if "sex" in df.columns:
    df["sex"] = df["sex"].astype(str).str.lower().str.strip()
    df.loc[~df["sex"].isin(["male", "female"]), "sex"] = np.nan

# Missing values handling (appropriate, minimal, non-distorting)
# Age and fare: median imputation for plotting distributions with full sample size
if "age" in df.columns:
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df["age_filled"] = df["age"].fillna(df["age"].median())
else:
    df["age_filled"] = np.nan

if "fare" in df.columns:
    df["fare"] = pd.to_numeric(df["fare"], errors="coerce")
    df["fare_filled"] = df["fare"].fillna(df["fare"].median())
else:
    df["fare_filled"] = np.nan

# Embarkation
if "embarked" in df.columns:
    df["embarked"] = df["embarked"].astype(str).str.upper().str.strip()
    df.loc[~df["embarked"].isin(["C", "Q", "S"]), "embarked"] = np.nan

# Family size (sibsp + parch + 1)
for col in ["sibsp", "parch"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    else:
        df[col] = 0

df["family_size"] = df["sibsp"] + df["parch"] + 1

# Helpful labels
pclass_label = {1: "1st", 2: "2nd", 3: "3rd"}
df["pclass_label"] = df.get("pclass", np.nan).map(pclass_label)

surv_label = {0: "Not Survived", 1: "Survived"}
df["survived_label"] = df["survived"].map(surv_label)

# -----------------------------
# Styling
# -----------------------------
sns.set_theme(style="whitegrid")
palette2 = sns.color_palette("colorblind", 2)
col_not, col_yes = palette2[0], palette2[1]

# -----------------------------
# Figure + layout (2x3 dashboard)
# -----------------------------
fig, axes = plt.subplots(2, 3, figsize=(16, 9))
fig.suptitle("Titanic Disaster: Comprehensive Survival Analysis", fontsize=18, y=0.98)

# -------- Panel 1: Survival by class (rates + counts)
ax = axes[0, 0]
class_order = ["1st", "2nd", "3rd"]
tmp = df.dropna(subset=["pclass_label"]).copy()

# counts by class & survived
ct = (
    tmp.groupby(["pclass_label", "survived"])
       .size()
       .reset_index(name="count")
)

# ensure both survived categories exist for each class
idx = pd.MultiIndex.from_product([class_order, [0, 1]], names=["pclass_label", "survived"])
ct = (
    ct.set_index(["pclass_label", "survived"])
      .reindex(idx, fill_value=0)
      .reset_index()
)

count_not = ct[ct["survived"] == 0].set_index("pclass_label").loc[class_order]["count"].to_numpy()
count_yes = ct[ct["survived"] == 1].set_index("pclass_label").loc[class_order]["count"].to_numpy()

x = np.arange(len(class_order))
w = 0.38
b0 = ax.bar(x - w/2, count_not, width=w, color=col_not, label="Not Survived")
b1 = ax.bar(x + w/2, count_yes, width=w, color=col_yes, label="Survived")

ax.set_title("Survival by Passenger Class")
ax.set_xlabel("Class")
ax.set_ylabel("Count")
ax.set_xticks(x)
ax.set_xticklabels(class_order)

# annotate survival rate per class
tot = count_not + count_yes
rate = np.where(tot > 0, count_yes / tot, 0.0)
ymax = max(tot.max(), 1)
ax.set_ylim(0, ymax * 1.25)

for i in range(len(class_order)):
    top = max(count_not[i], count_yes[i])
    ax.annotate(
        f"{rate[i]*100:.1f}%\n({int(count_yes[i])}/{int(tot[i])})",
        (x[i], top),
        textcoords="offset points",
        xytext=(0, 28),
        ha="center",
        va="bottom",
        fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="0.85")
    )

ax.legend(title="Outcome", frameon=True)

# -------- Panel 2: Survival by gender (rates)
ax = axes[0, 1]
tmp = df.dropna(subset=["sex"]).copy()
gender_order = ["female", "male"]

gender_rate = (
    tmp.groupby("sex")["survived"]
       .mean()
       .reindex(gender_order)
)

sns.barplot(
    x=gender_rate.index,
    y=gender_rate.values * 100,
    ax=ax,
    palette=[col_yes if g == "female" else col_not for g in gender_rate.index]
)

ax.set_title("Survival Rate by Gender")
ax.set_xlabel("Gender")
ax.set_ylabel("Survival Rate (%)")
ax.set_ylim(0, 100)

# annotate with counts and %
gender_counts = tmp.groupby(["sex", "survived"]).size().unstack(fill_value=0).reindex(gender_order)
for i, g in enumerate(gender_rate.index):
    surv = int(gender_counts.loc[g, 1]) if 1 in gender_counts.columns else 0
    total = int(gender_counts.loc[g].sum())
    ax.annotate(
        f"{gender_rate.loc[g]*100:.1f}%\n({surv}/{total})",
        (i, gender_rate.loc[g] * 100),
        textcoords="offset points",
        xytext=(0, 8),
        ha="center",
        va="bottom",
        fontsize=9
    )

# -------- Panel 3: Age distribution by survival
ax = axes[0, 2]
tmp = df.dropna(subset=["survived"]).copy()

# Use filled ages to keep consistent sample size; show by survival
sns.kdeplot(
    data=tmp,
    x="age_filled",
    hue="survived_label",
    ax=ax,
    common_norm=False,
    fill=True,
    alpha=0.35,
    linewidth=1.2,
    palette={"Not Survived": col_not, "Survived": col_yes}
)

ax.set_title("Age Distribution (KDE)")
ax.set_xlabel("Age (years)")
ax.set_ylabel("Density")
ax.legend(title="Outcome")

# -------- Panel 4: Fare distribution by survival (log-scaled x for interpretability)
ax = axes[1, 0]
tmp = df.copy()
tmp = tmp[tmp["fare_filled"].notna()]
tmp["fare_pos"] = tmp["fare_filled"].clip(lower=0.01)  # avoid log(0)

sns.histplot(
    data=tmp,
    x="fare_pos",
    hue="survived_label",
    bins=35,
    element="step",
    stat="density",
    common_norm=False,
    ax=ax,
    palette={"Not Survived": col_not, "Survived": col_yes},
    alpha=0.35
)

ax.set_xscale("log")
ax.set_title("Fare Distribution (log scale)")
ax.set_xlabel("Fare (log scale)")
ax.set_ylabel("Density")
ax.legend(title="Outcome")

# -------- Panel 5: Family size vs survival rate
ax = axes[1, 1]
tmp = df.copy()

# cap family size for readability (long tail)
cap = 8
tmp["family_size_capped"] = tmp["family_size"].clip(upper=cap)

fam_rate = (
    tmp.groupby("family_size_capped")["survived"]
       .mean()
       .reset_index()
)

sns.lineplot(
    data=fam_rate,
    x="family_size_capped",
    y=fam_rate["survived"] * 100,
    ax=ax,
    marker="o",
    linewidth=2
)

ax.set_title("Survival Rate by Family Size")
ax.set_xlabel(f"Family Size (capped at {cap})")
ax.set_ylabel("Survival Rate (%)")
ax.set_ylim(0, 100)

# Add sample size labels for each family size
fam_n = tmp.groupby("family_size_capped").size().reindex(fam_rate["family_size_capped"]).to_numpy()
for xval, yval, n in zip(fam_rate["family_size_capped"], fam_rate["survived"] * 100, fam_n):
    ax.annotate(f"n={int(n)}", (xval, yval), textcoords="offset points", xytext=(0, 8),
                ha="center", va="bottom", fontsize=8)

# -------- Panel 6: Embarkation vs survival (rate + counts)
ax = axes[1, 2]
tmp = df.dropna(subset=["embarked"]).copy()
emb_order = ["C", "Q", "S"]

emb_rate = (
    tmp.groupby("embarked")["survived"]
       .mean()
       .reindex(emb_order)
)

sns.barplot(
    x=emb_rate.index,
    y=emb_rate.values * 100,
    ax=ax,
    palette=sns.color_palette("colorblind", len(emb_order))
)

ax.set_title("Survival Rate by Embarkation Port")
ax.set_xlabel("Embarked (C/Q/S)")
ax.set_ylabel("Survival Rate (%)")
ax.set_ylim(0, 100)

# annotate counts
emb_counts = tmp.groupby(["embarked", "survived"]).size().unstack(fill_value=0).reindex(emb_order)
for i, e in enumerate(emb_rate.index):
    surv = int(emb_counts.loc[e, 1]) if 1 in emb_counts.columns else 0
    total = int(emb_counts.loc[e].sum())
    ax.annotate(
        f"{emb_rate.loc[e]*100:.1f}%\n({surv}/{total})",
        (i, emb_rate.loc[e] * 100),
        textcoords="offset points",
        xytext=(0, 8),
        ha="center",
        va="bottom",
        fontsize=9
    )

# -----------------------------
# Final polish + save
# -----------------------------
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("output.png", dpi=300, bbox_inches="tight")
plt.close(fig)
