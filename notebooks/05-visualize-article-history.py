
# coding: utf-8

# # Tailorit - Visualizing Article History

# ### Prerequisites, Imports and Loading Data

# In[1]:


# Display plots inline
get_ipython().run_line_magic('matplotlib', 'inline')

# Autoreload all package before excecuting a call
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[2]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import tailor
from tailor.data import group_by
from tailor.visualization import *


# In[3]:


df = tailor.load_data()


# ### Visualizing the Weekly History of Articles

# We can visualize some random articles for certain measures:

# In[4]:


plot_articles(df, [900001, 900002, 900030], 'revenue');


# In[5]:


plot_articles(df, [900001, 900002, 900030], 'avq');


# In[6]:


plot_articles(df, [900001, 900002, 900030], 'article_count');


# That also allows us to group by certain (possibly clustering features) and only plot these articles:

# In[7]:


brown_fimmilena = df.loc[(df.color == 'mittelbraun') & (df.brand == 'Fimmilena') & (df.WUG == 'WUG073')]
ids = brown_fimmilena.article_id.unique()

plot_articles(brown_fimmilena, ids, 'article_count', False);


# It's also possible to plot the mean curve for the characteristics of a feature:

# In[8]:


plot_feature_characteristics(df, 'Abteilung', 'article_count');


# We can now look at a specific feature characteristic to possible identify a cluster characteristic:

# In[9]:


ids = df.loc[(df.Abteilung == 'Abteilung003', 'article_id')].unique()
plot_articles(df, ids, 'article_count', legend=False);

