
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
from tailor.visualization import *


# In[3]:


df = tailor.load_data()


# In[4]:


feats = ['color', 'brand', 'Abteilung', 'WHG', 'WUG', 'season', 'month']
ranked_features = ranking.rank_features(df, distance.euclidean, feats, 'article_count')
print(ranked_features)
feat = 'Abteilung'


# In[5]:


get_ipython().run_cell_magic('time', '', "df_cluster = build_clusters(df, feat, distance.euclidean, 'article_count')\ncharacteristic_clusters = df_cluster.loc[:, [feat, 'cluster']].groupby(feat).mean()\ndf = df.merge(characteristic_clusters, left_on=feat, right_on=feat)\nprint(output_clusters(df, feat))")


# In[6]:


print("Number Characteristics: ", len(df[feat].unique()))
plot_feature_characteristics(df, feat, 'article_count', legend=True);


# In[7]:


print("Number Clusters: ", len(df_cluster['cluster'].unique()))
plot_feature_characteristics(df, 'cluster', 'article_count');


# ### Plot characteristics that are included in a specific Cluster

# In[8]:


plot_cluster_characteristics(df, 1, feat, 'article_count', legend=True);


# ### Plot articles that are included in a Cluster

# In[9]:


plot_cluster_articles(df, 2, 'article_count', legend=False);


# ## Todo: 
# - Cluster/Characteristics that are not defined for the full time on sale values
