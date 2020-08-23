## Hierarchical cluster for google trends data
## Creates dendrogram, elbows diagram, silhouette diagram and heatmap

## Import required packages
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import pdist
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_samples
from sklearn.metrics import silhouette_score
from sklearn.metrics import pairwise_distances
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import os
import numpy as np
import seaborn as sns; sns.set(color_codes=True)

## Set graph specifications
from pylab import rcParams
rcParams['figure.figsize'] = 12, 9
import seaborn as sns
sns.set_style('whitegrid')

## Import and prepare google trends dataset for analysis
#Change current working directory
os.chdir('C:/Users/12407/Desktop/Education/Projects/Google_Trends')
#Read in google trends dataset
X = pd.read_csv('cluster_data.csv')
#Set index to age categories
X = X.set_index('State_Name')

## Dendrogram creation
#Transpose data set and create dendrogram
X_t = X.transpose()
c_dist = pdist(X, metric='euclidean') # computing the distance
c_link = linkage(X, metric='euclidean', method='ward') # computing the linkage
B = dendrogram(c_link,labels=(X_t.columns))
#Save dendrogram
plt.xlabel('State')
plt.ylabel('Distance Clustered On')
plt.title('State Dendrogram')
plt.savefig('dendrogram.png', format='png', bbox_inches='tight', dpi=600)
plt.close()

## Elbow plot
dendrogram_step = []
dendrogram_dist = c_link[:, 2]
dendrogram_dist = np.append([0], dendrogram_dist)
for i in range (0,len(dendrogram_dist)):
    dendrogram_step.append(i)
plt.plot(dendrogram_step,dendrogram_dist)
plt.title('Plot of Step to Distance')
plt.xlabel('Dendrogram Step')
plt.ylabel('Dendrogram Clustered On')
plt.savefig('elbows.png', format='png', bbox_inches='tight')
plt.close()

## Create silhouette diagram and calculate silhouette coefficient
#Set list of number of clusters to try out
no_of_clusters = [2, 3, 4, 5, 10, 20, 30, 40]
#Import euclidean
def cb_affinity(X):
    return pairwise_distances(X, metric='euclidean')
#Calculate and print average silhouette scores, and create and save associated charts
for no_clusters in no_of_clusters:
    fig, (ax1) = plt.subplots(1, 1)
    fig.set_size_inches(18, 7)
    ax1.set_xlim([-0.1,1])
    ax1.set_ylim([0, len(X) + (no_clusters+1)*10])
    c_link = linkage(X, metric='euclidean', method='ward')
    cluster_labels = fcluster(c_link, no_clusters, criterion="maxclust")
    silhouette_avg = silhouette_score(X, cluster_labels)
    print("For no_clusters = ", no_clusters,
        ". The average silhouette_score is: ", silhouette_avg)
    sample_silhouette_values = silhouette_samples(X, cluster_labels)
    y_lower = 10
    for i in range(no_clusters):
        ith_cluster_silhouette_values = \
            sample_silhouette_values[cluster_labels == i]
        ith_cluster_silhouette_values.sort()
        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i
        color = cm.nipy_spectral(float(i) / no_clusters)
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=color, edgecolor=color, alpha=0.7)
        if (ith_cluster_silhouette_values.size == 1):
            ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i) + ': One value' )
        else:
            ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i) )
        y_lower = y_upper + 10
    ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")
    plt.text(silhouette_avg+0.01,2,np.round_(silhouette_avg, decimals=3),fontsize=16,color="red")
    ax1.set_yticks([-0.2, 0, 0.2, 0.4, 0.6, 0.8, 1])
    plt.suptitle(("Silhouette analysis for agglomerative clustering on sample data "
                  "with no_clusters = %d" % no_clusters),
                fontsize=14, fontweight='bold')
    plt.savefig('silhouette_' + str(no_clusters) + '_clusters.png')
    plt.close()

#Create clustermap and save to file
sns.set(font_scale=0.5)
g = sns.clustermap(X, col_cluster=False, cmap="coolwarm", metric='euclidean', row_linkage=c_link)
g.savefig("heatmap.png", dpi=600)

plt.close()

