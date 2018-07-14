
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


df_raw = data.load_csv()


# In[4]:


print(df_raw.shape)
df_raw = data.drop_invalid_rows(df_raw)
df_raw.shape


# In[5]:


df = data.transform_datatypes(df_raw)


# In[6]:


df = features.build(df_raw)


# In[7]:


df = data.group_by.weeks_on_sale(df)


# In[8]:


df = data.fill_missing_values(df)


# In[9]:


test = df


# In[10]:


df = data.normalize(test)


# In[11]:


df = data.order_columns(df)


# In[12]:


df.head(20)

