import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

df = pd.read_csv('Problem1/results.csv', na_values= 'N/a')
df.drop(columns=['Unnamed: 0', 'Player', 'Nation', 'Team', 'Pos', 'Age', 'Min'], inplace= True)

for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].str.replace(',', '').astype(float)
df.fillna(df.mean(numeric_only= True), inplace= True)

wscc = []
k_values = range(1, 11)

for k in k_values:
    kmeans = KMeans(n_clusters= k, random_state= 42)
    kmeans.fit(df)
    wscc.append(kmeans.inertia_)

plt.plot(k_values, wscc, 'bo-')
plt.savefig('Problem3/elbow_method.png')

plt.figure()
silhouette = []

for k in range(2, 11):
    kmeans = KMeans(n_clusters= k, random_state= 42)
    label = kmeans.fit_predict(df)
    score = silhouette_score(df, label)
    silhouette.append(score)

plt.plot(range(2, 11), silhouette, 'go-')
plt.savefig('Problem3/silhouette_method.png')


