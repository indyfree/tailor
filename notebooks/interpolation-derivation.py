
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.interpolate as spi
import tailor


# In[17]:


series_a = pd.Series([0,3,8,12,8,3,1], [1,2,3,4,5,6,10])


# In[3]:


series_b = pd.Series([2,24,3], [1,4,6])


# In[4]:


series_a - series_b


# In[5]:


abs(series_a - series_b)


# In[6]:


sum(abs(series_a - series_b))


# In[7]:


abs(series_a - series_b).mean()


# In[8]:


abs(series_a - series_b).sum()


# In[20]:



x = pd.Series([1,2,3,4,5,6,7])
y = series_a.copy()
s = spi.UnivariateSpline(y.index, y.values, s=1)
xs = np.linspace(y.index.min(), y.index.max(), 1000)
ys = s(xs)
ds = s.derivative()
yds = ds(xs)
plt.plot(y.index, y.values, '.-')
plt.plot(xs, ys)
plt.plot(xs, yds)

