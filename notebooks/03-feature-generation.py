
# coding: utf-8

# # Feature Generation and Timing

# ## Initialization

# In[1]:


import numpy as np
import pandas as pd
from tailor import data


# In[2]:


df = data.load_csv()


# In[3]:


# because we need to have datetime category for transaction_date
df = data.transform_datatypes(df)


# In[4]:


df.head()


# ## Date Information Expansion and Method Comparison

# ### timing on big scale

# In[5]:


get_ipython().run_cell_magic('time', '', '\n# expand transaction_date information\nseason = list()\nweekday = list()\nmonths = list()\n\nfor i in df.transaction_date:\n    month = i.month\n    # meteorological seasons\n    if 2 < month < 6:\n        season.append(\'spring\')\n    elif 5 < month < 9:\n        season.append("summer")\n    elif 8 < month < 12:\n        season.append("fall")\n    else:\n        season.append("winter")\n\n    months.append(month)\n    day = i.weekday()\n    weekday.append(day)\n\ndf[\'season_buy\'] = pd.Series(season, index=df.index)\ndf[\'month\'] = pd.Series(months, index=df.index)\ndf[\'weekday\'] = pd.Series(weekday, index=df.index)')


# In[6]:


get_ipython().run_cell_magic('time', '', '\n# expand transaction_date information\n\n\ndef get_season(month):\n    if 2 < month < 6:\n        return \'spring\'\n    elif 5 < month < 9:\n        return "summer"\n    elif 8 < month < 12:\n        return "fall"\n    else:\n        return "winter"\n\n\ndf[\'month\'] = df[\'transaction_date\'].apply(lambda x: x.month)\ndf[\'season_buy\'] = df[\'month\'].apply(lambda x: get_season(x))\ndf[\'weekday\'] = df[\'transaction_date\'].apply(lambda x: x.weekday())')


# ### timing on small scale

# In[7]:


df = df.head()


# In[8]:


get_ipython().run_cell_magic('time', '', '\n# expand transaction_date information\nseason = list()\nweekday = list()\nmonths = list()\n\nfor i in df.transaction_date:\n    month = i.month\n    # meteorological seasons\n    if 2 < month < 6:\n        season.append(\'spring\')\n    elif 5 < month < 9:\n        season.append("summer")\n    elif 8 < month < 12:\n        season.append("fall")\n    else:\n        season.append("winter")\n\n    months.append(month)\n    day = i.weekday()\n    weekday.append(day)\n\ndf[\'season_buy\'] = pd.Series(season, index=df.index)\ndf[\'month\'] = pd.Series(months, index=df.index)\ndf[\'weekday\'] = pd.Series(weekday, index=df.index)')


# In[9]:


get_ipython().run_cell_magic('time', '', '\n# expand transaction_date information\n\n\ndef get_season(month):\n    if 2 < month < 6:\n        return \'spring\'\n    elif 5 < month < 9:\n        return "summer"\n    elif 8 < month < 12:\n        return "fall"\n    else:\n        return "winter"\n\n\ndf[\'month\'] = df[\'transaction_date\'].apply(lambda x: x.month)\ndf[\'season_buy\'] = df[\'month\'].apply(lambda x: get_season(x))\ndf[\'weekday\'] = df[\'transaction_date\'].apply(lambda x: x.weekday())')

