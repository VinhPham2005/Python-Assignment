import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('SourceCode/Problem1/results.csv', na_values= 'N/a')
drop_cols = ['Unnamed: 0', 'Player', 'Nation', 'Team', 'Pos', 'Age']
df.drop(columns=drop_cols, inplace= True)

for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].str.replace(',', '').astype(float)

missing_rate = df.isna().mean()
df = df.loc[:, missing_rate < 0.3]

df.fillna(df.mean(numeric_only= True), inplace= True)

scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

pca = PCA(n_components= 2)
df_pca = pca.fit_transform(df_scaled)

kmeans = KMeans(n_clusters= 3, random_state= 42)
labels = kmeans.fit_predict(df_pca)

plt.figure(figsize=(8, 6))
plt.scatter(df_pca[:, 0],df_pca[:, 1], c= labels, cmap= 'viridis')
plt.title('PCA for EPL 2024 - 2025 season data')
plt.savefig('SourceCode/Problem3/PCA.png')



