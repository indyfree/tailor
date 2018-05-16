
# coding: utf-8

# In[1]:


import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tailor.data.load_dataframe as ld


# In[2]:


data_raw = ld.load_raw_dataframe()


# In[3]:


data_raw.head()


# In[4]:


# checking whether there are any NaN cells
data_raw.isnull().sum()


# In[5]:


data_raw.min()


# In[6]:


data_raw.max()


# In[7]:


# checking whether article_id unique count matches with min max values
np.count_nonzero(data_raw.article_id.unique())


# In[8]:


# describe() is pretty useless for transaction_date, markdown_start_date, markdown_end_date


# In[9]:


# change float format for better readability, without it describe() shows x.xxxxxxxxxe+xx
pd.options.display.float_format = "{:.2f}".format
# the 50% of the describe output is the median
data_raw.original_price.describe()


# In[10]:


data_raw.sells_price.describe()


# In[11]:


data_raw.discount.describe()


# In[12]:


data_raw.markdown.describe()


# In[13]:


data_raw.article_count.describe()


# In[14]:


data_raw.revenue.describe()


# In[15]:


# there are some really ridiculous outliers here
data_raw.stock_total.describe()


# In[16]:


# max value of this is above 100%, probably an accumulated rounding error, but still there
data_raw.avq.describe()


# In[17]:


data_raw.time_on_sale.describe()


# In[18]:


data_raw.season.unique()


# In[19]:


data_raw.season.value_counts()


# In[20]:


data_raw.brand.unique()


# In[21]:


data_raw.brand.value_counts()


# In[22]:


data_raw.color.unique()


# In[23]:


data_raw.color.value_counts()


# In[24]:


sorted(data_raw.Abteilung.unique())


# In[25]:


sorted(data_raw.WHG.unique())


# In[26]:


data_raw.WHG.value_counts()


# In[27]:


sorted(data_raw.WUG.unique())


# In[28]:


data_raw.WUG.value_counts()

