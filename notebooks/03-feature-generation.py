
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import tailor


# In[2]:


df = tailor.load_data()


# In[3]:


df.head()


# In[4]:


get_ipython().run_cell_magic('time', '', '\n# expand transaction_date information\nseason = list()\nweekday = list()\nmonths = list()\n\nfor i in df.transaction_date:\n    month = i.month\n    # meteorological seasons\n    if 2 < month < 6:\n        season.append(\'spring\')\n    elif 5 < month < 9:\n        season.append("summer")\n    elif 8 < month < 12:\n        season.append("fall")\n    else:\n        season.append("winter")\n\n    months.append(month)\n    day = i.weekday()\n    weekday.append(day)\n\ndf[\'season_buy\'] = pd.Series(season, index=df.index)\ndf[\'month\'] = pd.Series(months, index=df.index)\ndf[\'weekday\'] = pd.Series(weekday, index=df.index)')


# In[5]:


get_ipython().run_cell_magic('time', '', '\n# expand transaction_date information\n\ndef get_season(month):\n    if 2 < month < 6:\n        return \'spring\'\n    elif 5 < month < 9:\n        return "summer"\n    elif 8 < month < 12:\n        return "fall"\n    else:\n        return "winter"\n\ndf[\'month\'] = df[\'transaction_date\'].apply(lambda x : x.month)\ndf[\'season_buy\'] = df[\'month\'].apply(lambda x : get_season(x))\ndf[\'weekday\'] = df[\'transaction_date\'].apply(lambda x : x.weekday())')

