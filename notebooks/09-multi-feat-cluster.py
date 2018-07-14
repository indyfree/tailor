
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
import multiprocessing as mp
import itertools

import tailor
from tailor.clustering import *


# In[3]:


data = tailor.load_data()


# In[4]:


data.sample(10)


# # Code

# In[5]:


min_cluster_size = 50
max_cluster_count = 10
clustering_feature = 'norm_article_count'


# In[6]:


get_ipython().run_cell_magic('time', '', "\nsplit_results, merge_results = cluster.multi_feature(data, distance.absolute, 'norm_article_count', min_cluster_size, max_cluster_count)")


# In[7]:


# show the available split layers/depth
split_results['Clusters'].index


# In[8]:


# showcasing how to retrieve the cluster feauteres of the first cluster of the fifth layer
split_results['Clusters']['5'][0]['Features']


# In[11]:


cluster.show_cluster_characteristics(data, merge_results, 4)


# In[12]:


cluster.show_cluster_characteristics(data, merge_results, 4, 0.75)


# In[13]:


cluster.show_cluster_characteristics(data, merge_results, 3, 0.75)


# In[14]:


cluster.show_cluster_characteristics(data, merge_results, 3)

