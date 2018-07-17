
# coding: utf-8

# # About the Project

# ## The Customer

# The customer is a fashion retailer with numerous stores across Germany. It collected data of articles that have been on sale over a period of time and now wants to do some analysis on the basis of that data.

# ## The Task

# The fashion retailer wants to use the data for:
# 
#   * Sales volume predictions for articles 
#   * Optimal price determination of new articles on market launch
#   * Inventory calculation 
#   * General predictions and strategic decision making
# 
# 
# Such predictions need a population, which serves as a basis for statistical calculations.
# Predicting the sales of a specific article on basis of the whole assortment would be too imprecise.
# The mean variation is too high, hence the quality of the prediction would be very low.
# The amount and variety of articles allows to refer to a more representative population. For an optimal prediction quality, the population should be as big as possible and its mean variation as small as possible.
# 
# It is possible to create such a population, by grouping articles with similar characteristic attributes together. This can be realized through a clustering algorithm.

# ## The Goal

# The overall goal of the project is to develop a clustering algorithm, that provide meaningful article clusters. The algorithm should provide reasonable results and build on statistically verified methods. The special challenge of the clustering algorithm is:

# - Clusters should be characterized by article attributes (e.g. brand, color, ..)
# - Clusters should be formed according to similar behavior in number of articles sold, revenue or sales-quotas over time

# In clustering the distance (similarity) and the characterizing attributes build on the same features. This is not the case here. Thus, we can not use existing packages for categorical-, nor time-series clustering, because each would contradict one of the constraints above. A further requirement is, that each article has to be assigned to a cluster.

# # Data Introduction

# First, we want to give an overview of the provided data. Therefore, we have a look at the raw dataset and 
# do some visualization for a better understanding of the data.

# In[1]:


# TODO: Remove before export
# Display plots inline
get_ipython().run_line_magic('matplotlib', 'inline')

# Autoreload all package before excecuting a call
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[2]:


# Needed imports for the rest of the notebook
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Our developed package 'tailor'
import tailor
from tailor import data
from tailor.clustering import *
from tailor.visualization import *


# ## Example of the Raw Data

# In[3]:


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

# In[4]:


pd.options.display.float_format = "{:.2f}".format
raw_data.describe(include=np.number)


# ## Consistency Checks

# #### Check if the dataset contains null values

# In[5]:


raw_data.isna().values.any()


# We are lucky, there are no null values in the dataset!

# #### Detect how many articles are contained in the dataset

# In[6]:


len(raw_data['article_id'].unique())


# #### Get the maximum timespan the articles have been on sale

# In[7]:


raw_data['time_on_sale'].max()


# This means we will be comparing sales of articles over a course of 182 consecutive days. Counting starts at day 0.
# 

# #### Check how many articles don't have values defined for the full range of the 182 days

# In[8]:


tos = raw_data.groupby('article_id').apply(lambda x: x.time_on_sale.nunique())
len(tos[tos == 182])


# After all there are a lot of missing data, but they were hidden. We do not see a single article has data for each of the 182 days they have been on sale! This problem has to be addressed in a later step.

# ## Visualization of the Raw Data

# In[9]:


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
#   * As we found out before, not all articles have sales on each day for the consecutive 182 days. Therefore, we add extra rows with zero values for the missing *time_on_sales* values
#   
# 6. __Data normalization__
#   * Come up with it here are in a later paragraph?

# # Data Exploration

# Next, we want to give an overview of the processed data and illustrate our procedure. We will have a look at the processed dataset, do some visualizations and explanations for a better and deeper understanding of the data.

# ## Example of the Processed Data

# In[10]:


df = data.load_data()
df.head(10)


# In[11]:


df.dtypes


# ## Visualization of the Processed Data

# In[12]:


plot_articles(df, [900001, 900002, 900030], 'article_count');
plot_articles(df, [900001, 900002, 900030], 'avq');


# In comparison to the raw data, you can see that the graphs no longer looks that messy. It is easier to identify which graphs are similar. Moreover we see that we removed seasonal effects by grouping the daily sales to weeks.

# ## Inter-Feature Variance

# Remember that we want to identify a (sub-)population of similar articles that we can use for prediction or further analysis. 
# 
# For an optimal prediction quality this group has to be:
# 
# - As similar as possible (Small variance)
# - As big as possible (Large sample size)
# 
# We want to create such a group by:
# 
# 1. Splitting the population into groups where the (article-) characteristics of a feature behave differently. (E.g. blue articles are different from red articles)
# 2. Grouping (article-)characteristics together that behave similarly. (E.g. blue and grey articles are similar to each other)
# 
# Here the **feature** is *color*, and the **characteristics** are *blue*, *grey* and *red*.
# 
# To find features, where this is easily possible, we will look at the **inter-feature variance**. The **inter-feature variance** measures the variance of the characteristics within a feature. A high **inter-feature variance** indicates differently behaving characteristics.
# 
# Next, we will look at the graphs some features to get an idea, how the different characteristics are distributed.

# In[13]:


plot_feature_characteristics(df, 'Abteilung', 'norm_article_count');


# This graph visualizes the inter-feat variance of the feature 'Abteilung'. We can see that all curves are quite different from each other. That indicates that the individual characteristics should be treated individually. (Form an own cluster) 

# In[14]:


plot_feature_characteristics(df, 'color', 'norm_article_count', legend=False);


# This graph visualizes the inter-feat variance of the feature 'color'. Each curve represents the averaged sells of articles with the same color. We can see that quite a few curves in the middle look very similar, while at the top and bottom are "far away" from the others. We can assume that the similar colors-curves in the middle should be treated the same (form a cluster together) and the curves which look different should be treated individually.

# Indeed, calculating the *inter-feat variances* of the two features clearly show that 'Abteilung' has a much larger variance then 'color', thus the feature 'Abteilung' is more interesting to consider for clustering.

# In[15]:


inter_feat_variance(df, distance.absolute, 'Abteilung', 'norm_article_count')


# In[16]:


inter_feat_variance(df, distance.absolute, 'color', 'norm_article_count')


# # The Clustering Algorithm

# ## General

# The general idea of the clustering algorithm is to recursively split the article population into the characteristics of each feature. After every step, merge "similar" characteristics together to clusters. This is a way of hierarchical clustering: With each considered feature the number of clusters increases and the size of the clusters grows smaller.
# 
# 
# In the end we will have clusters that look like this:
# 
# * Level 1
#     * __Cluster 1__:  
#         * _Brand_: Adidas
# 
#     * __Cluster 2__:  
#         * _Brand_: Nike, Rebook 
# * Level 2
#     * __Cluster 1.1__:  
#         * _Brand_: Adidas
#         * _Color_: blue, red 
#     * __Cluster 1.2__:  
#         * _Brand_: Adidas
#         * _Color_: green
#     * __Cluster 2.1__:
#         * _Brand_: Nike, Rebook
#         * _Color_: red
#     * __Cluster 2.2__:  
#         * _Brand_: Nike, Rebook
#         * _Color_: blue, green
# * Level 3:
#     * __Cluster 1.1.1__:  
#         * _Brand_: Adidas
#         * _Color_: blue, red
#         * _Season_: autumn 
#     * ...
#     
# Note: The features don't have to be split the same way across all cluster. See e.g. _Cluster 1.1_ vs. _Cluster 2.1_.  The feature color has been split differently. E.g. "Red and blue Adidas shoes are similar, but red Nikes and Rebooks and not similar to blue Nikes and Rebooks"
# 
# The challenge is a) to rank the features in the best order we want to consider them (e.g. first _Brand_ then _Color_) and b) find similar behaving characteristics (e.g. blue and red Adidas are similar).

# ## Similarity Measure

# Each clustering algorithm needs to define a similarity measure, also called "distance", to cluster similar items together. In our case "similar" articles are articles, that showed similar selling behavior while being on sale in the shops of the customer. The dataset yields measures for the number of articles sold over time (*article count*) the generated *revenue* and the sales quota in comparison to the stock (_avq_, _Abverkaufsquote_). So in the use-case of our customer similar articles are the ones that have a similar curve of *revenue*, *article_count* or *avq* over time.

# #### When we look at two pairs of articles we can see that the distance is lower when the curves are closer to each other

# In[17]:


plot_articles(df, [900001, 900080], 'article_count');
a = df.loc[df.article_id == 900001].set_index('time_on_sale')['article_count']
b = df.loc[df.article_id == 900080].set_index('time_on_sale')['article_count']
print("distance: ", distance.absolute(a,b))


# In[18]:


plot_articles(df, [900001, 900050], 'article_count');
a = df.loc[df.article_id == 900001].set_index('time_on_sale')['article_count']
b = df.loc[df.article_id == 900050].set_index('time_on_sale')['article_count']
print("distance: ", distance.absolute(a,b))


# ### Normalization

# One problem remains: If we look at the at the upper graph we can see that the two curves are far apart, but they have a somehow similar shape. Here it is crucial that we __normalize__ the curves. Normalized values allow the comparison of corresponding normalized values for different observations.
# 
# We chose to normalize the article curves with the **Standardized Moment**, the process is also called **standardization**. This kind of normalization is typically a division by the *standard deviation*. This has the advantage that such normalized moments differ only in other properties than variability, which facilitates e.g. comparison of shape.

# If we look at the same articles, but plot and calculate the distance with the normalized values we can see that the 
# two articles are now much closer.The distance measure is now implicitly taking the *shape* into account, when calculating the absolute distance between the normalized values.

# In[19]:


plot_articles(df, [900001, 900050], 'norm_article_count');
a = df.loc[df.article_id == 900001].set_index('time_on_sale')['norm_article_count']
b = df.loc[df.article_id == 900050].set_index('time_on_sale')['norm_article_count']
print("distance: ", distance.absolute(a,b))


# ## Outline of the Algorithm

# Remember we are searching article groups, characterized by their attributes (color, brand, etc..) that are similar to each other. We previously defined similarity, showed the structure of the resulting clusters, and discussed the categorical as well as the time-series part of the clustering. Now we will illustrate the top-level steps the clustering algorithm actually does.
# 
# 
# ```python
# # 1. Get a list of ranked features (color, brand, etc..) 
# #    according to their inter_feature score
# features =  rank_features()
# 
# # Repeat until all features considered
# for f in features:
#     # 2. Split feature characteristics into separate clusters
#     split_features()
#    
#     # 3. Merge similar characteristics together into a cluster. Merge when the distance
#     #    between two cluster is less then a 'similarity_threshold' 
#     merge_close_clusters()
#     
#     # 4. Merge clusters that are below the min_cluster_size into the closest cluster
#     merge_min_clusters()
#     
#     # 5. When no new clusters resulted from the considered feature finish the clustering
#     #    (e.g. all new clusters were too small)
#     if no_new_clusters:
#         break
# ```
# 
# In words, we are considering every feature, ranked by its variance score. The features characteristics form a cluster, which then get merged with similar characteristics (Remember we want the clusters to be as similar as possible). The merging is going to happen more frequently towards the end of the `ranked_feature list`, since the feature characteristics are closer to another (low variance). Furthermore we are looking at the size of the clusters, and merge clusters which are too small (Remember we want the clusters to be as big as possible). The `min_cluster_size` and the `similarity_threshold` are parameters and can be set according to the customers preferences. Of course there is always a trade-of between similarity and size of a cluster.

# ## Hierarchical Component

# (Here some kind of visualization of the clustering process would be cool)

# # Results and Evaluation

# To discuss the results we will pick out an potential use-case of a customer and go through the whole clustering process. 
# 
# Assuming we are a fashion retailer and want to introduce a new special edition shoe **Breeezy 5000** into our shops. Beforehand, we want to know how much **revenue** this article is likely going to generate and how the **revenue curve** will likley look like over the course of the 26 weeks this special shoe is available in our shops. In order to let our data science team do all the prediction work, we have to give them a reference population of shoes that are similar to our special edition shoe. Luckily we have paid the smart guys from tailorit to find this reference population, by using a **cluster analysis**. The smart guys from tailorit have developed a clustering package called **tailor** which they going to use for the analysis.

# ## Define The Use Case

# Our new shoes has a few attributes, like brand and color, is of a certain Type (WUG, WHG) and will be placed in a certain compartment (Abteilung) of our shops. Moreover we want to introduce it in August.
# 
# Consequently we assume the following attributes for our the **Breeezy 5000**:
# - brand: **Hödur**
# - color: **mittelbraun**
# - Abteilung: **Abteilung005**
# - WHG: **WHG014**
# - WUG: **WUG073**
# - month: **August**
# - season: **Sommer**

# ### Set Clustering Parameters

# In[20]:


# Use standardized revenue as measure for clustering
target_value = 'norm_revenue'
min_cluster_size = 50
# We want to observe all features available
features = ['color', 'brand', 'Abteilung', 'WHG', 'WUG', 'season', 'month']
# Use absolute distance between the curves as similarity measure
distance_measure = distance.absolute


# ### Rank the Features

# In[21]:


feats = ranking.rank_features(df, distance_measure, features, target_value)
feats


# We can see here that 'WUG' is the most informative feature for us. The **inter-feature variance** is the highest, which means that the single 'WUG's are far apart from each other, thus making good cluster candidates

# ## Building First Clusters (Level 1)

# We start by building cluster using the most informative feature.

# In[61]:


# Select important feature
feat =  feats.iloc[1].feature

# Build Cluster at Level 1
c1 = build_clusters(df, feat, distance_measure, target_value)
cluster_characteristics(c1, feat)


# After first clustering step, we can see that some big clusters (0, 1, 8, 12) and several small clusters have been formed. Since we want to generate clusters, that fulfill a minimum sample size, we now need to merge clusters that fall under the `min_cluster_size` with the respective closest cluster.

# In[62]:


c1 = merge_min_clusters(c1, feat, min_cluster_size, distance.absolute, target_value)
cluster_characteristics(c1, feat)


# We can see now that only clusters above the `min_cluster_size` remain. All other clusters have been merged with neighbouring clusters.

# ### Plotting the Clusters

# Visualizing the results we can see that the mean curves of the clusters are quite different. They follow a similar trend but have different course over time.

# In[24]:


plot_feature_characteristics(c1, 'cluster', target_value);


# #### Principal Component Analysis

# Principal Component Analysis (PCA) is a common technique for feature reduction and visualization multi-dimensional data in 2D. PCA transform the data onto new "orthogonal" axis, along the axis where there is the largest variance in the original data (the revenue curve with the 26 dimensions, one for each day). Time-series data is not the main use-case for PCA, but nevertheless we can see more than 50% of the variance explained by the first two components. 
# 
# Using PCA for visualization, and plotting the individual articles for some clusters (colored) we can observe a good clustering results.

# In[98]:


plot_cluster_pca(c1, [16, 17, 37], target_value);


# ## Further Clustering (Level 2)

# The first clustering step produced clusters that are characterized by *WHG*. We can use reference population for our new shoe, by finding the cluster, which groups articles that have the same *WHG* as the **Breeezy 5000**.
# In this case its *Cluster 0*, which includes WHG014.
# 
# We further want to inspect the cluster size and variance of *Cluster 0*:

# In[90]:


print("Number of articles: %s" % cluster_characteristics(c1, feat).loc[0].num_articles)
print("Variance: %s" % cluster_variance(c1, 0, distance_measure, target_value))


# Our shoe is in quite a big cluster, where the variance is close to 1. We believe, we can find a better reference population by clustering further and looking at more features.

# ### Redefine the Article Population

# In[71]:


# We looking to Cluster 0
c2 = c1.loc[c1.cluster == 0]


# ### Cluster with the Next Feature

# In[72]:


# For simplicity we define a function for a clustering step, that executes all of the above
def cluster_step(c):
    feats = ranking.rank_features(c, distance_measure, features, target_value)
    feat =  feats.iloc[0].feature
    print("Splitting on feature '%s'." % feat)
    c = build_clusters(c, feat, distance_measure, target_value)
    c = merge_min_clusters(c, feat, min_cluster_size, distance.absolute, target_value)
    return (c, feat)


# In[73]:


c2, feat = cluster_step(c2)
cluster_characteristics(c2, feat)


# In[99]:


print("Number of Articles: %s" % cluster_characteristics(c2, feat).loc[34].num_articles)
print("Variance: %s" % cluster_variance(c2, 34, distance_measure, target_value))


# In[108]:


plot_feature_characteristics(c2, 'cluster', target_value);


# The second level clustering produced a cluster that has a lot less variance (0.66 in comparison to 0.99), while still having a decent cluster size (87). Looking at the visual output we can see that the **Cluster 34** has a distinct curve than the other clusters.

# ### Evaluation

# Through clustering on two hierarchical levels we found an article population that is above the set `min_cluster_size` and has a low variance. The articles in that cluster are similar in their selling behavior and make a good basis for further predictions or analysis. Assuming a market introduction of the **Breezy 5000** we can use this population to determine strategies for a wanted 

# # Outlook and Discussion
