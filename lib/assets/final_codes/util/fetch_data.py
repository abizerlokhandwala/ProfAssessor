import pickle
from kmodes.kmodes import KModes
import pandas as pd
# mylist = [1,2,3,4,5,6]

# with open('list.pkl', 'wb') as f:
# 	pickle.dump(mylist, f)

default_path = '/home/abizer/BE_project/profassesor/lib/assets/final_codes/pickles5'

def get_pickle(filepath):
 with open(filepath, 'rb') as f:
  myfile = pickle.load(f)
 return myfile

def get_le_dict():
 return get_pickle(default_path+'/le_dict.pkl')

def get_techweights():
 return get_pickle(default_path+'/techweights.pkl')

def get_nontechweights():
 return get_pickle(default_path+'/nontechweights.pkl')

def get_cent_list():
 return get_pickle(default_path+'/kmodes_cc.pkl')

def get_weight_arr():
 return get_pickle(default_path+'/weights.pkl')

def get_level_weights():
 return get_pickle(default_path+'/clus_mapping.pkl')

def get_kmeans_centroids():
 return get_pickle(default_path+'/kmeans_centroids.pkl')

def get_kmeans_centroids():
 return get_pickle(default_path+'/kmeans_centroids.pkl')

def get_all_data():
 return pd.read_pickle(default_path+'/newdf.pkl')
# print(len(mynewlist[i].cost_))


# class CustomUnpickler(pickle.Unpickler):
#
#     def find_class(self, module, name):
#         if name == 'Manager':
#             from settings import Manager
#             return Manager
#         return super().find_class(module, name)
#
# pickle_data = CustomUnpickler(open('/home/saurabh/list2.pkl', 'rb')).load()
# print(pickle_data[0].cost_)
