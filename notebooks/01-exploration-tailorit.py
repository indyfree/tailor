
# coding: utf-8

# # Tailorit - Data Exploration

# ### Import required packages

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


# ### Load data

# In[3]:


df = tailor.load_data()
df = group_by.weeks_on_sale(df)


# ### Get an overview over the dataset
df.head(20)
# In[4]:


pd.options.display.float_format = "{:.2f}".format
df.describe(include=np.number)


# In[5]:


df.describe(include=['category'])


# ### Check for null values

# In[6]:


df.isna().values.any()


# Wow, we're in luck, there are no null values in the dataset!

# ### Plot sample article

# In[7]:


article = df.loc[df.article_id == 900003, [
    "weeks_on_sale", "article_count", "avq", "revenue", "sells_price", "original_price"]]
plt.plot(article.weeks_on_sale, article.article_count, 'blue')
plt.plot(article.weeks_on_sale, article.revenue/article.original_price, 'orange', label='revenue')
plt.plot(article.weeks_on_sale, article.avq, 'green')
plt.plot(article.weeks_on_sale, article.sells_price, 'red')
plt.xlabel('weeks on sale')
plt.legend();


# We can see the clear relationship between the amount of articles sold, it's sells price (including markdown and discounts) and the generated revenue here.
