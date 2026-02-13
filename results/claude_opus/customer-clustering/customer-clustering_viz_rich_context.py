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
#   - Model initially returned a visualization (image) instead of Python code, despite prompt explicitly
#     stating "Provide ONLY the Python code wrapped in triple backticks." User had to manually ask the
#     model to output the Python code.
#
# Code/execution:
#   - No path or output changes needed; code already used data/customer_segments.csv, output.png, plt.close().
# =========================



"""
Customer Segmentation Analysis Visualization
Uses PCA for dimensionality reduction and KMeans for clustering.
Generates synthetic customer data if 'data/customer_segments.csv' is not found.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score
import os
import warnings
warnings.filterwarnings('ignore')

# ──────────────────────────────────────────────
# 1. Load or Generate Data
# ──────────────────────────────────────────────
DATA_PATH = 'data/customer_segments.csv'

if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded dataset: {df.shape[0]} rows × {df.shape[1]} columns")
else:
    print("Dataset not found — generating synthetic customer data...")
    np.random.seed(42)

    segments = {
        'Budget Conscious':    dict(n=180, age=(28,6),  income=(30,8),   spend=(150,50),  frequency=(3,1.5),  tenure=(2,1),   online_pct=(70,15), satisfaction=(6.0,1.2), items=(3,1.2),  discount_use=(80,10), recency=(15,7),  support_calls=(2,1.5), loyalty_pts=(200,80),   referrals=(0.5,0.7), campaign_resp=(20,10)),
        'Premium Loyalist':    dict(n=150, age=(45,10), income=(95,20),  spend=(800,200), frequency=(8,2),    tenure=(8,3),   online_pct=(50,20), satisfaction=(8.5,0.8), items=(7,2),    discount_use=(15,10), recency=(5,3),   support_calls=(1,0.8), loyalty_pts=(2500,600), referrals=(4,1.5),   campaign_resp=(60,15)),
        'Young Digital Native': dict(n=170, age=(23,3),  income=(45,12),  spend=(350,100), frequency=(10,3),   tenure=(1.5,0.8),online_pct=(92,5),  satisfaction=(7.2,1.0), items=(5,1.5),  discount_use=(55,15), recency=(3,2),   support_calls=(0.5,0.5),loyalty_pts=(600,200), referrals=(3,1.5),   campaign_resp=(45,12)),
        'Occasional Shopper':  dict(n=160, age=(38,12), income=(60,18),  spend=(200,80),  frequency=(1.5,0.8),tenure=(4,2),   online_pct=(40,25), satisfaction=(5.5,1.5), items=(2,0.8),  discount_use=(30,20), recency=(45,20), support_calls=(1.5,1), loyalty_pts=(350,150),  referrals=(0.8,0.8), campaign_resp=(10,8)),
        'High-Value Churning':  dict(n=140, age=(35,8),  income=(80,15),  spend=(600,150), frequency=(2,1),    tenure=(5,2),   online_pct=(60,20), satisfaction=(3.5,1.2), items=(4,1.5),  discount_use=(40,15), recency=(60,25), support_calls=(5,2),   loyalty_pts=(1800,500), referrals=(1,1),     campaign_resp=(15,10)),
    }

    rows = []
    for seg_name, p in segments.items():
        for _ in range(p['n']):
            rows.append({
                'Age':                      max(18, np.random.normal(*p['age'])),
                'Annual_Income_K':          max(15, np.random.normal(*p['income'])),
                'Monthly_Spend':            max(10, np.random.normal(*p['spend'])),
                'Purchase_Frequency':       max(0.1, np.random.normal(*p['frequency'])),
                'Tenure_Years':             max(0.1, np.random.normal(*p['tenure'])),
                'Online_Purchase_Pct':      np.clip(np.random.normal(*p['online_pct']), 0, 100),
                'Satisfaction_Score':       np.clip(np.random.normal(*p['satisfaction']), 1, 10),
                'Avg_Items_Per_Order':      max(1, np.random.normal(*p['items'])),
                'Discount_Usage_Pct':       np.clip(np.random.normal(*p['discount_use']), 0, 100),
                'Days_Since_Last_Purchase': max(1, np.random.normal(*p['recency'])),
                'Support_Calls_Year':       max(0, np.random.normal(*p['support_calls'])),
                'Loyalty_Points':           max(0, np.random.normal(*p['loyalty_pts'])),
                'Referrals_Made':           max(0, np.random.normal(*p['referrals'])),
                'Campaign_Response_Pct':    np.clip(np.random.normal(*p['campaign_resp']), 0, 100),
            })

    df = pd.DataFrame(rows)
    mask = np.random.random(df.shape) < 0.02
    df = df.mask(mask)
    os.makedirs('data', exist_ok=True)
    df.to_csv(DATA_PATH, index=False)
    print(f"Generated synthetic dataset: {df.shape[0]} rows × {df.shape[1]} columns")

# ──────────────────────────────────────────────
# 2. Preprocessing
# ──────────────────────────────────────────────
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
X = df[numeric_cols].copy()

imputer = SimpleImputer(strategy='median')
X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=numeric_cols)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

# ──────────────────────────────────────────────
# 3. Determine optimal k via silhouette score
# ──────────────────────────────────────────────
sil_scores = {}
for k in range(3, 8):
    km = KMeans(n_clusters=k, n_init=15, random_state=42)
    labels = km.fit_predict(X_scaled)
    sil_scores[k] = silhouette_score(X_scaled, labels)

best_k = max(sil_scores, key=sil_scores.get)
print(f"Optimal k = {best_k} (silhouette = {sil_scores[best_k]:.3f})")

# ──────────────────────────────────────────────
# 4. Final clustering + PCA
# ──────────────────────────────────────────────
kmeans = KMeans(n_clusters=best_k, n_init=25, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_scaled)
centroids_pca = pca.transform(kmeans.cluster_centers_)

# ──────────────────────────────────────────────
# 5. Build descriptive segment labels
# ──────────────────────────────────────────────
profile = X_imputed.copy()
profile['Cluster'] = clusters
summary = profile.groupby('Cluster').mean()

segment_labels = {}
for c in range(best_k):
    row = summary.loc[c]
    traits = []
    if 'Annual_Income_K' in row.index:
        if row['Annual_Income_K'] > summary['Annual_Income_K'].quantile(0.7):
            traits.append('High-Income')
        elif row['Annual_Income_K'] < summary['Annual_Income_K'].quantile(0.3):
            traits.append('Budget')
    if 'Monthly_Spend' in row.index:
        if row['Monthly_Spend'] > summary['Monthly_Spend'].quantile(0.7):
            traits.append('Big Spenders')
        elif row['Monthly_Spend'] < summary['Monthly_Spend'].quantile(0.3):
            traits.append('Low Spend')
    if 'Purchase_Frequency' in row.index:
        if row['Purchase_Frequency'] > summary['Purchase_Frequency'].quantile(0.7):
            traits.append('Frequent')
        elif row['Purchase_Frequency'] < summary['Purchase_Frequency'].quantile(0.3):
            traits.append('Infrequent')
    if 'Online_Purchase_Pct' in row.index and row['Online_Purchase_Pct'] > 75:
        traits.append('Digital')
    if 'Satisfaction_Score' in row.index and row['Satisfaction_Score'] < 4.5:
        traits.append('At Risk')

    label = ' · '.join(traits[:3]) if traits else f'Segment {c}'
    n_members = (clusters == c).sum()
    segment_labels[c] = f"{label}\n(n={n_members})"

# ──────────────────────────────────────────────
# 6. Visualization
# ──────────────────────────────────────────────
# Colorblind-friendly palette (Wong 2011)
COLORS = ['#0077BB', '#EE7733', '#009988', '#CC3311', '#33BBEE', '#EE3377', '#BBBBBB']
palette = [COLORS[i % len(COLORS)] for i in range(best_k)]

fig, ax = plt.subplots(figsize=(14, 10), facecolor='#FAFAFA')
ax.set_facecolor('#FAFAFA')

for c in range(best_k):
    mask_c = clusters == c
    ax.scatter(
        X_pca[mask_c, 0], X_pca[mask_c, 1],
        c=palette[c], label=segment_labels[c],
        s=45, alpha=0.55, edgecolors='white', linewidth=0.3, zorder=2,
    )

for c in range(best_k):
    ax.scatter(
        centroids_pca[c, 0], centroids_pca[c, 1],
        c=palette[c], s=280, marker='D', edgecolors='#222222', linewidth=1.8, zorder=4,
    )
    short_label = segment_labels[c].split('\n')[0]
    ax.annotate(
        short_label,
        xy=(centroids_pca[c, 0], centroids_pca[c, 1]),
        xytext=(14, 14), textcoords='offset points',
        fontsize=9, fontweight='bold', color=palette[c],
        path_effects=[pe.withStroke(linewidth=3, foreground='white')],
        arrowprops=dict(arrowstyle='-', color='#888888', lw=0.8), zorder=5,
    )

var1, var2 = pca.explained_variance_ratio_[:2] * 100
ax.set_xlabel(f'Principal Component 1  ({var1:.1f}% variance)', fontsize=12, labelpad=10)
ax.set_ylabel(f'Principal Component 2  ({var2:.1f}% variance)', fontsize=12, labelpad=10)
ax.set_title('Customer Segmentation Analysis', fontsize=20, fontweight='bold', pad=20, color='#222222')
ax.text(
    0.5, 1.02,
    f'{best_k} segments via K-Means · {len(numeric_cols)} features projected with PCA '
    f'· {len(df)} customers · silhouette = {sil_scores[best_k]:.2f}',
    transform=ax.transAxes, ha='center', fontsize=10, color='#666666',
)

legend = ax.legend(
    title='Customer Segments', title_fontsize=11, fontsize=9,
    loc='upper left', frameon=True, fancybox=True, framealpha=0.92,
    edgecolor='#CCCCCC', borderpad=1, handletextpad=1, scatterpoints=1, markerscale=1.4,
)
legend.get_frame().set_facecolor('#FFFFFF')

ax.grid(True, alpha=0.25, linestyle='--', color='#AAAAAA')
ax.tick_params(colors='#555555')
for spine in ax.spines.values():
    spine.set_color('#CCCCCC')

plt.tight_layout()
plt.savefig('output.png', dpi=300, bbox_inches='tight', facecolor='#FAFAFA')
plt.close()
print("Visualization saved to output.png")
