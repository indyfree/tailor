
# coding: utf-8

# In[1]:


# Display plots inline
get_ipython().run_line_magic('matplotlib', 'inline')

# Autoreload all package before excecuting a call
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[2]:


import numpy as np
import pandas as pd
import tailor
from tailor import data
from tailor import features


# In[3]:


df = data.load_csv()


# In[4]:


df = data.transform_datatypes(df)


# In[5]:


df = data.fill_missing_values(df)


# In[6]:


df = features.build_features.weeks_on_sale(df)


# In[7]:


df = features.build_features.accurate_season(df)


# In[8]:


df = data.group_by.weeks_on_sale(df)


# In[9]:


df.head(28)

