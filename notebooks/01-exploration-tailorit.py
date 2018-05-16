
# coding: utf-8

# # Tailorit - Data Exploration

# ### Import required packages

# In[42]:


# Display plots inline
get_ipython().run_line_magic('matplotlib', 'inline')

# Autoreload all package before excecuting a call
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[43]:


import numpy as np
import pandas as pd

import tailor


# ### Load data

# In[65]:


df = tailor.load_data()


# ### Get an overview over the dataset

# In[46]:


df.head(20)


# In[72]:


pd.options.display.float_format = "{:.2f}".format
df.describe(include=np.number)


# In[68]:


df.describe(include=['category'])


# ### Check for null values

# In[71]:


df.isna().values.any()


# Wow, we're in luck, there are no null values in the dataset!
