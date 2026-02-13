'''
Prompt (Rich Context):
You are an expert data scientist and visualization specialist.
Dataset: Titanic (data/titanic.csv); schema provided with lowercase columns.
Technical: Load from data/titanic.csv, save as output.png (DPI 300), use matplotlib/seaborn/plotly.
Task: Create a multi-panel dashboard (2x3 or 3x2) showing 4-6 aspects: survival by class, gender,
  age distribution, fare distribution, family size, embarkation; title "Titanic Disaster: Comprehensive Survival Analysis".
Provide ONLY the Python code wrapped in triple backticks.

'''

# =========================
# MANUAL FIXES APPLIED (DOCUMENTED)
# Model output issues:
#   - Model initially returned a visualization (image) instead of Python code, despite prompt explicitly
#     stating "Provide ONLY the Python code wrapped in triple backticks." User had to manually ask the
#     model to output the Python code.
#
# Code/execution:
#   - No path or output changes needed; code already used data/titanic.csv, output.png, plt.close().
# =========================


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from matplotlib.patches import Patch
from matplotlib.gridspec import GridSpec

# ── Style & Palette ──────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", font_scale=0.95)
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titleweight": "bold",
    "axes.titlesize": 11,
    "axes.labelsize": 9.5,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "figure.facecolor": "#F7F7F7",
    "axes.facecolor": "#FFFFFF",
    "axes.edgecolor": "#CCCCCC",
    "grid.color": "#EBEBEB",
    "grid.linewidth": 0.6,
})

# Colorblind-friendly IBM palette
C_DIED = "#DC267F"      # magenta-pink
C_SURV = "#648FFF"      # blue
C_ACC1 = "#FFB000"      # amber
C_ACC2 = "#785EF0"      # violet
PAL_SURV = [C_DIED, C_SURV]
PAL_CLASS = ["#648FFF", "#FFB000", "#DC267F"]

# ── Data ─────────────────────────────────────────────────────────────────────
df = pd.read_csv("data/titanic.csv")
df["family_size"] = df["sibsp"] + df["parch"]
df["family_grp"] = pd.cut(
    df["family_size"], bins=[-1, 0, 2, 5, 12],
    labels=["Alone", "Small (1-2)", "Medium (3-5)", "Large (6+)"]
)
df["survived_label"] = df["survived"].map({0: "Died", 1: "Survived"})

# ── Figure ───────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(18, 11), dpi=150)
gs = GridSpec(2, 3, figure=fig, hspace=0.38, wspace=0.30,
              left=0.06, right=0.97, top=0.89, bottom=0.06)

fig.suptitle("Titanic Disaster: Comprehensive Survival Analysis",
             fontsize=20, fontweight="bold", y=0.96, color="#1A1A2E")
fig.text(0.5, 0.925,
         f"891 passengers  ·  342 survived (38.4 %)  ·  549 perished (61.6 %)",
         ha="center", fontsize=11, color="#555555", style="italic")

legend_elements = [Patch(facecolor=C_DIED, label="Died"),
                   Patch(facecolor=C_SURV, label="Survived")]

# ── Helper ───────────────────────────────────────────────────────────────────
def bar_label(ax, rects, fmt="{:.0f}"):
    for r in rects:
        h = r.get_height()
        if h > 0:
            ax.text(r.get_x() + r.get_width() / 2, h + 2,
                    fmt.format(h), ha="center", va="bottom",
                    fontsize=8, color="#333333", fontweight="semibold")

# ═══════════════════════════════  PANEL 1  ═══════════════════════════════════
# Survival by Passenger Class (stacked percentage bars)
ax1 = fig.add_subplot(gs[0, 0])
ct = pd.crosstab(df["class"], df["survived_label"])
ct = ct[["Died", "Survived"]]
pct = ct.div(ct.sum(axis=1), axis=0) * 100
pct.plot.bar(stacked=True, color=PAL_SURV, ax=ax1, width=0.6, edgecolor="white", linewidth=0.8)
ax1.set_title("Survival Rate by Passenger Class")
ax1.set_xlabel(""); ax1.set_ylabel("Percentage (%)")
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=0)
ax1.legend(handles=legend_elements, loc="upper right", fontsize=8, framealpha=0.9)
ax1.set_ylim(0, 105)
for i, (cls, row) in enumerate(pct.iterrows()):
    survived_pct = row["Survived"]
    ax1.text(i, 50, f"{survived_pct:.1f}%\nsurvived",
             ha="center", va="center", fontsize=9, fontweight="bold", color="white")

# ═══════════════════════════════  PANEL 2  ═══════════════════════════════════
# Survival by Gender (grouped bars with counts)
ax2 = fig.add_subplot(gs[0, 1])
gender_surv = df.groupby(["sex", "survived_label"]).size().unstack(fill_value=0)
gender_surv = gender_surv[["Died", "Survived"]]
x = np.arange(len(gender_surv))
w = 0.32
r1 = ax2.bar(x - w/2, gender_surv["Died"], w, color=C_DIED, edgecolor="white", linewidth=0.8, label="Died")
r2 = ax2.bar(x + w/2, gender_surv["Survived"], w, color=C_SURV, edgecolor="white", linewidth=0.8, label="Survived")
bar_label(ax2, r1); bar_label(ax2, r2)
ax2.set_xticks(x)
ax2.set_xticklabels(["Female", "Male"])
ax2.set_title("Survival Count by Gender")
ax2.set_ylabel("Passengers")
ax2.legend(handles=legend_elements, fontsize=8, framealpha=0.9)
for i, sex in enumerate(gender_surv.index):
    total = gender_surv.loc[sex].sum()
    surv = gender_surv.loc[sex, "Survived"]
    ax2.text(i, gender_surv.loc[sex].max() + 28,
             f"{surv/total*100:.0f}% survived", ha="center",
             fontsize=8.5, fontweight="bold", color="#333")

# ═══════════════════════════════  PANEL 3  ═══════════════════════════════════
# Age Distribution by Survival (overlapping KDE + histogram)
ax3 = fig.add_subplot(gs[0, 2])
age_died = df[df["survived"] == 0]["age"].dropna()
age_surv = df[df["survived"] == 1]["age"].dropna()
bins = np.arange(0, 82, 4)
ax3.hist(age_died, bins=bins, color=C_DIED, alpha=0.45, edgecolor="white", linewidth=0.5, label="Died")
ax3.hist(age_surv, bins=bins, color=C_SURV, alpha=0.55, edgecolor="white", linewidth=0.5, label="Survived")
ax3_tw = ax3.twinx()
sns.kdeplot(age_died, ax=ax3_tw, color=C_DIED, linewidth=2, bw_adjust=0.8)
sns.kdeplot(age_surv, ax=ax3_tw, color=C_SURV, linewidth=2, bw_adjust=0.8)
ax3_tw.set_ylabel(""); ax3_tw.set_yticks([])
ax3.set_title("Age Distribution by Survival")
ax3.set_xlabel("Age"); ax3.set_ylabel("Count")
ax3.legend(handles=legend_elements, fontsize=8, framealpha=0.9)
ax3.axvline(age_died.median(), color=C_DIED, ls="--", lw=1, alpha=0.7)
ax3.axvline(age_surv.median(), color=C_SURV, ls="--", lw=1, alpha=0.7)
ax3.text(age_died.median()+1, ax3.get_ylim()[1]*0.92, f"Med={age_died.median():.0f}", fontsize=7.5, color=C_DIED)
ax3.text(age_surv.median()+1, ax3.get_ylim()[1]*0.82, f"Med={age_surv.median():.0f}", fontsize=7.5, color=C_SURV)

# ═══════════════════════════════  PANEL 4  ═══════════════════════════════════
# Fare Distribution (box + strip)
ax4 = fig.add_subplot(gs[1, 0])
sns.boxplot(data=df, x="survived_label", y="fare", order=["Died", "Survived"],
            palette=PAL_SURV, width=0.45, fliersize=2.5,
            boxprops=dict(edgecolor="#555", linewidth=0.8),
            medianprops=dict(color="#1A1A2E", linewidth=1.5),
            ax=ax4)
sns.stripplot(data=df, x="survived_label", y="fare", order=["Died", "Survived"],
              palette=PAL_SURV, size=2, alpha=0.25, jitter=0.22, ax=ax4)
ax4.set_title("Fare Distribution by Survival")
ax4.set_xlabel(""); ax4.set_ylabel("Fare (£)")
ax4.set_ylim(-5, 300)
for i, lbl in enumerate(["Died", "Survived"]):
    med = df[df["survived_label"] == lbl]["fare"].median()
    ax4.text(i, med + 8, f"Med: £{med:.1f}", ha="center", fontsize=8, fontweight="bold", color="#333")

# ═══════════════════════════════  PANEL 5  ═══════════════════════════════════
# Family Size vs Survival Rate (bar chart)
ax5 = fig.add_subplot(gs[1, 1])
fam = df.groupby("family_grp", observed=False).agg(
    total=("survived", "count"),
    survived=("survived", "sum")
).reset_index()
fam["rate"] = fam["survived"] / fam["total"] * 100

colors_fam = [C_SURV, C_ACC1, C_ACC2, C_DIED]
bars5 = ax5.bar(fam["family_grp"], fam["rate"], color=colors_fam,
                width=0.55, edgecolor="white", linewidth=0.8)
for b, row in zip(bars5, fam.itertuples()):
    ax5.text(b.get_x() + b.get_width()/2, b.get_height() + 1.5,
             f"{row.rate:.1f}%\n(n={row.total})", ha="center",
             fontsize=8, fontweight="semibold", color="#333")
ax5.set_title("Survival Rate by Family Size")
ax5.set_ylabel("Survival Rate (%)")
ax5.set_xlabel("")
ax5.set_ylim(0, 75)

# ═══════════════════════════════  PANEL 6  ═══════════════════════════════════
# Embarkation Port (grouped horizontal bars)
ax6 = fig.add_subplot(gs[1, 2])
port_map = {"S": "Southampton", "C": "Cherbourg", "Q": "Queenstown"}
df["port"] = df["embarked"].map(port_map)
emb = df.dropna(subset=["port"]).groupby(["port", "survived_label"]).size().unstack(fill_value=0)
emb = emb.loc[["Southampton", "Cherbourg", "Queenstown"]]
emb = emb[["Died", "Survived"]]

y = np.arange(len(emb))
h = 0.32
r1 = ax6.barh(y - h/2, emb["Died"], h, color=C_DIED, edgecolor="white", linewidth=0.8)
r2 = ax6.barh(y + h/2, emb["Survived"], h, color=C_SURV, edgecolor="white", linewidth=0.8)
ax6.set_yticks(y)
ax6.set_yticklabels(emb.index)
ax6.set_title("Survival by Embarkation Port")
ax6.set_xlabel("Passengers")
ax6.legend(handles=legend_elements, fontsize=8, framealpha=0.9, loc="lower right")
for i, port in enumerate(emb.index):
    total = emb.loc[port].sum()
    surv = emb.loc[port, "Survived"]
    ax6.text(total + 8, i, f"{surv/total*100:.0f}%",
             ha="left", va="center", fontsize=8.5, fontweight="bold", color="#333")

# ── Save ─────────────────────────────────────────────────────────────────────
plt.savefig("output.png", dpi=300, facecolor=fig.get_facecolor(), bbox_inches="tight")
plt.close()
print("✓ Dashboard saved to output.png")