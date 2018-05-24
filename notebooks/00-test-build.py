
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import tailor
from tailor import data
from tailor import features


# In[2]:


df = data.load_csv()


# In[3]:


df = df.head()


# In[4]:


df = data.transform_datatypes(df)


# In[5]:


df.head()


# In[6]:


df = features.build_features.weeks_on_sale(df)


# In[7]:


df = features.build_features.date_info(df)


# In[8]:


df.head()


# In[9]:


df = features.build(df)


# In[10]:


df.head()

