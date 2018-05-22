
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import tailor
from tailor import data


# In[2]:


df = data.load_csv()


# In[3]:


df.head()


# In[4]:


df = data.transform_datatypes(df)


# In[5]:


df.head()


# In[6]:


from tailor import features


# In[7]:


df = features.build_features.weeks_on_sale(df)


# In[8]:


df = features.build_features.expand_date_info(df)


# In[9]:


df.head()


# In[10]:


df = tailor.load_data()


# In[11]:


df.head()

