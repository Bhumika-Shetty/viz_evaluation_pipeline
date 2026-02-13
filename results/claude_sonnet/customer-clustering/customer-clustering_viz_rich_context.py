'''
Prompt (Rich Context):
You are an expert data scientist and visualization specialist.
Dataset: Customer Segments (data/customer_segments.csv); marketing data with demographic, behavioral, purchasing features.
Technical: Load from data/customer_segments.csv, save as output.png (DPI 300), use matplotlib/seaborn/plotly.
Task: Create a visualization showing customer clusters or segments; use PCA/t-SNE for 2D, color encoding, title "Customer Segmentation Analysis".
Provide ONLY the Python code wrapped in triple backticks.

'''

# =========================
# MANUAL FIXES APPLIED (DOCUMENTED)
# Model output issues:
#   - Used df = pd.read_csv('/mnt/user-data/uploads/customer_segments.csv') (path not valid in repo)
#   - Saved to '/mnt/user-data/outputs/output.png' (path not valid in repo; grader expects 'output.png' in cwd)
#   - Used plt.show() and did not close figure (evaluation expects saved file only)
#
# Minimal fixes (no visual/logic changes intended):
#   1) Input path portability:
#        pd.read_csv('/mnt/user-data/uploads/customer_segments.csv')  ->  pd.read_csv('data/customer_segments.csv')
#   2) Output capture for evaluation:
#        plt.savefig('/mnt/user-data/outputs/output.png', ...)  ->  plt.savefig('output.png', dpi=300, bbox_inches='tight')
#   3) Removed plt.show(), added plt.close()
# =========================


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

# Load the data
df = pd.read_csv('data/customer_segments.csv')

# Display basic info
print("Dataset shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())
print("\nFirst few rows:")
print(df.head())
print("\nMissing values:")
print(df.isnull().sum())
print("\nData types:")
print(df.dtypes)

# Select numerical features for clustering
numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
print("\nNumerical columns:", numerical_cols)

# Prepare data for clustering
X = df[numerical_cols].copy()

# Handle missing values using mean imputation
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

# Determine optimal number of clusters using elbow method
inertias = []
K_range = range(2, 11)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)

# Use 4 clusters as default (common for customer segmentation)
n_clusters = 4
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)

# Apply PCA for dimensionality reduction to 2D
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_scaled)

# Create the visualization
fig, ax = plt.subplots(figsize=(12, 8))

# Use colorblind-friendly palette
colors = ['#0173B2', '#DE8F05', '#029E73', '#CC78BC']

# Plot each cluster
for i in range(n_clusters):
    mask = clusters == i
    ax.scatter(X_pca[mask, 0], X_pca[mask, 1], 
              c=colors[i], 
              label=f'Segment {i+1}',
              alpha=0.6, 
              s=100,
              edgecolors='white',
              linewidth=0.5)

# Plot cluster centroids
centroids_pca = pca.transform(kmeans.cluster_centers_)
ax.scatter(centroids_pca[:, 0], centroids_pca[:, 1],
          c='black', 
          marker='X', 
          s=300, 
          edgecolors='white',
          linewidth=2,
          label='Centroids',
          zorder=5)

# Add annotations for centroids
for i, (x, y) in enumerate(centroids_pca):
    ax.annotate(f'C{i+1}', 
               xy=(x, y), 
               xytext=(10, 10),
               textcoords='offset points',
               fontsize=10,
               fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black', alpha=0.7))

# Formatting
ax.set_xlabel(f'First Principal Component ({pca.explained_variance_ratio_[0]:.1%} variance)', 
             fontsize=12, fontweight='bold')
ax.set_ylabel(f'Second Principal Component ({pca.explained_variance_ratio_[1]:.1%} variance)', 
             fontsize=12, fontweight='bold')
ax.set_title('Customer Segmentation Analysis', fontsize=16, fontweight='bold', pad=20)
ax.legend(loc='best', frameon=True, shadow=True, fontsize=10)
ax.grid(True, alpha=0.3, linestyle='--')

# Add text box with cluster information
total_variance = pca.explained_variance_ratio_[:2].sum()
textstr = f'Total variance explained: {total_variance:.1%}\nNumber of segments: {n_clusters}\nTotal customers: {len(df):,}'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=9,
        verticalalignment='top', bbox=props)

plt.tight_layout()

# Save the figure
plt.savefig('output.png', dpi=300, bbox_inches='tight')
print(f"\nVisualization saved as 'output.png'")
print(f"Cluster distribution: {np.bincount(clusters)}")

plt.close()
