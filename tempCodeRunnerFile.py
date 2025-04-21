import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score

x, _ = make_blobs(n_samples= 300, centers= 4, cluster_std= 0.6, random_state= 24)

wcss = []
k_values = range(1, 11)

for k in k_values:
    kmeans = KMeans(n_clusters= k, random_state= 24)
    kmeans.fit(x)
    wcss.append(kmeans.inertia_)

plt.plot(k_values, wcss, 'bo-')
plt.xlabel('Số cụm k')
plt.ylabel('Wcss')
plt.show()

kmeans