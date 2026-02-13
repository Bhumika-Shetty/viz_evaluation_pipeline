'''
Prompt :
The Sleep Health and Lifestyle dataset contains health and lifestyle data.
Create a visualization showing clusters or groupings within the sleep data.
Provide ONLY the Python code wrapped in triple backticks.

'''

# =========================
# MANUAL FIXES APPLIED (DOCUMENTED)
# Model output issues:
#   - Model initially returned a visualization (image) instead of Python code, despite prompt explicitly
#     stating "Provide ONLY the Python code wrapped in triple backticks." User had to manually ask the
#     model to output the Python code.
#   - Used df = pd.read_csv("Sleep_health_and_lifestyle_dataset.csv") (file not in repo root)
#   - Saved to "sleep_clusters.png" (grader requires "output.png")
#   - Used plt.show() and did not close figure (evaluation expects saved file only)
#
# Minimal fixes (no visual/logic changes intended):
#   1) Input path portability:
#        pd.read_csv("Sleep_health_and_lifestyle_dataset.csv")  ->  pd.read_csv("data/Sleep_health_and_lifestyle_dataset.csv")
#   2) Output capture for evaluation:
#        plt.savefig("sleep_clusters.png", dpi=180, ...)  ->  plt.savefig("output.png", dpi=300, bbox_inches="tight", ...)
#   3) Removed plt.show(), added plt.close()
# =========================


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from matplotlib.patches import Ellipse

# ---------- Load & Prepare ----------
df = pd.read_csv("data/Sleep_health_and_lifestyle_dataset.csv")

df[["Systolic_BP", "Diastolic_BP"]] = (
    df["Blood Pressure"].str.split("/", expand=True).astype(float)
)

features = [
    "Sleep Duration", "Quality of Sleep", "Physical Activity Level",
    "Stress Level", "Heart Rate", "Daily Steps",
    "Systolic_BP", "Diastolic_BP", "Age",
]

X = df[features].dropna()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ---------- K-Means Clustering ----------
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)

# ---------- PCA for 2-D projection ----------
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# ---------- Cluster labels based on profile ----------
cluster_df = pd.DataFrame(X.values, columns=features)
cluster_df["Cluster"] = clusters
profiles = cluster_df.groupby("Cluster")[features].mean()

label_map = {}
remaining = set(range(4))
c = profiles["Quality of Sleep"].idxmax(); label_map[c] = "Healthy Sleepers"; remaining.discard(c)
c = profiles.loc[list(remaining), "Stress Level"].idxmax(); label_map[c] = "High-Stress / Poor Sleep"; remaining.discard(c)
c = profiles.loc[list(remaining), "Physical Activity Level"].idxmax(); label_map[c] = "Active Lifestyle"; remaining.discard(c)
label_map[list(remaining)[0]] = "Sedentary / At-Risk"

cluster_names = [label_map[c] for c in clusters]

# ---------- Visualization ----------
plt.rcParams.update({
    "font.family": "serif",
    "axes.facecolor": "#0d1117",
    "figure.facecolor": "#0d1117",
    "text.color": "#c9d1d9",
    "axes.labelcolor": "#c9d1d9",
    "xtick.color": "#8b949e",
    "ytick.color": "#8b949e",
})

palette = {
    "Healthy Sleepers":         "#58d68d",
    "High-Stress / Poor Sleep": "#e74c3c",
    "Active Lifestyle":         "#3498db",
    "Sedentary / At-Risk":      "#f39c12",
}

fig = plt.figure(figsize=(18, 10))
gs = gridspec.GridSpec(2, 3, width_ratios=[2.5, 1, 1], hspace=0.35, wspace=0.35)

# ── Main scatter ──
ax_main = fig.add_subplot(gs[:, 0])
for name, color in palette.items():
    mask = np.array(cluster_names) == name
    ax_main.scatter(
        X_pca[mask, 0], X_pca[mask, 1],
        c=color, label=name, s=60, alpha=0.8,
        edgecolors="white", linewidths=0.3,
    )
    if mask.sum() > 2:
        pts = X_pca[mask]
        cov = np.cov(pts, rowvar=False)
        vals, vecs = np.linalg.eigh(cov)
        angle = np.degrees(np.arctan2(vecs[1, 1], vecs[0, 1]))
        w, h = 2 * 1.8 * np.sqrt(vals)
        ell = Ellipse(
            xy=pts.mean(axis=0), width=w, height=h, angle=angle,
            facecolor=color, alpha=0.08, edgecolor=color, linewidth=1.2,
            linestyle="--",
        )
        ax_main.add_patch(ell)

ax_main.set_xlabel(f"PC 1  ({pca.explained_variance_ratio_[0]:.0%} variance)", fontsize=12)
ax_main.set_ylabel(f"PC 2  ({pca.explained_variance_ratio_[1]:.0%} variance)", fontsize=12)
ax_main.set_title("Sleep Health Clusters  —  PCA Projection", fontsize=16, fontweight="bold", color="white", pad=14)
ax_main.legend(loc="lower right", fontsize=9, frameon=True, facecolor="#161b22", edgecolor="#30363d", labelcolor="#c9d1d9")
ax_main.grid(True, alpha=0.08)

# ── Radar chart ──
radar_features = ["Sleep Duration", "Quality of Sleep", "Physical Activity Level",
                   "Stress Level", "Heart Rate", "Daily Steps"]
radar_labels = ["Sleep\nDuration", "Sleep\nQuality", "Activity\nLevel",
                "Stress", "Heart\nRate", "Daily\nSteps"]

means = cluster_df.groupby("Cluster")[radar_features].mean()
mins = cluster_df[radar_features].min()
maxs = cluster_df[radar_features].max()
normed = (means - mins) / (maxs - mins)

angles = np.linspace(0, 2 * np.pi, len(radar_features), endpoint=False).tolist()
angles += angles[:1]

ax_radar = fig.add_subplot(gs[0, 1:], polar=True)
ax_radar.set_facecolor("#0d1117")
for cid, name in label_map.items():
    vals = normed.loc[cid].tolist() + [normed.loc[cid].tolist()[0]]
    ax_radar.fill(angles, vals, alpha=0.12, color=palette[name])
    ax_radar.plot(angles, vals, color=palette[name], linewidth=1.8, label=name)

ax_radar.set_xticks(angles[:-1])
ax_radar.set_xticklabels(radar_labels, fontsize=8, color="#8b949e")
ax_radar.set_yticks([0.25, 0.5, 0.75, 1.0])
ax_radar.set_yticklabels(["25%", "50%", "75%", "100%"], fontsize=7, color="#484f58")
ax_radar.set_title("Cluster Profiles", fontsize=13, fontweight="bold", color="white", pad=18)
ax_radar.grid(True, alpha=0.15)

# ── Box plots ──
ax_box1 = fig.add_subplot(gs[1, 1])
ax_box2 = fig.add_subplot(gs[1, 2])

for ax, feat, title in [
    (ax_box1, "Sleep Duration", "Sleep Duration (hrs)"),
    (ax_box2, "Stress Level", "Stress Level"),
]:
    data = [cluster_df.loc[cluster_df["Cluster"] == cid, feat].values for cid in label_map]
    bp = ax.boxplot(
        data, patch_artist=True, widths=0.6,
        medianprops=dict(color="white", linewidth=1.5),
        whiskerprops=dict(color="#8b949e"),
        capprops=dict(color="#8b949e"),
        flierprops=dict(marker="o", markersize=3, markerfacecolor="#8b949e", alpha=0.5),
    )
    for patch, (cid, name) in zip(bp["boxes"], label_map.items()):
        patch.set_facecolor(palette[name])
        patch.set_alpha(0.65)
        patch.set_edgecolor("white")
        patch.set_linewidth(0.5)
    ax.set_xticklabels(
        [n.split("/")[0].split()[0] for n in label_map.values()],
        fontsize=7, rotation=30, ha="right",
    )
    ax.set_title(title, fontsize=11, fontweight="bold", color="white", pad=8)
    ax.grid(True, axis="y", alpha=0.08)

fig.suptitle("Sleep Health & Lifestyle  ·  K-Means Cluster Analysis", fontsize=20, fontweight="bold", color="white", y=0.98)

plt.savefig("output.png", dpi=300, bbox_inches="tight", facecolor="#0d1117")
plt.close()
