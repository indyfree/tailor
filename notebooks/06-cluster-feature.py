
# coding: utf-8

# # Tailorit - 1 Feature Clustering

# ### Imports and jupyter settings

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


# ### Load data

# In[3]:


data = tailor.load_data()


# ### Rank features by their inter-feature variance

# In[4]:


feats = ['color', 'brand', 'Abteilung', 'WHG', 'WUG', 'season', 'month']
ranking.rank_features(data, distance.absolute, feats, 'norm_revenue')


# A high score indicates feature characteristics are far apart, and thus better for clustering.

# ### Select a feature to cluster by

# In[9]:


feat = 'WUG'
target_value = 'norm_revenue'
min_cluster_size = 50


# ### Run the Clustering Algorithm

# In[6]:


df = build_clusters(data, feat, distance.absolute, target_value)
cluster_characteristics(df, feat)


# In[10]:


df = merge_min_clusters(df, feat, min_cluster_size, distance.absolute, target_value)
cluster_characteristics(df, feat)


# ### Plot the article-count curves before and after the clustering

# In[11]:


print("Number Characteristics: ", len(df[feat].unique()))
plot_feature_characteristics(df, feat, target_value, legend=False);


# In[12]:


print("Number of Clusters: ", len(df['cluster'].unique()))
plot_feature_characteristics(df, 'cluster', target_value);


# ### Plot characteristics that are included in a specific Cluster

# In[13]:


plot_cluster_characteristics(df, 0, feat, target_value, legend=False);
plot_cluster_characteristics(df, 1, feat, target_value, legend=False);


# ### Plot all articles that are included in a Cluster

# In[14]:


plot_cluster_articles(df, 0, target_value, legend=False);
plot_cluster_articles(df, 1, target_value, legend=False);

