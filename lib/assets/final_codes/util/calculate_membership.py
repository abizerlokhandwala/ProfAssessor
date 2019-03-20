import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import scipy
from sklearn.preprocessing import LabelEncoder
from kmodes.kmodes import KModes
from collections import defaultdict
from util import fetch_data
import math


kmodes_centroids_list_all = fetch_data.get_cent_list()
weights = fetch_data.get_weight_arr()
is_bin = 2

def calc_membership_2(attribute_index, df_dummy, returnInd, returnAll, power):
    centroids = kmodes_centroids_list_all[attribute_index]
#     print(centroids)

#     df_dummy.astype(float)
    data_list = df_dummy.values.tolist()
    data_list = np.array(data_list, dtype=np.float64)

    data_list_length = 1
#     data_list_length = len(data_list)

#     print("Calculating distance between: centroid: ", centroids, " and point ", data_list)
#     print("data type: ", type(data_list[0][3]), "   :   centroid type: ", type(centroids[0][3]), " length of centroid: ",  len(centroids[0]))
#     print((data_list[0]))
#     print(len(centroids[0]))
#     print(len(weights[0]))
    temp_dist = 0
    distance = []
#     for temp in range(0, len(data_list)):
#       distance[temp] = []

#     distance.append([])
    for i in range (0, data_list_length):
#       print("Calculating distance between: centroid: ", centroids, " and point ", data_list[i])
#       print("weights used: ", weights[attribute_index])
      temp_dist = 0
      temp_row = []
      for j in range(0, len(centroids)):
        temp_dist = 0
        for k in range(0, len(centroids[j])):

          num = 1
          if is_bin == 0:
            if k==0:
              num = 100
          elif is_bin == 2:
              if (k==0) | (k == 1):
                num = 100
          temptemp_dist = temp_dist
          temp_dist += abs((((centroids[j][k]-(data_list[i][k]/num))/num)*weights[attribute_index][k])**power)
#           print("before  temp: ", temptemp_dist, " after temp: ", temp_dist, " = ((", centroids[j][k], "-", data_list[i][k]/num, ")/", num, "*", weights[attribute_index][k], "^", power)
#         print("temp_distance: ", temp_dist)
        temp_dist = temp_dist**(1/power)
        temp_row.append(temp_dist)

#       print("TEMP ROW: ", temp_row)

#       temp_row_sum = 0
#       temp_row_min = min(temp_row)
#       for l in range(0, len(temp_row)):
#         temp_row_sum += temp_row[l]
#       temp_row[:] = [temp_row_sum/x for x in temp_row]
#       temp_row[:] = [ '%.2f' % elem for elem in temp_row ]

      belong = []
      #calculate belongingness of a point with respect to each cluster
      for i in range(0, len(temp_row)):
        temp_belong = 0
        for j in range(0, len(temp_row)):
            temp_belong += (temp_row[i]/temp_row[j])
        belong.append(1/temp_belong)
#       print("BELONG: ", belong)
      belong = [1 if math.isnan(x) else x for x in belong]
      belong[:] = [ '%.2f' % elem for elem in belong ]
      distance.append(belong)

    if (not returnInd) and ( not returnAll):
      for i in range(0, data_list_length):
        if ((dfemail.iloc[i])["Email Address"]) in knowset:
          print((dfemail.iloc[i])["Email Address"]," : ",distance[i])

    if returnInd:
      return distance[0]

    if returnAll:
      return distance
