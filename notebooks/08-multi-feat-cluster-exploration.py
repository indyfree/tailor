
# coding: utf-8

# # Multi Feature Clustering

# ## Initialization

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


# ## Feature Selection

# ### Ranking by Euclidean

# In[5]:


feats = ['color', 'brand', 'Abteilung', 'WHG', 'WUG', 'season']
ranking.rank_features(data, distance.euclidean , feats, 'article_count')


# ### Ranking by Derivative Euclidean

# In[6]:


ranking.rank_features(data, distance.derivative_euclidean , feats, 'article_count')


# While both distance measures find 'Abteilung' the most informative first clustering feature by a large margin and 'color' the least informative, the order of the other features is quite different.

# In[7]:


dfs_abteilung = pd.Series()

uniques = data.Abteilung.unique()

feats = ['color', 'brand', 'WHG', 'WUG', 'season']

for abteilung in uniques:
    dfs_abteilung[abteilung] = data[data.Abteilung == abteilung].drop(columns='Abteilung')
    print(abteilung + ":")
    print(ranking.rank_features(dfs_abteilung[abteilung], distance.derivative_euclidean , feats, 'article_count'))
    print("")


# In[8]:


df = dfs_abteilung['Abteilung001']
df.article_id.unique()


# In[9]:


plot_feature_characteristics(df, 'WUG', 'article_count', legend=True);


# In[10]:


df_temp = df[df.WUG == 'WUG004']
df_temp.article_id.unique()


# WUG has scored high in our rank_features method for 'Abteilung001', but results in an inefficient separation as 'WUG004' only contains 1 article.

# In[11]:


df = dfs_abteilung['Abteilung002']
df.article_id.unique()


# In[12]:


plot_feature_characteristics(df, 'WUG', 'article_count', legend=False);


# 'Abteilung002' has much more WUG uniques than 'Abteilung001' and 19 times the articles. This should be taken into consideration when determining the second clustering feature.
