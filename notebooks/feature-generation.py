
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import tailor


# In[2]:


df = tailor.load_data()


# In[3]:


df.head()


# In[5]:


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
df.head()

