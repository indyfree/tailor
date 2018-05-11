
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


# In[2]:


import tailor.data.load_dataframe as ld


# In[3]:


data_raw = ld.load_raw_dataframe()


# In[4]:


data_raw


# In[5]:


data_raw.min()


# In[6]:


data_raw.max()


# In[7]:


data_raw.season.unique()


# In[8]:


data_raw.brand.unique()


# In[9]:


data_raw.original_price.mean()


# In[10]:


data_raw.sells_price.mean()


# In[11]:


data_raw.discount.mean()


# In[12]:


data_raw.discount.median()


# In[13]:


data_raw.markdown.mean()


# In[14]:


data_raw.markdown.median()


# In[15]:


data_raw.article_count.mean()


# In[16]:


data_raw.article_count.median()


# In[17]:


data_raw.color.unique()


# In[18]:


data_raw.color.value_counts()


# In[19]:


data_raw.brand.value_counts()


# In[20]:


data_raw.season.value_counts()


# In[23]:


np.count_nonzero(data_raw.article_id.unique())


# In[24]:


np.count_nonzero(data_raw.article_id)


# In[25]:


1131329-608555


# In[26]:


data_raw.isnull().sum()

