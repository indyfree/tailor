
# coding: utf-8

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
from tailor.clustering import ranking
from tailor.visualization import *


# In[3]:


df = tailor.load_data()


# In[4]:


feats = ['color', 'brand', 'Abteilung', 'WHG', 'WUG', 'season', 'month']
ranked_features = ranking.rank_features(df, distance.euclidean, feats, 'article_count')
print(ranked_features)
feat = 'brand'


# In[5]:


get_ipython().run_cell_magic('time', '', "df_cluster = build_clusters(df, feat, distance.euclidean, 'article_count')")


# In[9]:


print("Number Characteristics: ", len(df[feat].unique()))
plot_feature_history(df, feat, 'article_count', False);


# In[7]:


print("Number Cluster: ", len(df_cluster['cluster'].unique()))
plot_feature_history(df_cluster, 'cluster', 'article_count');


# ### Plot characteristics that are included in a Cluster

# In[8]:


plot_feature_history(df_cluster.loc[df_cluster.cluster == 0], feat, 'article_count', False);


# ## Todo: 
# - Cluster/Characteristics that are not defined for the full time on sale values
# - Visualize inside cluster
# - Merge cluster-assignment with big df to be able to cluster with multiple features
