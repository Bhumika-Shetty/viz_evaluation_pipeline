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
#   - Used df = pd.read_csv('/mnt/user-data/uploads/Sleep_health_and_lifestyle_dataset.csv') (path not valid in repo)
#
# Minimal fixes (no visual/logic changes intended):
#   1) Input path portability:
#        pd.read_csv('/mnt/user-data/uploads/Sleep_health_and_lifestyle_dataset.csv')  ->  pd.read_csv('data/Sleep_health_and_lifestyle_dataset.csv')
#   - No output or plt.close() changes needed; code already used output.png, plt.close().
# =========================


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Load the data
df = pd.read_csv('data/Sleep_health_and_lifestyle_dataset.csv')

# Handle missing values
df = df.dropna()

# Select features for clustering
features_for_clustering = ['Sleep Duration', 'Quality of Sleep', 'Physical Activity Level', 
                           'Stress Level', 'Heart Rate', 'Daily Steps']

# Create feature matrix
X = df[features_for_clustering].copy()

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Perform KMeans clustering
n_clusters = 4
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)

# Add cluster labels to dataframe
df['Cluster'] = clusters

# Use PCA for 2D visualization
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_scaled)

# Create the visualization
fig, ax = plt.subplots(figsize=(14, 10))

# Define colorblind-friendly palette
colors = ['#0173B2', '#DE8F05', '#029E73', '#CC78BC']

# Create scatter plot
for i in range(n_clusters):
    mask = clusters == i
    ax.scatter(X_pca[mask, 0], X_pca[mask, 1], 
              c=colors[i], label=f'Cluster {i+1}', 
              s=100, alpha=0.6, edgecolors='black', linewidth=0.5)

# Add cluster centroids
centroids_pca = pca.transform(kmeans.cluster_centers_)
ax.scatter(centroids_pca[:, 0], centroids_pca[:, 1], 
          c='red', marker='X', s=300, edgecolors='black', 
          linewidth=2, label='Centroids', zorder=5)

# Calculate cluster statistics for annotations
cluster_stats = []
for i in range(n_clusters):
    cluster_data = df[df['Cluster'] == i]
    avg_sleep_quality = cluster_data['Quality of Sleep'].mean()
    avg_stress = cluster_data['Stress Level'].mean()
    avg_sleep_duration = cluster_data['Sleep Duration'].mean()
    cluster_stats.append({
        'cluster': i+1,
        'quality': avg_sleep_quality,
        'stress': avg_stress,
        'duration': avg_sleep_duration,
        'size': len(cluster_data)
    })

# Add text box with cluster characteristics
textstr = 'Cluster Characteristics:\n'
for stats in cluster_stats:
    textstr += f"\nCluster {stats['cluster']} (n={stats['size']}):\n"
    textstr += f"  Avg Sleep Quality: {stats['quality']:.1f}\n"
    textstr += f"  Avg Stress Level: {stats['stress']:.1f}\n"
    textstr += f"  Avg Sleep Duration: {stats['duration']:.1f}h\n"

props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=9,
        verticalalignment='top', bbox=props, family='monospace')

# Labels and title
ax.set_xlabel(f'First Principal Component ({pca.explained_variance_ratio_[0]:.1%} variance)', 
             fontsize=12, fontweight='bold')
ax.set_ylabel(f'Second Principal Component ({pca.explained_variance_ratio_[1]:.1%} variance)', 
             fontsize=12, fontweight='bold')
ax.set_title('Sleep Health Clusters: Lifestyle vs. Sleep Quality', 
            fontsize=16, fontweight='bold', pad=20)

# Legend
ax.legend(loc='upper right', fontsize=10, framealpha=0.9)

# Grid
ax.grid(True, alpha=0.3, linestyle='--')

# Add note about PCA
note = f'Features used: Sleep Duration, Quality, Physical Activity, Stress, Heart Rate, Daily Steps\nPCA explains {pca.explained_variance_ratio_.sum():.1%} of total variance'
ax.text(0.5, -0.1, note, transform=ax.transAxes, 
       ha='center', fontsize=9, style='italic', color='gray')

plt.tight_layout()
plt.savefig('output.png', dpi=300, bbox_inches='tight')
plt.close()

print("Visualization saved as 'output.png'")
print(f"\nClustering Summary:")
print(f"Total samples: {len(df)}")
print(f"Number of clusters: {n_clusters}")
print(f"PCA variance explained: {pca.explained_variance_ratio_.sum():.1%}")
