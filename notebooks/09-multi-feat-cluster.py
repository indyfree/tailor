
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

import tailor
from tailor.clustering import *


# In[3]:


data = tailor.load_data()


# In[4]:


data.sample(10)


# # Code

# In[5]:


split_results = cluster.multi_feature_split(data, distance.euclidean, 50)


# In[6]:


split_results['Clusters'].index


# In[7]:


split_results['Clusters']['5'][0]['Features']

