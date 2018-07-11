
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

# # Data Introduction

# First, we want to give an overview of the provided data.
# Therefore, we have a look at the raw dataset and 
# do some visualization for a better understanding of the data

# ## Example of raw data

# In[2]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import tailor
from tailor import data
from tailor import clustering
from tailor.visualization import *


# In[3]:


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

# In[4]:


pd.options.display.float_format = "{:.2f}".format
raw_data.describe(include=np.number)


# ## Consistency check

# ### Check if the dataset contains null values

# In[5]:


raw_data.isna().values.any()


# ### Detect how many articles are contained in the dataset

# In[6]:


len(raw_data['article_id'].unique())


# ### Get the maximum *time_on_sale* value

# In[7]:


raw_data['time_on_sale'].max()


# ### Check, how many articles have less then 182 *time_on_sale* values

# In[8]:


tos_test = pd.DataFrame(raw_data.groupby('article_id').apply(lambda x: x.time_on_sale.nunique()))
tos_test.columns = ['number_tos']
len(tos_test.loc[tos_test.number_tos < 182])


# To sum up, there are 8708 different articles in the dataset. Non of the articles have 182 *time_on_sale* values. To build consistent series, we have to fill up the lacked values of each series

# ## Visualization of raw data

# In[9]:


plot_articles(raw_data, [900001, 900002, 900030], 'article_count');
plot_articles(raw_data, [900001, 900002, 900030], 'avq');


# # Data processing

# For the next step, we process the raw data into a consistent and suitable dataset.
# Therefore, we perform the following steps:
# 
# * __Drop Invalid Rows which do not make sense (e.g. negative sells price)__
# 
# 
# * __Transform the different columns into specific datatypes:__
#   * *article_id* = category
#   * *transaction_date* = datetime
#   * *markdown_start_date* = datetime
#   * *markdown_end_date* = datetime
#   * *all other columns* with datatype object = category
#   
#   
# * __Build Features__
#   * Build a new column and calculate the weeks an article has been on sale (weeks_on_sale)
#   * Rebuild the season column with the season of the first transaction
#   
#   
# * __Group By Weeks On Sale__
#   * Replace the time_on_sale values through weeks on sale
#   * As a result, we consider every article on a weekly basis instead of a daily basis
#   
#   
# * __Fill Missing Values__
#   * As we found out before, not all articles have sales on each day for the consecutive 182 days. Therefore, we add extra rows with zero values for the missing time_on_sales values

# # Data Exploration

# Next, we want to give an overview of the processed data and illustrate our proceed. Therefore, we now have a look at the processed dataset and do some visualization and explanations for a better and deeper understanding of the data.

# ## Example of processed data

# In[17]:


processed_data = data.load_data()
processed_data


# In[11]:


processed_data.dtypes


# ## Visualization of processed data

# In[18]:


plot_articles(processed_data, [900001, 900002, 900030], 'article_count');
plot_articles(processed_data, [900001, 900002, 900030], 'avq');


# In comparison to the visualization of the raw data, you can see that the graphs no longer looks that messy. Thereby, you can get a better idea of how similar graphs are.

# ## Inter-feature-variance

# For the development of the clustering algorithm, we have to think about a criterion on which we divide the dataset into multiple pieces (cluster).
# To remember, for an optimal prediction quality, we need a population as big as possible and with a mean variation as small as possible. We want to create such a population by grouping articles with similar characteristics.
# 
# 
# Therefore, we want to split the feature with the highest variation between the individual characteristics and group the individual characteristics for a first segmentation. As from now, we will call the variation between the individual characteristics _inter-feat-variance_.
# 
# 
# Thus, we next have a look at the graphs of the individual characteristics of a feature to get an idea, how different or similar they are.

# In[13]:


plot_feature_characteristics(processed_data, 'Abteilung', 'article_count');


# In[14]:


plot_feature_characteristics(processed_data, 'color', 'article_count', legend=False);


# The first graph visualize the _inter-feat-variance_ of the feature _Abteilung_, the second one the _inter-feat-variance_ of the feature _color_.
# These plots give a valuable representation on how the _inter-feat-variance_ of the different features could looks like.
# In this example, the feature _Abteilung_ is more likely to have a high variance between the individual characteristics then the feature _color_.
