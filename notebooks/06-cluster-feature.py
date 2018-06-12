
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


df.head()


# In[5]:


feats = ['color', 'brand', 'Abteilung', 'WHG', 'WUG', 'season']

r_feats = rank_features(df, distance.euclidean, feats, 'article_count')
print(r_feats)


# In[6]:


f = feat.index[5]
print(f)


# In[49]:


plot_feature_history(df, f, 'article_count');


# In[50]:


df_f = group_by.feature(df, f)
A5 = df_f.loc[df_f.Abteilung == 'Abteilung007'].set_index('time_on_sale')
A6 = df_f.loc[df_f.Abteilung == 'Abteilung006'].set_index('time_on_sale')
distance.euclidean(A5['article_count'],A6['article_count'])


# In[51]:


chars = df_f[f].unique()
dists = np.empty((len(chars), len(chars)))
l = []
                 
for i, x in enumerate(chars):
    x_rev = df_f.loc[df_f[f] == x].set_index('time_on_sale')
    
    for k, y in enumerate(chars):
        if y <= x:
            continue
            
        y_rev = df_f.loc[df_f[f] == y].set_index('time_on_sale')
        d = distance.euclidean(x_rev['article_count'], y_rev['article_count'])
        dists[i][k] = d
        l.append((d,x,y))

df_d = pd.DataFrame(l, columns=['distance', 'charA', 'charB'])
df_d = df_d.loc[df_d.charA != df_d.charB].sort_values(by='distance')
threshhold = df_d.distance.mean() / 2
df_t = df_d.loc[df_d.distance < threshhold]


# In[52]:


df_t

