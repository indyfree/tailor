
# coding: utf-8

# # About the project

# ## The customer

# The customer is a fashion retailer with numerous stores. The dataset consists only of the stationary trades in Germany, summarized over all stores.

# ## Task description

# The fashion retailer want to use his data for:
# 
#   * sales volume predictions for articles 
#   * optimal price determination of new articles on market launch
#   * inventory calculation 
#   * general predictions and strategic decision making
#   
# Such predictions needs a basic population, which serve as a basis for statistical calculations.
# Predicting the sales of a specific article on basis of the whole assortment would be too imprecise.
# The mean variation is too high, hence the quality of the prediction would be very low.
# The multiplicity of articles allows to refer on a more representative population. For an optimal prediction quality, the population should be as big as possible and his mean variation as small as possible. It is possible to create such a population, by grouping articles with similar characteristic attributes to one unit. This can be realized through a clustering algorithm.

# ## Project goal

# The overall goal of the project is to develop a clustering algorithm. This algorithm should be reasonable and statistically established. Further, the cluster building should be done on basis of revenue, article counts or sales quotas of the articles and every article has to be assigned to a cluster.

# # Data exploration

# First, we want to give an overview of the provided data.
# Therefore, we have a look at the raw dataset and 
# do some visualization for a better understanding of the data

# ## Example of raw data

# In[51]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import tailor
from tailor import data
from tailor.visualization import *


# In[52]:


raw_data = data.load_csv()
raw_data.head(10)


# ## Feature overview

#   * *markdown* is constant for *article_id* and *transaction_date* between *markdown_start_date* and *markdown_end_date*
#   * *original_price* is constant for *article_id*
#   * *sells_price* is the actual price paid by the customer
#   * *sells_price*, *discount* and *markdown* are of the unit [Euro/article]
#   * *article_count* denominates the number of sold articles
#   * *discount* = *original_price* - *markdown* - *sells_price*
#   * *avq* is the current stock divided by *stock_total*

# In[53]:


pd.options.display.float_format = "{:.2f}".format
raw_data.describe(include=np.number)


# ## Consistency check

# ### Check if the dataset contains null values

# In[70]:


raw_data.isna().values.any()


# ### Detect how many articles are contained in the dataset

# In[76]:


len(raw_data['article_id'].unique())


# ### Get the maximum *time_on_sale* value

# In[77]:


raw_data['time_on_sale'].max()


# ### Check, how many articles have less then 181 *time_on_sale* values

# In[79]:


tos_test = pd.DataFrame(raw_data.groupby('article_id').apply(lambda x: x.time_on_sale.nunique()))
tos_test.columns = ['number_tos']
len(tos_test.loc[tos_test.number_tos < 181])


# To sum up, there are 8708 different articles in the dataset. Non of the articles have 181 *time_on_sale* values. To build consistent series, we have to fill up the lacked values of each series

# ## Visualization of raw data

# In[60]:


plot_articles(raw_data, [900001, 900002, 900030], 'article_count');
plot_articles(raw_data, [900001, 900002, 900030], 'avq');


# # Data processing

# For the next step, we process the raw data.
# As part of this, we transform the different columns into specific datatypes:
# 
#   * *article_id* = category
#   * *transaction_date* = datetime
#   * *markdown_start_date* = datetime
#   * *markdown_end_date* = datetime
