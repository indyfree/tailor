
# coding: utf-8

# # Initialization

# In[1]:


# Display plots inline
get_ipython().run_line_magic('matplotlib', 'inline')

# Autoreload all package before excecuting a call
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[51]:


import pandas as pd
import numpy as np
import multiprocessing as mp
import itertools

import tailor
from tailor.clustering import *
from tailor.visualization import *


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


# In[10]:


multi_feature_cluster.show_cluster_characteristics(data, merge_results, 3, 0.75)


# In[9]:


multi_feature_cluster.show_cluster_characteristics(data, merge_results, 4, 0.75)


# In[57]:


multi_feature_cluster.evaluate_clustering(merge_results, 2, data)


# In[19]:


assigned_df = multi_feature_cluster.get_cluster_dataframe(merge_results, 3, data)


# In[55]:


multi_feature_cluster.evaluate_clustering(merge_results, 3, data)


# In[60]:


plot_cluster_articles(assigned_df, 1, clustering_feature, legend=False);
plot_cluster_articles(assigned_df, 10, clustering_feature, legend=False);


# In[30]:


assigned_df2 = multi_feature_cluster.get_cluster_dataframe(merge_results, 4, data)


# In[56]:


multi_feature_cluster.evaluate_clustering(merge_results, 4, data)


# In[61]:


plot_cluster_articles(assigned_df, 0, clustering_feature, legend=False);
plot_cluster_articles(assigned_df, 1, clustering_feature, legend=False);


# In[22]:


plot_feature_characteristics(assigned_df, 'cluster', clustering_feature);


# In[49]:


plot_feature_characteristics(assigned_df, 'cluster', 'article_count');


# In[32]:


plot_feature_characteristics(assigned_df2, 'cluster', clustering_feature);


# In[50]:


plot_feature_characteristics(assigned_df2, 'cluster', 'article_count');

