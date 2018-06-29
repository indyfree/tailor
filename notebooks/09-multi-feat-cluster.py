
# coding: utf-8

# # Initialization

# In[1]:


# Display plots inline
get_ipython().run_line_magic('matplotlib', 'inline')

# Autoreload all package before excecuting a call
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[2]:


import pandas as pd
import numpy as np

import tailor
from tailor.clustering import *
from tailor.visualization import *


# In[3]:


data = tailor.load_data()


# In[4]:


data.sample(10)


# # Code

# In[5]:


feats = ['color', 'brand', 'Abteilung', 'WHG', 'WUG', 'season']
ranking.rank_features(data, distance.euclidean , feats, 'article_count').index[0]


# In[6]:


min_cluster_size = 10

split_number = 0
split_possible = True

# this will contain the whole hierarchical top-down clustering
split_results = pd.Series()
# this will contain all the clusters in an array with the split_number as index
split_results['Clusters'] = pd.Series()
# this will contain all the clusters' split features in an array with the split_number as index
split_results['Features'] = pd.Series()

# this is the data structure used for all clusters
first_cluster = pd.Series()
# this only contains the cluster's articles, all split clusteres will use splines of this
first_cluster['DataFrame'] = data.copy()
# this contains the features and characteristics used for the cluster
first_cluster['Features'] = pd.Series()
# the name will be defined in a manner that the hierarchy of the clustering will become clear
first_cluster['Name'] = "0"


# In[7]:


# initializing the 0 split
# adding the base cluster
split_results['Clusters'][str(split_number)] = list()
split_results['Clusters'][str(split_number)].append(first_cluster)

# determining the feature the cluster should be split by
split_feature = ranking.rank_features(first_cluster['DataFrame'], distance.euclidean , feats, 'article_count').index[0]
# the split_feature is entered in the unsplit layer
split_results['Features'][str(split_number)] = list()
split_results['Features'][str(split_number)].append(split_feature)


# In[8]:


get_ipython().run_cell_magic('time', '', '\nwhile (split_possible):\n    split_possible = False\n    for position, cluster in enumerate(split_results[\'Clusters\'][str(split_number)]):\n        if (cluster[\'DataFrame\'][\'article_id\'].nunique() > min_cluster_size):\n            if (split_possible == False):\n                split_possible = True\n            # retrieving the feature to split the cluster\n            split_feature = split_results[\'Features\'][str(split_number)][position]\n            # retrieving the values the cluster will be split into\n            feature_uniques = cluster[\'DataFrame\'][split_feature].unique()\n            \n            df = cluster[\'DataFrame\']\n            # generating the new split layer\n            new_layer = split_number + 1\n            split_results[\'Clusters\'][str(new_layer)] = list()\n            split_results[\'Features\'][str(new_layer)] = list()\n            \n            for position, characteristic in enumerate(feature_uniques):\n                # create new cluster\n                new_cluster = pd.Series()\n                # select the relevant part of the dataframe\n                new_cluster[\'DataFrame\'] = df[df[split_feature] == characteristic].drop(columns=[split_feature])\n                # copy the features from the parent cluster\n                new_cluster[\'Features\'] = cluster[\'Features\'].copy()\n                # add the split feature to it\n                new_cluster[\'Features\'][split_feature] = characteristic\n                # name the cluster\n                new_cluster[\'Name\'] = cluster[\'Name\'] + "_" + str(position + 1)\n                \n                # retrieve the features relevant for clustering\n                rank_features = new_cluster[\'DataFrame\'].select_dtypes(include=[\'category\']).drop(columns=[\'article_id\']).columns.values\n                # determine the feature the new cluster will be split by\n                new_split_feature = ranking.rank_features(new_cluster[\'DataFrame\'], distance.euclidean , rank_features, \'article_count\').index[0]\n                \n                # add the cluster to the split_results\n                split_results[\'Clusters\'][str(new_layer)].append(new_cluster)\n                split_results[\'Features\'][str(new_layer)].append(new_split_feature)\n            \n            \n    split_number += 1')


# In[9]:


print(split_results['Clusters']['0'])


# In[10]:


print(split_results['Features']['1'])


# In[11]:


print(split_results['Clusters'].index)


# In[12]:


print(split_results['Clusters']['4'])


# In[13]:


print(split_results['Clusters']['4'][0]['Features'])


# In[14]:


split_results['Clusters']['3'][0]['DataFrame']

