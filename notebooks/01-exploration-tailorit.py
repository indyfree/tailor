
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


# ### Load data

# In[3]:


df = tailor.load_data()


# ### Get an overview over the dataset

# In[4]:


df.head(20)


# In[5]:


pd.options.display.float_format = "{:.2f}".format
df.describe(include=np.number)


# In[6]:


df.describe(include=['category'])


# ### Check for null values

# In[7]:


df.isna().values.any()


# Wow, we're in luck, there are no null values in the dataset!

# ### Plot sample article

# In[8]:


article = df.loc[df.article_id == 900003, ["time_on_sale", "article_count", "avq"]]
plt.plot(article.time_on_sale, article.article_count)
plt.plot(article.time_on_sale, article.avq);

