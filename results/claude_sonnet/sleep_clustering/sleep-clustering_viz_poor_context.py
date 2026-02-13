'''
Prompt :
The Sleep Health and Lifestyle dataset contains health and lifestyle data.
Create a visualization showing clusters or groupings within the sleep data.
Provide ONLY the Python code wrapped in triple backticks.

'''

# =========================
# MANUAL FIXES APPLIED (DOCUMENTED)
# Model output issues:
#   - Used df = pd.read_csv('/mnt/user-data/uploads/Sleep_health_and_lifestyle_dataset.csv') (path not valid in repo)
#   - Saved to '/mnt/user-data/outputs/sleep_clusters_visualization.png' (path not valid; grader requires 'output.png')
#   - Used plt.show() and did not close figure (evaluation expects saved file only)
#
# Minimal fixes (no visual/logic changes intended):
#   1) Input path portability:
#        pd.read_csv('/mnt/user-data/uploads/Sleep_health_and_lifestyle_dataset.csv')  ->  pd.read_csv('data/Sleep_health_and_lifestyle_dataset.csv')
#   2) Output capture for evaluation:
#        plt.savefig('/mnt/user-data/outputs/sleep_clusters_visualization.png', ...)  ->  plt.savefig('output.png', dpi=300, bbox_inches='tight')
#   3) Removed plt.show(), added plt.close()
# =========================


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Load the dataset
df = pd.read_csv('data/Sleep_health_and_lifestyle_dataset.csv')

# Display basic info
print("Dataset shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())
print("\nFirst few rows:")
print(df.head())
print("\nData types:")
print(df.dtypes)
print("\nMissing values:")
print(df.isnull().sum())

# Select numerical features for clustering
numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
print("\nNumerical columns:", numerical_cols)

# Prepare data for clustering (select relevant features)
# Common sleep-related features to look for
potential_features = ['Sleep Duration', 'Quality of Sleep', 'Physical Activity Level', 
                     'Stress Level', 'Heart Rate', 'Daily Steps']

# Use available numerical columns
cluster_features = [col for col in potential_features if col in df.columns]
if not cluster_features:
    cluster_features = numerical_cols[:min(5, len(numerical_cols))]

print(f"\nUsing features for clustering: {cluster_features}")

# Remove rows with missing values in selected features
df_clean = df[cluster_features].dropna()

# Standardize the features
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df_clean)

# Determine optimal number of clusters using elbow method
inertias = []
K_range = range(2, 11)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(scaled_data)
    inertias.append(kmeans.inertia_)

# Perform K-means clustering with optimal k (let's use 3-4 clusters)
optimal_k = 4
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
clusters = kmeans.fit_predict(scaled_data)

# Add cluster labels to dataframe
df_clean['Cluster'] = clusters

# Use PCA for 2D visualization
pca = PCA(n_components=2)
pca_data = pca.fit_transform(scaled_data)

# Create visualization
fig = plt.figure(figsize=(18, 12))

# 1. Elbow plot
plt.subplot(2, 3, 1)
plt.plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
plt.xlabel('Number of Clusters (k)', fontsize=12)
plt.ylabel('Inertia', fontsize=12)
plt.title('Elbow Method for Optimal k', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)

# 2. PCA scatter plot with clusters
plt.subplot(2, 3, 2)
scatter = plt.scatter(pca_data[:, 0], pca_data[:, 1], c=clusters, 
                     cmap='viridis', s=50, alpha=0.6, edgecolors='black', linewidth=0.5)
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)', fontsize=12)
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)', fontsize=12)
plt.title('Sleep Data Clusters (PCA Projection)', fontsize=14, fontweight='bold')
plt.colorbar(scatter, label='Cluster')
plt.grid(True, alpha=0.3)

# 3. Cluster distribution
plt.subplot(2, 3, 3)
cluster_counts = pd.Series(clusters).value_counts().sort_index()
bars = plt.bar(cluster_counts.index, cluster_counts.values, color='skyblue', edgecolor='black')
plt.xlabel('Cluster', fontsize=12)
plt.ylabel('Number of Individuals', fontsize=12)
plt.title('Distribution of Individuals Across Clusters', fontsize=14, fontweight='bold')
plt.xticks(cluster_counts.index)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}', ha='center', va='bottom', fontsize=10)

# 4-6. Feature comparison across clusters (box plots)
for idx, feature in enumerate(cluster_features[:3], start=4):
    plt.subplot(2, 3, idx)
    df_clean.boxplot(column=feature, by='Cluster', ax=plt.gca())
    plt.xlabel('Cluster', fontsize=12)
    plt.ylabel(feature, fontsize=12)
    plt.title(f'{feature} by Cluster', fontsize=12, fontweight='bold')
    plt.suptitle('')

plt.tight_layout()
plt.savefig('output.png', dpi=300, bbox_inches='tight')
plt.close()
print("\nVisualization saved to: output.png")

# Print cluster statistics
print("\n" + "="*60)
print("CLUSTER ANALYSIS SUMMARY")
print("="*60)
for i in range(optimal_k):
    print(f"\nCluster {i} (n={sum(clusters == i)}):")
    cluster_data = df_clean[df_clean['Cluster'] == i][cluster_features]
    print(cluster_data.mean().to_string())
