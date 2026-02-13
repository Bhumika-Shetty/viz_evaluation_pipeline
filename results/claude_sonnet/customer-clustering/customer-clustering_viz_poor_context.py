'''
Prompt :
The Customer Segments dataset contains marketing and customer data.
Create a visualization showing customer clusters or segments.
Provide ONLY the Python code wrapped in triple backticks.

'''

# =========================
# MANUAL FIXES APPLIED (DOCUMENTED)
# Model output issues:
#   - Used df = pd.read_csv('/mnt/user-data/uploads/customer_segments.csv') (path not valid in repo)
#   - Saved to '/mnt/user-data/outputs/customer_segments_visualization.png' (path not valid; grader requires 'output.png')
#   - Used plt.show() and did not close figure (evaluation expects saved file only)
#
# Minimal fixes (no visual/logic changes intended):
#   1) Input path portability:
#        pd.read_csv('/mnt/user-data/uploads/customer_segments.csv')  ->  pd.read_csv('data/customer_segments.csv')
#   2) Output capture for evaluation:
#        plt.savefig('/mnt/user-data/outputs/customer_segments_visualization.png', ...)  ->  plt.savefig('output.png', dpi=300, bbox_inches='tight')
#   3) Removed plt.show(), added plt.close()
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
df = pd.read_csv('data/customer_segments.csv')

# Data preprocessing
# Calculate total spending
df['TotalSpent'] = df['MntWines'] + df['MntFruits'] + df['MntMeatProducts'] + \
                   df['MntFishProducts'] + df['MntSweetProducts'] + df['MntGoldProds']

# Calculate total purchases
df['TotalPurchases'] = df['NumWebPurchases'] + df['NumCatalogPurchases'] + \
                       df['NumStorePurchases']

# Calculate customer age
df['Age'] = 2014 - df['Year_Birth']

# Fill missing Income values with median
df['Income'].fillna(df['Income'].median(), inplace=True)

# Select features for clustering
features_for_clustering = ['Income', 'TotalSpent', 'TotalPurchases', 
                          'NumWebVisitsMonth', 'Recency', 'Age']

# Prepare data for clustering
X = df[features_for_clustering].copy()
X.fillna(X.median(), inplace=True)

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Determine optimal number of clusters using elbow method
inertias = []
K_range = range(2, 11)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)

# Perform K-means clustering with optimal k=4
optimal_k = 4
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# PCA for visualization
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
df['PC1'] = X_pca[:, 0]
df['PC2'] = X_pca[:, 1]

# Create visualizations
fig = plt.figure(figsize=(20, 12))

# 1. Elbow plot
plt.subplot(2, 3, 1)
plt.plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
plt.xlabel('Number of Clusters', fontsize=12)
plt.ylabel('Inertia', fontsize=12)
plt.title('Elbow Method For Optimal K', fontsize=14, fontweight='bold')
plt.grid(alpha=0.3)

# 2. PCA scatter plot
plt.subplot(2, 3, 2)
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
for i in range(optimal_k):
    cluster_data = df[df['Cluster'] == i]
    plt.scatter(cluster_data['PC1'], cluster_data['PC2'], 
               c=colors[i], label=f'Cluster {i}', alpha=0.6, s=50)
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)', fontsize=12)
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)', fontsize=12)
plt.title('Customer Segments (PCA Visualization)', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(alpha=0.3)

# 3. Income vs Total Spent
plt.subplot(2, 3, 3)
for i in range(optimal_k):
    cluster_data = df[df['Cluster'] == i]
    plt.scatter(cluster_data['Income'], cluster_data['TotalSpent'], 
               c=colors[i], label=f'Cluster {i}', alpha=0.6, s=50)
plt.xlabel('Income', fontsize=12)
plt.ylabel('Total Spent', fontsize=12)
plt.title('Income vs Total Spending by Segment', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(alpha=0.3)

# 4. Cluster sizes
plt.subplot(2, 3, 4)
cluster_counts = df['Cluster'].value_counts().sort_index()
bars = plt.bar(range(optimal_k), cluster_counts.values, color=colors, alpha=0.7, edgecolor='black')
plt.xlabel('Cluster', fontsize=12)
plt.ylabel('Number of Customers', fontsize=12)
plt.title('Customer Distribution Across Segments', fontsize=14, fontweight='bold')
plt.xticks(range(optimal_k), [f'Cluster {i}' for i in range(optimal_k)])
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}', ha='center', va='bottom', fontsize=10)
plt.grid(axis='y', alpha=0.3)

# 5. Segment characteristics - Total Spent
plt.subplot(2, 3, 5)
segment_stats = df.groupby('Cluster')['TotalSpent'].mean().sort_index()
bars = plt.bar(range(optimal_k), segment_stats.values, color=colors, alpha=0.7, edgecolor='black')
plt.xlabel('Cluster', fontsize=12)
plt.ylabel('Average Total Spent', fontsize=12)
plt.title('Average Spending by Segment', fontsize=14, fontweight='bold')
plt.xticks(range(optimal_k), [f'Cluster {i}' for i in range(optimal_k)])
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
            f'${int(height)}', ha='center', va='bottom', fontsize=10)
plt.grid(axis='y', alpha=0.3)

# 6. Heatmap of cluster characteristics
plt.subplot(2, 3, 6)
cluster_profile = df.groupby('Cluster')[features_for_clustering].mean()
cluster_profile_normalized = (cluster_profile - cluster_profile.mean()) / cluster_profile.std()
sns.heatmap(cluster_profile_normalized.T, annot=True, fmt='.2f', cmap='RdYlGn', 
           center=0, cbar_kws={'label': 'Normalized Value'},
           xticklabels=[f'Cluster {i}' for i in range(optimal_k)])
plt.title('Segment Characteristics Profile', fontsize=14, fontweight='bold')
plt.ylabel('Features', fontsize=12)

plt.tight_layout()
plt.savefig('output.png', dpi=300, bbox_inches='tight')
plt.close()

# Print cluster summary
print("\n" + "="*80)
print("CUSTOMER SEGMENT ANALYSIS SUMMARY")
print("="*80)
for i in range(optimal_k):
    cluster_data = df[df['Cluster'] == i]
    print(f"\nCluster {i} ({len(cluster_data)} customers):")
    print(f"  Average Income: ${cluster_data['Income'].mean():.2f}")
    print(f"  Average Total Spent: ${cluster_data['TotalSpent'].mean():.2f}")
    print(f"  Average Total Purchases: {cluster_data['TotalPurchases'].mean():.2f}")
    print(f"  Average Age: {cluster_data['Age'].mean():.1f} years")
    print(f"  Average Recency: {cluster_data['Recency'].mean():.1f} days")
