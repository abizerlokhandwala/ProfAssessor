import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import scipy
from sklearn.preprocessing import LabelEncoder
from kmodes.kmodes import KModes
from collections import defaultdict
from util import fetch_data
import math

FINAL_CLUSTER_MAPPING = fetch_data.get_level_weights()

kmeans_centroids = fetch_data.get_kmeans_centroids()


def get_ind_levels(all_membership_values):
  final_levels = []
  for i in range(0, len(all_membership_values[0])):
    temp_level = []
    for j in range(0, len(all_membership_values)):
      all_membership_values[j] = np.array(all_membership_values[j])
      temp = []
      for k in range(0, len(all_membership_values[j][i])):
        temp.append((float(FINAL_CLUSTER_MAPPING[j][k]))*(float(all_membership_values[j][i][k])))
      temp = np.sum(temp).tolist()
      temp_level.append(temp)
    final_levels.append(temp_level)

  return(final_levels[0])


def apply_kmeans(scaled_levels):
  temp = 0
  distance_min = 1000000000000
  min_cluster_index = -1

  for i in range(0, len(kmeans_centroids)):
    temp = 0
    for j in range(0, len(kmeans_centroids[0])):
      temp += (scaled_levels[j]-kmeans_centroids[i][j])**2
    temp = temp**(0.5)
    if(temp<distance_min):
      min_cluster_index = i
      distance_min = temp

  return distance_min, min_cluster_index
