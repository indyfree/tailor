
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


# In[237]:


multi_feature_cluster.show_cluster_characteristics(data, merge_results, 4, 0.75)


# In[10]:


multi_feature_cluster.show_cluster_characteristics(data, merge_results, 3, 0.75)


# In[243]:


def evaluate_cluster(df):
    # characteristic - percentage dictionary
    c_p = pd.Series()

    for col in df.select_dtypes(include=['category']):
        if "article_id" not in col:
            for characteristic in df[col].unique():
                query_string = str(col) + " == " + '"' + str(characteristic) + '"'
                temp_df = df.query(query_string)
                temp_nunique = temp_df['article_id'].nunique()
                temp_percentage = temp_nunique / data.query(query_string)['article_id'].nunique()
                c_p[characteristic] = temp_percentage

    df_temp = df.copy().select_dtypes(include=['category']).drop_duplicates()
    df_temp = df_temp.reset_index(drop=True)
    df_percentages = pd.DataFrame(index = range(len(df_temp.index)), columns=df_temp.columns)
    
    for i, article in df_temp.iterrows():
        for col in df_temp.columns:
            if "article_id" not in col:
                characteristic = df_temp[col][i]
                df_percentages.at[i, col] = c_p[characteristic]
                df_percentages.at[i, 'article_id'] = df_temp['article_id'][i]
    
    percentage_matrix = df_percentages.drop(columns='article_id').values
    percentage_sum = 0.0
    for row in percentage_matrix:
        percentage_sum += row.max()
    return percentage_sum / len(percentage_matrix)


# In[244]:


evaluate_cluster(merge_results['DataFrames']['2'][1])


# In[247]:


def evaluate_clustering(merge_results, layer):
    # cluster - evaluation dictionary
    c_e = pd.Series(index=range(len(merge_results['DataFrames'][str(layer)])))
    for i, df in enumerate(merge_results['DataFrames'][str(layer)]):
        c_e[i] = evaluate_cluster(df)
        
    return c_e


# In[249]:


evaluate_clustering(merge_results, 3)


# In[250]:


evaluate_clustering(merge_results, 4)

