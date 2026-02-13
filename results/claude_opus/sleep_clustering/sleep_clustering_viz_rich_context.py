'''
Prompt (Rich Context):
You are an expert data scientist and visualization specialist.
Dataset: Sleep Health and Lifestyle (data/Sleep_health_and_lifestyle_dataset.csv); schema provided.
Technical: Load from data/Sleep_health_and_lifestyle_dataset.csv, save as output.png (DPI 300), use matplotlib/seaborn/plotly.
Task: Create a visualization showing clusters or groupings within the sleep data (sleep quality vs lifestyle);
  scatter plot, color encoding for clusters, title "Sleep Health Clusters: Lifestyle vs. Sleep Quality".
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
#   - No path or output changes needed; code already used data/Sleep_health_and_lifestyle_dataset.csv, output.png, plt.close().
# =========================


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ---------- Load & prep ----------
df = pd.read_csv('data/Sleep_health_and_lifestyle_dataset.csv')

# Parse blood pressure
df['BP_Systolic'] = df['Blood Pressure'].str.split('/').str[0].astype(float)
df['BP_Diastolic'] = df['Blood Pressure'].str.split('/').str[1].astype(float)

# Fill missing sleep disorder
df['Sleep Disorder'] = df['Sleep Disorder'].fillna('None')

# Features for clustering
features = ['Sleep Duration', 'Quality of Sleep', 'Physical Activity Level',
            'Stress Level', 'Heart Rate', 'Daily Steps', 'BP_Systolic', 'BP_Diastolic']
X = df[features].dropna()
df_clean = df.loc[X.index].copy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ---------- KMeans ----------
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df_clean['Cluster'] = kmeans.fit_predict(X_scaled)

# PCA for 2-D projection
pca = PCA(n_components=2, random_state=42)
coords = pca.fit_transform(X_scaled)
df_clean['PC1'] = coords[:, 0]
df_clean['PC2'] = coords[:, 1]

# ---------- Summarise clusters for labels ----------
cluster_profiles = df_clean.groupby('Cluster').agg(
    sleep_q=('Quality of Sleep', 'mean'),
    stress=('Stress Level', 'mean'),
    activity=('Physical Activity Level', 'mean'),
    duration=('Sleep Duration', 'mean'),
).round(1)

cluster_labels = {}
for c, row in cluster_profiles.iterrows():
    tag_parts = []
    tag_parts.append(f"Sleep Q {row.sleep_q}")
    tag_parts.append(f"Stress {row.stress}")
    tag_parts.append(f"Activity {row.activity}")
    cluster_labels[c] = f"Cluster {c}: " + " | ".join(tag_parts)

# ---------- Plot ----------
# Colorblind-friendly palette (IBM Design Library)
palette = {0: '#648FFF', 1: '#FE6100', 2: '#785EF0', 3: '#DC267F'}
disorder_markers = {'None': 'o', 'Sleep Apnea': 's', 'Insomnia': '^'}

fig, axes = plt.subplots(1, 2, figsize=(20, 9), gridspec_kw={'width_ratios': [3, 2]})
fig.patch.set_facecolor('#FAFAFA')

# ---- Left: Main scatter ----
ax = axes[0]
ax.set_facecolor('#F5F5F5')

for disorder, marker in disorder_markers.items():
    subset = df_clean[df_clean['Sleep Disorder'] == disorder]
    for cluster in sorted(df_clean['Cluster'].unique()):
        pts = subset[subset['Cluster'] == cluster]
        if len(pts) == 0:
            continue
        ax.scatter(pts['PC1'], pts['PC2'],
                   c=palette[cluster], marker=marker,
                   s=80, alpha=0.72, edgecolors='white', linewidths=0.5)

# Cluster centroids
centroids_pca = pca.transform(kmeans.cluster_centers_)
for c in range(4):
    cx, cy = centroids_pca[c]
    ax.scatter(cx, cy, c=palette[c], s=320, marker='*',
               edgecolors='#222', linewidths=1.2, zorder=5)
    ax.annotate(f'C{c}', (cx, cy), fontsize=9, fontweight='bold',
                ha='center', va='bottom', xytext=(0, 10),
                textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=palette[c], alpha=0.9))

ax.set_xlabel('Principal Component 1', fontsize=12, fontweight='bold', labelpad=8)
ax.set_ylabel('Principal Component 2', fontsize=12, fontweight='bold', labelpad=8)
ax.set_title('Sleep Health Clusters: Lifestyle vs. Sleep Quality',
             fontsize=16, fontweight='bold', pad=14)

# Build legends
cluster_handles = [Line2D([0], [0], marker='o', color='w', markerfacecolor=palette[c],
                          markersize=10, label=cluster_labels[c]) for c in sorted(palette)]
disorder_handles = [Line2D([0], [0], marker=m, color='w', markerfacecolor='gray',
                           markersize=9, label=d) for d, m in disorder_markers.items()]
centroid_handle = [Line2D([0], [0], marker='*', color='w', markerfacecolor='#555',
                          markersize=14, label='Cluster Centroid')]

leg1 = ax.legend(handles=cluster_handles, title='Cluster Profiles',
                 loc='upper left', fontsize=7.5, title_fontsize=9,
                 framealpha=0.92, edgecolor='#ccc')
ax.add_artist(leg1)
ax.legend(handles=disorder_handles + centroid_handle, title='Sleep Disorder / Symbol',
          loc='lower left', fontsize=8.5, title_fontsize=9,
          framealpha=0.92, edgecolor='#ccc')

var_explained = pca.explained_variance_ratio_
ax.text(0.98, 0.02,
        f'PCA variance explained: {var_explained[0]:.1%} + {var_explained[1]:.1%} = {sum(var_explained[:2]):.1%}',
        transform=ax.transAxes, fontsize=8, ha='right', va='bottom',
        style='italic', color='#555')

ax.grid(True, alpha=0.3, linestyle='--')
ax.tick_params(labelsize=10)

# ---- Right: Cluster profile heatmap ----
ax2 = axes[1]
profile = df_clean.groupby('Cluster')[features].mean()
profile_norm = (profile - profile.min()) / (profile.max() - profile.min())

sns.heatmap(profile_norm.T, annot=profile.T.round(1).values, fmt='',
            cmap='YlGnBu', linewidths=1.5, linecolor='white',
            ax=ax2, cbar_kws={'label': 'Normalised Value', 'shrink': 0.8},
            annot_kws={'fontsize': 9})
ax2.set_title('Cluster Feature Profiles', fontsize=14, fontweight='bold', pad=12)
ax2.set_xlabel('Cluster', fontsize=12, fontweight='bold', labelpad=8)
ax2.set_ylabel('')
ax2.tick_params(labelsize=10)
ax2.set_yticklabels(ax2.get_yticklabels(), rotation=0)

plt.tight_layout(pad=2)
plt.savefig('output.png', dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print('Saved output.png')
