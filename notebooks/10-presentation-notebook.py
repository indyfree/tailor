
# coding: utf-8

# # About the Project

# ## The Customer

# The customer is a fashion retailer with numerous stores across Germany. It collected data of articles that have been on sale over a period of time in the stores. (More info..)

# ## The Task

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

# ## The Goal

# The overall goal of the project is to develop a clustering algorithm. This algorithm should be reasonable and statistically established. Further, the cluster building should be done on basis of revenue, article counts or sales quotas of the articles and every article has to be assigned to a cluster.

# # Data Introduction

# First, we want to give an overview of the provided data. Therefore, we have a look at the raw dataset and 
# do some visualization for a better understanding of the data.

# In[1]:


# Needed imports for the rest of the notebook
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import tailor
from tailor import data
from tailor import clustering
from tailor.visualization import *


# ## Example of the Raw Data

# In[2]:


raw_data = data.load_csv()
raw_data.head(10)


# ## Feature Overview

#   * *markdown* is constant for *article_id* and *transaction_date* between *markdown_start_date* and *markdown_end_date*
#   * *original_price* is constant for *article_id*
#   * *sells_price* is the actual price paid by the customer
#   * *sells_price*, *discount* and *markdown* are of the unit [Euro/article]
#   * *article_count* denominates the number of sold articles
#   * *discount* = *original_price* - *markdown* - *sells_price*
#   * *avq* is the current stock divided by *stock_total*

# In[3]:


pd.options.display.float_format = "{:.2f}".format
raw_data.describe(include=np.number)


# ## Consistency Checks

# __Check if the dataset contains null values__

# In[4]:


raw_data.isna().values.any()


# We are lucky, there are no null values in the dataset!

# __Detect how many articles are contained in the dataset__

# In[5]:


len(raw_data['article_id'].unique())


# __Get the maximum timespan the articles have been on sale __

# In[6]:


raw_data['time_on_sale'].max()


# This means we will be comparing sales of articles over a course of 182 consecutive days. Counting starts at day 0.
# 

# __Check how many articles don't have values defined for each of the 182 days__

# In[7]:


tos = raw_data.groupby('article_id').apply(lambda x: x.time_on_sale.nunique())
len(tos[tos == 182])


# After all there are a lot of missing data, but they are hidden! We see not a single article has data for each of the 182 days they have been on sale! This problem has to be addressed in a later step.

# ## Visualization of the Raw Data

# In[8]:


plot_articles(raw_data, [900001, 900002, 900030], 'article_count');
plot_articles(raw_data, [900001, 900002, 900030], 'avq');


# # Data Processing

# For the next step, we process the raw data into a consistent and suitable dataset.
# Therefore, we perform the following steps:
# 
# 1. __Drop invalid rows which do not make sense (e.g. negative sells price)__
# 
# 
# 2. __Transform the different columns into specific datatypes:__
#   * *article_id* = category
#   * *transaction_date* = datetime
#   * *markdown_start_date* = datetime
#   * *markdown_end_date* = datetime
#   * *all other columns* with datatype object = category
#   
#   
# 3. __Build new features__
#   * Build a new column and calculate the weeks an article has been on sale (weeks_on_sale)
#   * Rebuild the season column with the season of the first transaction
#   
#   
# 4. __Group time on sale by weeks__
#   * Replace the time_on_sale values through weeks on sale
#   * As a result, we consider every article on a weekly basis instead of a daily basis
#   
#   
# 5. __Fill missing values__
#   * As we found out before, not all articles have sales on each day for the consecutive 182 days. Therefore, we add extra rows with zero values for the missing time_on_sales values
#   
# 6. __Data normalization__
#   * Come up with it here are in a later paragraph?

# # Data Exploration

# Next, we want to give an overview of the processed data and illustrate our procedure. We will have a look at the processed dataset, do some visualizations and explanations for a better and deeper understanding of the data.

# ## Example of the Processed Data

# In[9]:


processed_data = data.load_data()
processed_data.head(26)


# In[10]:


processed_data.dtypes


# ## Visualization of the Processed Data

# In[11]:


plot_articles(processed_data, [900001, 900002, 900030], 'article_count');
plot_articles(processed_data, [900001, 900002, 900030], 'avq');


# In comparison to the raw data, you can see that the graphs no longer looks that messy. It is easier to identify which graphs are similar. Moreover we see that we removed seasonal/temporal effects by grouping on weeks.

# ## Inter-Feature Variance

# For the development of the clustering algorithm, we have to think about a criterion on which we divide the dataset into multiple pieces (clusters).
# 
# Remember that for an optimal prediction quality, we need to identify a (sub-)population that:
# 
# 1. is as big as possible (Large sample size)
# 2. has a small variance (Similar sample)
# 
# We want to create such a population by grouping articles with similar characteristics together (== build clusters).
# 
# 
# Therefore, we want to split the feature with the highest variance between the individual characteristics and group the individual characteristics for a first segmentation. As from now, we will call the variation between the individual characteristics _inter-feat-variance_. **-->Unclear**
# 
# 
# Thus, we next have a look at the graphs of the individual characteristics of a feature to get an idea, how different or similar they are.

# In[12]:


plot_feature_characteristics(processed_data, 'Abteilung', 'article_count');


# In[13]:


plot_feature_characteristics(processed_data, 'color', 'article_count', legend=False);


# The first graph visualize the _inter-feat-variance_ of the feature _Abteilung_, the second one the _inter-feat-variance_ of the feature _color_.
# These plots give a valuable representation on how the _inter-feat-variance_ of the different features could looks like.
# In this example, the feature _Abteilung_ is more likely to have a high variance between the individual characteristics then the feature _color_.
