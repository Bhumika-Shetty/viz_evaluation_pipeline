'''
Prompt :
The Customer Segments dataset contains marketing and customer data.
Create a visualization showing customer clusters or segments.
Provide ONLY the Python code wrapped in triple backticks.

'''

# =========================
# MANUAL FIXES APPLIED (DOCUMENTED)
# Model output issues:
#   - Model initially returned a visualization (image) instead of Python code, despite prompt explicitly
#     stating "Provide ONLY the Python code wrapped in triple backticks." User had to manually ask the
#     model to output the Python code.
#   - Used df = pd.read_csv("/mnt/user-data/uploads/customer_segments.csv") (path not valid in repo)
#   - Saved to "customer_segments_viz.png" (grader requires "output.png")
#
# Minimal fixes (no visual/logic changes intended):
#   1) Input path portability:
#        pd.read_csv("/mnt/user-data/uploads/customer_segments.csv")  ->  pd.read_csv("data/customer_segments.csv")
#   2) Output capture for evaluation:
#        plt.savefig("customer_segments_viz.png", dpi=180, ...)  ->  plt.savefig("output.png", dpi=300, bbox_inches="tight", ...)
# =========================


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ── Load & Prepare Data ──────────────────────────────────────────────
df = pd.read_csv("data/customer_segments.csv")
df["Income"] = pd.to_numeric(df["Income"], errors="coerce")
df.dropna(subset=["Income"], inplace=True)

# Feature engineering
df["Age"] = 2025 - df["Year_Birth"]
df["TotalSpend"] = (df["MntWines"] + df["MntFruits"] + df["MntMeatProducts"] +
                    df["MntFishProducts"] + df["MntSweetProducts"] + df["MntGoldProds"])
df["TotalPurchases"] = (df["NumDealsPurchases"] + df["NumWebPurchases"] +
                        df["NumCatalogPurchases"] + df["NumStorePurchases"])
df["TotalChildren"] = df["Kidhome"] + df["Teenhome"]
df["TotalCampaignsAcc"] = (df["AcceptedCmp1"] + df["AcceptedCmp2"] + df["AcceptedCmp3"] +
                           df["AcceptedCmp4"] + df["AcceptedCmp5"] + df["Response"])

features = ["Income", "TotalSpend", "TotalPurchases", "Recency",
            "Age", "TotalChildren", "NumWebVisitsMonth", "TotalCampaignsAcc"]

X = df[features].copy()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ── KMeans Clustering ─────────────────────────────────────────────────
kmeans = KMeans(n_clusters=4, random_state=42, n_init=20)
df["Cluster"] = kmeans.fit_predict(X_scaled)

# ── PCA for 2D projection ────────────────────────────────────────────
pca = PCA(n_components=2)
pca_coords = pca.fit_transform(X_scaled)
df["PC1"] = pca_coords[:, 0]
df["PC2"] = pca_coords[:, 1]

# ── Cluster Labels ────────────────────────────────────────────────────
cluster_profiles = df.groupby("Cluster")[["Income", "TotalSpend", "TotalChildren"]].mean()
label_map = {}
sorted_by_spend = cluster_profiles.sort_values("TotalSpend")
labels = ["Budget-Conscious", "Moderate Spenders", "High-Value", "Premium Elite"]
for i, idx in enumerate(sorted_by_spend.index):
    label_map[idx] = labels[i]
df["Segment"] = df["Cluster"].map(label_map)

# ── Color Palette ─────────────────────────────────────────────────────
palette = {
    "Budget-Conscious": "#5B8DBE",
    "Moderate Spenders": "#F0A35E",
    "High-Value": "#6DBE8A",
    "Premium Elite": "#D95B5B"
}
segment_order = ["Budget-Conscious", "Moderate Spenders", "High-Value", "Premium Elite"]

# ── Plot ──────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(20, 14), facecolor="#0F1117")
gs = gridspec.GridSpec(2, 3, hspace=0.35, wspace=0.30,
                       left=0.06, right=0.97, top=0.90, bottom=0.06)

title_color = "#EAEAEA"
label_color = "#B0B0B0"
grid_color = "#2A2D3A"
bg_color = "#0F1117"
ax_face = "#181B25"

def style_ax(ax, title="", xlabel="", ylabel=""):
    ax.set_facecolor(ax_face)
    ax.set_title(title, color=title_color, fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel, color=label_color, fontsize=10)
    ax.set_ylabel(ylabel, color=label_color, fontsize=10)
    ax.tick_params(colors=label_color, labelsize=9)
    for spine in ax.spines.values():
        spine.set_color(grid_color)
    ax.grid(True, color=grid_color, alpha=0.4, linewidth=0.5)

# ── 1. PCA Scatter ───────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0:2])
for seg in segment_order:
    mask = df["Segment"] == seg
    ax1.scatter(df.loc[mask, "PC1"], df.loc[mask, "PC2"],
                c=palette[seg], label=seg, s=22, alpha=0.65, edgecolors="white", linewidths=0.2)
style_ax(ax1, "Customer Segments — PCA Projection",
         f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)",
         f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)")
legend = ax1.legend(fontsize=10, loc="upper right", framealpha=0.15, edgecolor=grid_color)
for text in legend.get_texts():
    text.set_color(title_color)

# ── 2. Segment Size Donut ────────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 2])
sizes = df["Segment"].value_counts().reindex(segment_order)
colors = [palette[s] for s in segment_order]
wedges, texts, autotexts = ax2.pie(
    sizes, labels=None, colors=colors, autopct="%1.1f%%",
    startangle=90, pctdistance=0.78, wedgeprops=dict(width=0.45, edgecolor=bg_color, linewidth=2))
for t in autotexts:
    t.set_color(title_color)
    t.set_fontsize(9)
ax2.set_title("Segment Distribution", color=title_color, fontsize=13, fontweight="bold", pad=12)
ax2.legend(wedges, segment_order, loc="lower center", fontsize=8.5,
           framealpha=0.15, edgecolor=grid_color, ncol=2,
           bbox_to_anchor=(0.5, -0.08))
for text in ax2.get_legend().get_texts():
    text.set_color(title_color)

# ── 3. Income vs Total Spend ─────────────────────────────────────────
ax3 = fig.add_subplot(gs[1, 0])
for seg in segment_order:
    mask = df["Segment"] == seg
    ax3.scatter(df.loc[mask, "Income"], df.loc[mask, "TotalSpend"],
                c=palette[seg], s=18, alpha=0.55, edgecolors="white", linewidths=0.15)
style_ax(ax3, "Income vs Total Spending", "Income ($)", "Total Spend ($)")

# ── 4. Avg Metrics by Segment (Grouped Bar) ─────────────────────────
ax4 = fig.add_subplot(gs[1, 1])
radar_feats = ["Income", "TotalSpend", "TotalPurchases", "Recency", "NumWebVisitsMonth"]
radar_labels = ["Income", "Spend", "Purchases", "Recency", "Web Visits"]
seg_means = df.groupby("Segment")[radar_feats].mean().reindex(segment_order)
seg_normed = (seg_means - seg_means.min()) / (seg_means.max() - seg_means.min())

x_pos = np.arange(len(radar_labels))
bar_w = 0.18
for i, seg in enumerate(segment_order):
    ax4.bar(x_pos + i * bar_w, seg_normed.loc[seg], bar_w,
            color=palette[seg], alpha=0.85, label=seg, edgecolor="none")
ax4.set_xticks(x_pos + bar_w * 1.5)
ax4.set_xticklabels(radar_labels, fontsize=9)
style_ax(ax4, "Normalized Avg Metrics by Segment", "", "Normalized Value")
ax4.legend(fontsize=7.5, loc="upper right", framealpha=0.15, edgecolor=grid_color)
for text in ax4.get_legend().get_texts():
    text.set_color(title_color)

# ── 5. Spending Category Breakdown ───────────────────────────────────
ax5 = fig.add_subplot(gs[1, 2])
spend_cats = ["MntWines", "MntFruits", "MntMeatProducts", "MntFishProducts", "MntSweetProducts", "MntGoldProds"]
spend_labels = ["Wine", "Fruit", "Meat", "Fish", "Sweets", "Gold"]
cat_means = df.groupby("Segment")[spend_cats].mean().reindex(segment_order)

bottom = np.zeros(len(segment_order))
cat_colors = ["#8B5CF6", "#EC4899", "#F97316", "#06B6D4", "#84CC16", "#EAB308"]
for j, (cat, lbl) in enumerate(zip(spend_cats, spend_labels)):
    vals = cat_means[cat].values
    ax5.barh(segment_order, vals, left=bottom, color=cat_colors[j], label=lbl, height=0.55)
    bottom += vals
style_ax(ax5, "Avg Spending by Category", "Average Amount ($)", "")
ax5.legend(fontsize=7.5, loc="lower right", framealpha=0.15, edgecolor=grid_color)
for text in ax5.get_legend().get_texts():
    text.set_color(title_color)

# ── Suptitle ──────────────────────────────────────────────────────────
fig.suptitle("Customer Segmentation Analysis", fontsize=22,
             fontweight="bold", color="#FFFFFF", y=0.96)

plt.savefig("output.png", dpi=300, bbox_inches="tight", facecolor=bg_color)
plt.close()
