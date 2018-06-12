
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
from tailor.clustering import rank_features
from tailor.clustering import distance
from tailor.data import group_by
from tailor.visualization import plot_article_history, plot_feature_history


# In[3]:


df = tailor.load_data()


# In[4]:


feats = ['color', 'brand', 'Abteilung', 'WHG', 'WUG', 'season']

r_feats = rank_features(df, distance.euclidean, feats, 'article_count')
print(r_feats)


# In[5]:


feat = r_feats.index[0]
print(feat)
plot_feature_history(df, feat, 'article_count');


# In[6]:


df_f = group_by.feature(df, feat)
df_f


# ### Each characteristic forms a cluster

# In[7]:


df_f['cluster'] = df_f[feat].cat.codes


# In[8]:


plot_feature_history(df_f, 'cluster', 'article_count');


# ### Calculate distance between clusters

# In[9]:


def cluster_distances(df, distance_target):
    cluster = df_f.cluster.unique()
    l = []
    for i, x in enumerate(cluster):
        x_curve = df_f.loc[df_f.cluster == x].set_index('time_on_sale')

        for k, y in enumerate(cluster):
            if k <= i:
                continue

            y_curve = df_f.loc[df_f.cluster == y].set_index('time_on_sale')
            d = distance.euclidean(
                x_curve[distance_target], y_curve[distance_target])
            l.append((x, y, d))

    return pd.DataFrame(l, columns=['from', 'to','cluster_distance'])

distances = cluster_distances(df_f, 'article_count')


# ### Find out characteristics to cluster together

# In[10]:


# Fix threshold value
threshold = distances.cluster_distance.mean()/2
print(threshold)
df_t = distances.loc[distances.cluster_distance < threshold]
df_t


# In[11]:


to_cluster = df_t.loc[df_t.cluster_distance == df_t.cluster_distance.min()]


# In[12]:


plot_feature_history(df_f, 'cluster', 'article_count');


# ### Reassign characteristic cluster

# In[13]:


df_f.loc[df_f.cluster == to_cluster['to'].values[0], 'cluster'] = to_cluster['from'].values[0]


# In[14]:


df_c = group_by.feature(df_f, 'cluster')


# In[15]:


plot_feature_history(df_c, 'cluster', 'article_count');


# In[16]:


distances = cluster_distances(df_f, 'article_count')
# Fix threshold value
threshold = distances.cluster_distance.mean()/2
print(threshold)
df_t = distances.loc[distances.cluster_distance < threshold]
df_t

