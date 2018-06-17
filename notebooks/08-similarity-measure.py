
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


df = cluster(df, distance_measure=distance.euclidean, distance_target='article_count')


# In[5]:


b = df.cluster.unique()
print(sorted(b, reverse=True))


# In[6]:


cluster_scatter(df, 4, distance.euclidean, 'article_count')
plot_cluster_articles(df, 4, 'article_count', legend=False);


# In[7]:


print(cluster_scatter(df, 2, distance.euclidean, 'article_count'))
plot_cluster_articles(df, 2, 'article_count', legend=False);


# In[8]:


print(cluster_scatter(df, 0, distance.euclidean, 'article_count'))
plot_cluster_articles(df, 0, 'article_count', legend=False);


# In[9]:


plot_feature_characteristics(df, 'cluster', 'article_count');


# In[10]:


cluster_separation(df, 2, 5, distance.euclidean, 'article_count')


# In[11]:


cluster_separation(df, 2, 5, distance.euclidean, 'article_count')


# In[12]:


# davis_bouldin(df, distance.euclidean, 'article_count')


# ### Why choosing a different evaluation metric than the 'rank_features'?

# In[17]:


df = tailor.load_data()
feats = ['color', 'brand', 'Abteilung', 'WHG', 'WUG', 'season', 'month']
ranked_features = ranking.rank_features(df, distance.euclidean, feats, 'article_count')
print(ranked_features)
for feat in ranked_features.index:
    df_cluster = build_clusters(df, feat, distance.euclidean, 'article_count')
    char_to_clusters = df_cluster.loc[:, [feat, 'cluster']].groupby(feat).mean()
    result = df.merge(char_to_clusters, left_on=feat, right_on=feat)
    print(output_clusters(result, feat))
    print("DB-",feat, ":", davis_bouldin(result, distance.euclidean, 'article_count'))


# In[15]:


print(df_cluster)

