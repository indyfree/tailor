
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


# ## Comparison

# ### timing on big scale

# In[5]:


get_ipython().run_line_magic('', 'time')

# expand transaction_date information
season = list()
weekday = list()
months = list()

for i in df.transaction_date:
    month = i.month
    # meteorological seasons
    if 2 < month < 6:
        season.append('spring')
    elif 5 < month < 9:
        season.append("summer")
    elif 8 < month < 12:
        season.append("fall")
    else:
        season.append("winter")

    months.append(month)
    day = i.weekday()
    weekday.append(day)

df['season_buy'] = pd.Series(season, index=df.index)
df['month'] = pd.Series(months, index=df.index)
df['weekday'] = pd.Series(weekday, index=df.index)


# In[6]:


get_ipython().run_line_magic('', 'time')

# expand transaction_date information


def get_season(month):
    if 2 < month < 6:
        return 'spring'
    elif 5 < month < 9:
        return "summer"
    elif 8 < month < 12:
        return "fall"
    else:
        return "winter"


df['month'] = df['transaction_date'].apply(lambda x: x.month)
df['season_buy'] = df['month'].apply(lambda x: get_season(x))
df['weekday'] = df['transaction_date'].apply(lambda x: x.weekday())


# ### timing on small scale

# In[7]:


df = df.head()


# In[8]:


get_ipython().run_line_magic('', 'time')

# expand transaction_date information
season = list()
weekday = list()
months = list()

for i in df.transaction_date:
    month = i.month
    # meteorological seasons
    if 2 < month < 6:
        season.append('spring')
    elif 5 < month < 9:
        season.append("summer")
    elif 8 < month < 12:
        season.append("fall")
    else:
        season.append("winter")

    months.append(month)
    day = i.weekday()
    weekday.append(day)

df['season_buy'] = pd.Series(season, index=df.index)
df['month'] = pd.Series(months, index=df.index)
df['weekday'] = pd.Series(weekday, index=df.index)


# In[9]:


get_ipython().run_line_magic('', 'time')

# expand transaction_date information


def get_season(month):
    if 2 < month < 6:
        return 'spring'
    elif 5 < month < 9:
        return "summer"
    elif 8 < month < 12:
        return "fall"
    else:
        return "winter"


df['month'] = df['transaction_date'].apply(lambda x: x.month)
df['season_buy'] = df['month'].apply(lambda x: get_season(x))
df['weekday'] = df['transaction_date'].apply(lambda x: x.weekday())

