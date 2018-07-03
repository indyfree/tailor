
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


# In[3]:


data = tailor.load_data()


# In[4]:


data.sample(10)


# # Code

# In[7]:


get_ipython().run_cell_magic('time', '', '\nsplit_results = cluster.multi_feature_split(data, distance.euclidean, 50)')


# In[8]:


split_results['Clusters'].index


# In[9]:


split_results['Clusters']['5'][0]['Features']


# In[10]:


# get all clusters that remained unsplit
leafs = list()

# iterate through all layers of the clustering
for layer in split_results['Clusters'].index:
    # add all layer leaves and remove leaf parents
    for add_cluster in split_results['Clusters'][layer]:
        # iterate until parent cluster is found then remove it
        for index, check_cluster in enumerate(leafs):
            if check_cluster['Name'] in add_cluster['Name']:
                # parent cluster found, remove it
                del leafs[index]
                # no more than one parent cluster, therefore exit second for loop
                break
        leafs.append(add_cluster)


# In[11]:


for cluster in leafs:
    print(cluster['Name'] + ": " + str(cluster['DataFrame']['article_id'].nunique()))


# In[12]:


len(leafs)

