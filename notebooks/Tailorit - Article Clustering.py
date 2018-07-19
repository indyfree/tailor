
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#About-the-Project" data-toc-modified-id="About-the-Project-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>About the Project</a></span><ul class="toc-item"><li><span><a href="#The-Customer" data-toc-modified-id="The-Customer-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>The Customer</a></span></li><li><span><a href="#The-Goal" data-toc-modified-id="The-Goal-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>The Goal</a></span></li></ul></li><li><span><a href="#Data-Introduction" data-toc-modified-id="Data-Introduction-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Data Introduction</a></span><ul class="toc-item"><li><span><a href="#Example-of-the-Raw-Data" data-toc-modified-id="Example-of-the-Raw-Data-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>Example of the Raw Data</a></span></li><li><span><a href="#Feature-Overview" data-toc-modified-id="Feature-Overview-2.2"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>Feature Overview</a></span></li><li><span><a href="#Consistency-Checks" data-toc-modified-id="Consistency-Checks-2.3"><span class="toc-item-num">2.3&nbsp;&nbsp;</span>Consistency Checks</a></span></li><li><span><a href="#Visualization-of-the-Raw-Data" data-toc-modified-id="Visualization-of-the-Raw-Data-2.4"><span class="toc-item-num">2.4&nbsp;&nbsp;</span>Visualization of the Raw Data</a></span></li></ul></li><li><span><a href="#Data-Processing" data-toc-modified-id="Data-Processing-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Data Processing</a></span></li><li><span><a href="#Data-Exploration" data-toc-modified-id="Data-Exploration-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Data Exploration</a></span><ul class="toc-item"><li><span><a href="#Example-of-the-Processed-Data" data-toc-modified-id="Example-of-the-Processed-Data-4.1"><span class="toc-item-num">4.1&nbsp;&nbsp;</span>Example of the Processed Data</a></span></li><li><span><a href="#Visualization-of-the-Processed-Data" data-toc-modified-id="Visualization-of-the-Processed-Data-4.2"><span class="toc-item-num">4.2&nbsp;&nbsp;</span>Visualization of the Processed Data</a></span></li></ul></li><li><span><a href="#Tailor---The-Clustering-Algorithm" data-toc-modified-id="Tailor---The-Clustering-Algorithm-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Tailor - The Clustering Algorithm</a></span><ul class="toc-item"><li><span><a href="#Inter-Feature-Variance" data-toc-modified-id="Inter-Feature-Variance-5.1"><span class="toc-item-num">5.1&nbsp;&nbsp;</span>Inter-Feature Variance</a></span></li><li><span><a href="#Similarity-Measure" data-toc-modified-id="Similarity-Measure-5.2"><span class="toc-item-num">5.2&nbsp;&nbsp;</span>Similarity Measure</a></span><ul class="toc-item"><li><span><a href="#Normalization" data-toc-modified-id="Normalization-5.2.1"><span class="toc-item-num">5.2.1&nbsp;&nbsp;</span>Normalization</a></span></li></ul></li><li><span><a href="#Overview-of-The-Algorithm" data-toc-modified-id="Overview-of-The-Algorithm-5.3"><span class="toc-item-num">5.3&nbsp;&nbsp;</span>Overview of The Algorithm</a></span><ul class="toc-item"><li><span><a href="#General-Idea" data-toc-modified-id="General-Idea-5.3.1"><span class="toc-item-num">5.3.1&nbsp;&nbsp;</span>General Idea</a></span></li><li><span><a href="#Outline" data-toc-modified-id="Outline-5.3.2"><span class="toc-item-num">5.3.2&nbsp;&nbsp;</span>Outline</a></span></li></ul></li></ul></li><li><span><a href="#Results-and-Evaluation" data-toc-modified-id="Results-and-Evaluation-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>Results and Evaluation</a></span><ul class="toc-item"><li><span><a href="#Use-Case" data-toc-modified-id="Use-Case-6.1"><span class="toc-item-num">6.1&nbsp;&nbsp;</span>Use Case</a></span></li><li><span><a href="#Clustering-Process" data-toc-modified-id="Clustering-Process-6.2"><span class="toc-item-num">6.2&nbsp;&nbsp;</span>Clustering Process</a></span><ul class="toc-item"><li><span><a href="#Setting-the-Clustering-Parameters" data-toc-modified-id="Setting-the-Clustering-Parameters-6.2.1"><span class="toc-item-num">6.2.1&nbsp;&nbsp;</span>Setting the Clustering Parameters</a></span></li><li><span><a href="#Rank-the-Features" data-toc-modified-id="Rank-the-Features-6.2.2"><span class="toc-item-num">6.2.2&nbsp;&nbsp;</span>Rank the Features</a></span></li><li><span><a href="#Building-Clusters-(Level-1)" data-toc-modified-id="Building-Clusters-(Level-1)-6.2.3"><span class="toc-item-num">6.2.3&nbsp;&nbsp;</span>Building Clusters (Level 1)</a></span></li><li><span><a href="#Visualizing-Cluster-Results" data-toc-modified-id="Visualizing-Cluster-Results-6.2.4"><span class="toc-item-num">6.2.4&nbsp;&nbsp;</span>Visualizing Cluster Results</a></span></li><li><span><a href="#Principal-Component-Analysis" data-toc-modified-id="Principal-Component-Analysis-6.2.5"><span class="toc-item-num">6.2.5&nbsp;&nbsp;</span>Principal Component Analysis</a></span></li><li><span><a href="#Cluster-Evaluation" data-toc-modified-id="Cluster-Evaluation-6.2.6"><span class="toc-item-num">6.2.6&nbsp;&nbsp;</span>Cluster Evaluation</a></span></li><li><span><a href="#Clustering-and-Evaluation-(Level-2)" data-toc-modified-id="Clustering-and-Evaluation-(Level-2)-6.2.7"><span class="toc-item-num">6.2.7&nbsp;&nbsp;</span>Clustering and Evaluation (Level 2)</a></span></li></ul></li></ul></li><li><span><a href="#Conclusion-and-Outlook" data-toc-modified-id="Conclusion-and-Outlook-7"><span class="toc-item-num">7&nbsp;&nbsp;</span>Conclusion and Outlook</a></span></li></ul></div>

# # About the Project

# ## The Customer

# The customer is a fashion retailer with numerous stores across Germany. It collected data of articles that have been on sale over a period of time.
# The customer wants to use the data for further analysis.  
# For example:
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
# It is possible to create such a population, by grouping articles with similar characteristic attributes together. Those populations can be generated through a clustering algorithm.

# ## The Goal

# The overall goal of the project is to develop a clustering algorithm, that builds meaningful article clusters. The algorithm should provide reasonable results and build on statistically verified methods. The challenges of the clustering algorithm are:

# - Clusters should be characterized by article attributes (e.g. brand, color, ..)
# - Clusters should be formed according to similar behavior in number of articles sold, revenue or sales-quotas over time

# These requirements combines the tasks of categorical and time-series clustering. Thus, we can not use existing packages for categorical-, nor time-series clustering, because each would contradict one of the constraints above. A further requirement is, that each article has to be assigned to a cluster.

# # Data Introduction

# First, we want to give an overview of the provided data. Therefore, we have a look at the raw dataset and 
# do some visualization for a better understanding of the data.

# In[1]:


# Needed imports for the rest of the notebook
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# The developed package 'tailor'
import tailor
from tailor import data
from tailor.clustering import *
from tailor.visualization import *


# ## Example of the Raw Data

# In[2]:


raw_data = data.load_csv()
raw_data.sample(3)


# ## Feature Overview

# The dataset contains the following numerical features:

#   * *markdown* is constant for *article_id* and *transaction_date* between *markdown_start_date* and *markdown_end_date*
#   * *original_price* is constant for *article_id*
#   * *sells_price* is the actual price paid by the customer
#   * *sells_price*, *discount* and *markdown* are of the unit [Euro/article]
#   * *article_count* denominates the number of sold articles
#   * *discount* = *original_price* - *markdown* - *sells_price*
#   * *avq* is the current stock divided by *stock_total*

# Date and categorical features include the following:

# In[8]:


raw_data.describe(include=np.object)


# ## Consistency Checks

# #### Check if the dataset contains null values

# In[4]:


raw_data.isna().values.any()


# We can observe that there are no null values in the dataset.

# #### Detect how many articles are contained in the dataset

# In[5]:


len(raw_data['article_id'].unique())


# #### Get the maximum timespan the articles have been on sale

# In[6]:


raw_data['time_on_sale'].max()


# This means we will be comparing sales of articles over a course of 182 consecutive days (counting starts at day 0). 
# 

# #### Check how many articles don't have values defined for the full range of the 182 days

# In[7]:


tos = raw_data.groupby('article_id').apply(lambda x: x.time_on_sale.nunique())
len(tos[tos == 182])


# After all there are a lot of missing data points, but they were hidden. We do not see a single article has data for each of the 182 days they have been on sale! This problem has to be addressed in a later step.

# ## Visualization of the Raw Data

# In[8]:


plot_articles(raw_data, [900001, 900002, 900030], 'article_count')
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
#   
# 6. __Data normalization__
#   * Since we want to be able to compare the shape of graphs as well as the values we need to add columns with normalized values. The exact procedure will be explained later on

# # Data Exploration

# Next, we want to give an overview of the processed data and illustrate our procedure. We will have a look at the processed dataset, do some visualizations and explanations for a better and deeper understanding of the data.

# ## Example of the Processed Data

# In[9]:


df.sample(3)


# ## Visualization of the Processed Data

# In[10]:


plot_articles(df, [900001, 900002, 900030], 'article_count')
plot_articles(df, [900001, 900002, 900030], 'avq');


# In comparison to the raw data, you can see that the graphs no longer looks that messy. It is easier to identify which graphs are similar. Moreover we see that we removed seasonal effects by grouping the daily sales to weeks.

# # Tailor - The Clustering Algorithm

# ## Inter-Feature Variance

# Remember that we want to identify a (sub-)population of similar articles that we can use for prediction or further analysis. 
# 
# For an optimal prediction quality this group has to be:
# 
# - As similar as possible (small variance)
# - As big as possible (large sample size)
# 
# We want to create such a group by:
# 
# 1. Splitting the population into groups where the (article-) characteristics of a feature behave differently. (e.g. blue articles are different from red articles)
# 2. Grouping (article-)characteristics together that behave similarly. (e.g. blue and grey articles are similar to each other)
# 
# Here the **feature** is *color*, and the **characteristics** are *blue*, *grey* and *red*.
# 
# To find features, where this is easily possible, we will look at the **inter-feature variance**. The **inter-feature variance** measures the variance of the characteristics within a feature. A high **inter-feature variance** indicates differently behaving characteristics.
# 
# Next, we will look at the graphs of some features to get an idea, how the different characteristics are distributed.

# In[11]:


plot_feature_characteristics(df, 'Abteilung', 'norm_article_count');


# This graph visualizes the inter-feat variance of the feature 'Abteilung'. We can see that all curves are quite different from each other. That indicates that the characteristics should be treated individually. Therefore, building cluster out of these characteristics produces better populations.

# In[12]:


plot_feature_characteristics(df, 'color', 'norm_article_count', legend=False);


# This graph visualizes the inter-feat variance of the feature 'color'. Each curve represents the averaged sells of articles with the same color. The curves in the middle look very similar, while the ones at the top and bottom are "far away" from the others. We can assume that the similar colors-curves in the middle should be treated the same (form a cluster together) and the curves which look different should be treated individually.

# Indeed, calculating the *inter-feat variances* of the two features clearly show that 'Abteilung' has a much larger variance then 'color', thus the feature 'Abteilung' is more interesting to consider for clustering.

# In[13]:


inter_feat_variance(df, distance.absolute, 'Abteilung', 'norm_article_count')


# In[14]:


inter_feat_variance(df, distance.absolute, 'color', 'norm_article_count')


# ## Similarity Measure

# Each clustering algorithm needs to define a similarity measure, also called "distance", to cluster similar items together. In our case "similar" articles are articles, that showed similar selling behavior. The dataset yields measures for the number of articles sold over time (*article count*) the generated *revenue* and the sales quota in comparison to the stock (_avq_, _Abverkaufsquote_). So in the use-case of our customer similar articles are the ones that have a similar curve of *revenue*, *article_count* or *avq* over time.  

# When we look at two pairs of articles we can see that the distance is lower when the curves are closer to each other

# In[15]:


plot_articles(df, [900001, 900080], 'article_count')
a = df.loc[df.article_id == 900001].set_index('time_on_sale')['article_count']
b = df.loc[df.article_id == 900080].set_index('time_on_sale')['article_count']
print("distance: ", distance.absolute(a, b))


# In[16]:


plot_articles(df, [900001, 900050], 'article_count')
a = df.loc[df.article_id == 900001].set_index('time_on_sale')['article_count']
b = df.loc[df.article_id == 900050].set_index('time_on_sale')['article_count']
print("distance: ", distance.absolute(a, b))


# ### Normalization

# One problem remains: If we look at the at the upper graph we can see that the two curves are far apart, but they have a similar shape. Here it is crucial that we __normalize__ the curves. Normalized values allow the comparison of corresponding normalized values for different observations.
# 
# We chose to normalize the article curves by **standardization**. This kind of normalization is typically a division by the *standard deviation*. This has the advantage that standardized values differ only in other properties than variability, which facilitates the comparisons of curve shapes.

# If we plot and calculate the distance with the normalized values the two articles are now much closer. The distance measure is now implicitly taking the *shape* into account, when calculating the absolute distance between the normalized values.

# In[17]:


plot_articles(df, [900001, 900050], 'norm_article_count')
a = df.loc[df.article_id == 900001].set_index(
    'time_on_sale')['norm_article_count']
b = df.loc[df.article_id == 900050].set_index(
    'time_on_sale')['norm_article_count']
print("distance: ", distance.absolute(a, b))


# ## Overview of The Algorithm

# ### General Idea

# The general idea of the clustering algorithm is to split the article population into the characteristics of each feature. Afterwards "similar" characteristics are merged together to clusters. These clusters can then be split by a different feature. This is hierarchical clustering: With each considered feature the number of clusters increases and the size of the clusters decreases.
# 
# 
# The resulting clusters will look like this:
# 
# * Level 1
#     * __Cluster 1__:  
#         * _Brand_: Adidas
#     * __Cluster 2__:  
#         * _Brand_: Nike, Rebook 
#         
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
#         
# * Level 3:
#     * __Cluster 1.1.1__:  
#         * _Brand_: Adidas
#         * _Color_: blue, red
#         * _Season_: autumn 
#     * ...
#     
# **Note:** The features don't have to be split the same way across all cluster. See e.g. _Cluster 1.1_ vs. _Cluster 2.1_.  The feature color has been split differently. E.g. "Red and blue Adidas shoes are similar, but red Nikes and Rebooks are not similar to blue Nikes and Rebooks"
# 
# The challenge is a) to rank the features in the best order we want to consider them (e.g. first _Brand_ then _Color_) and b) find similar behaving characteristics (e.g. blue and red Adidas are similar).

# ### Outline

# Remember we are searching article groups, characterized by their attributes (color, brand, etc..) that are similar to each other. We previously defined similarity, showed the structure of the resulting clusters, and discussed the categorical as well as the time-series part of the clustering. Now we will illustrate the top-level steps the clustering algorithm actually does.
# 
# ```python
# # 1. Get a list of ranked features (color, brand, etc..) 
# #    according to their inter_feature score
# features =  rank_features()
# # Repeat until all features considered
#  for f in features:
#     # 2. Split feature characteristics into separate clusters
#     split_features()
#     # 3. Merge similar characteristics together into a cluster. Merge when the distance
#     #    between two cluster is less then a 'similarity_threshold' 
#     merge_close_clusters()
#     # 4. Merge clusters that are below the min_cluster_size into the closest cluster
#     merge_min_clusters()
#     # 5. When no new clusters resulted from the considered feature finish the clustering
#     #    (e.g. all new clusters were too small)
#     if no_new_clusters:
#         break
# 
#  ```
# In words, we are considering every feature, ranked by its variance score. The features characteristics form a cluster, which get merged with similar characteristics (We want the clusters to be as similar as possible). The merging is going to happen more frequently towards the end of the `ranked_feature list`, since the feature characteristics are closer to another (low variance). Furthermore we are looking at the size of the clusters, and merge clusters which are too small (Remember we want the clusters to be as big as possible). The `min_cluster_size` and the `target_value` are parameters and can be set according to the customers preferences. Of course there is always a trade-of between similarity and size of a cluster.

# # Results and Evaluation

# ## Use Case

# To make the clustering process more tangible, we are constructing a use case on which bases we perform the cluster analysis.
# 
# Assuming the fashion retailer wants to introduce a new special edition shoe, the **Breeezy 5000**. Beforehand, the customer wants to analyze possible sales behaviors and determine a successful market introduction strategy. More specifically the retailer is interested how the new shoes **revenue** behavior will look like.
# 
# 
# We assume the following attributes for our **Breeezy 5000**:
# 
# - brand: **Hödur**
# - color: **mittelbraun**
# - Abteilung: **Abteilung005**
# - WHG: **WHG014**
# - WUG: **WUG084**
# - month: **July**
# - season: **Sommer**

# ## Clustering Process

# ### Setting the Clustering Parameters

# In[18]:


# Use standardized article count as measure for clustering
target_value = 'norm_revenue'
min_cluster_size = 50
# We want to observe all features available
features = ['color', 'brand', 'Abteilung', 'WHG', 'WUG', 'season', 'month']
# Use absolute distance between the curves as similarity measure
distance_measure = distance.absolute


# ### Rank the Features

# As mentioned in the clustering outline, we have to find a feature, that we can use for the first step of clustering.

# In[19]:


feats = ranking.rank_features(df, distance_measure, features, target_value)
feats


# We can see here *WUG* is the most informative feature. The **inter-feature variance** is the highest, which means that the single *WUG*'s are far apart from each other, thus making good cluster candidates.

# ### Building Clusters (Level 1)

# We start building clusters using the feature *WUG*.

# In[20]:


# Select most important feature
feat = feats.iloc[0].feature
c1 = build_clusters(df, feat, distance_measure, target_value)


# In[21]:


cluster_characteristics(c1, feat)


# After first clustering step, we can see that some big clusters (0, 1, 12, ...) and several small clusters have been formed. Since we want to generate clusters, that fulfill a minimum sample size, we now need to merge clusters that fall under the `min_cluster_size` with the respective closest cluster.

# In[22]:


c1 = merge_min_clusters(c1, feat, min_cluster_size,
                        distance.absolute, target_value)


# In[23]:


cluster_characteristics(c1, feat)


# We can see now that only clusters above the `min_cluster_size` remain. All other clusters have been merged with neighboring clusters. Additionally, the time needed for the merging is negligible compared to the initial clustering step. 

# ### Visualizing Cluster Results

# Visualizing the results we can see that the mean curves of the clusters are quite different. They follow a similar trend but have different course over time.

# In[24]:


plot_feature_characteristics(c1, 'cluster', target_value);


# ### Principal Component Analysis

# Principal Component Analysis (PCA) is a common technique for feature reduction and visualization of multi-dimensional data in 2D. PCA transform the data onto new "orthogonal" axis, along the axis where there is the largest variance in the original data (the revenue curve with the 26 dimensions, one for each day). Time-series data is not the main use-case for PCA, but nevertheless we can see more than 50% of the variance explained by the first two components. 
# 
# Using PCA for visualization, we can see that some of the clusters are overlapping. This indicates that further clustering may be needed. However, there are also relatively distinct clusters observable (e.g. Cluster 43) after the first step, which provides validation to our method.

# In[26]:


plot_cluster_pca(c1, [43, 36, 64], target_value);


# ### Cluster Evaluation

# The first clustering step produced clusters that are characterized by *WHG*. 
# 
# The *Cluster 5* represents a reference population for the **Breeezy 5000**. *Cluster 5* includes amongst others, articles with `WHG = WUG084`, to which the **Breeezy 5000** belongs to.
# 
# We further want to inspect the cluster size and variance of *Cluster 5*:

# In[48]:


cluster = 5
print("Number of articles: %s" %
      cluster_characteristics(c1, feat).loc[cluster].num_articles)
print("Variance: %s" % cluster_variance(c1, cluster, distance_measure, target_value))


# Our shoe is in a relatively large cluster (795 articles), which has a variance slightly above 0.5. We believe that we can find a better reference population by performing a second clustering step.

# ### Clustering and Evaluation (Level 2)

# In[39]:


# For simplicity we define a function for a clustering step
def cluster_step(c):
    feats = ranking.rank_features(c, distance_measure, features, target_value)
    feat = feats.iloc[0].feature
    print("Splitting on feature '%s'." % feat)
    c = build_clusters(c, feat, distance_measure, target_value)
    c = merge_min_clusters(c, feat, min_cluster_size,
                           distance.absolute, target_value)
    return (c, feat)


# In[49]:


# Select Cluster 0 from previous level
c2 = c1.loc[c1.cluster == 5]
c2, feat = cluster_step(c2)


# In[50]:


cluster_characteristics(c2, feat)


# The corresponding cluster for the Breeezy 5000 is **Cluster 4**. The desired release *month* of the shoe, **July**, has been clustered in that cluster. 

# In[51]:


plot_feature_characteristics(c2, 'cluster', target_value);


# In[54]:


cluster = 4
print("Number of Articles: %s" %
      cluster_characteristics(c2, feat).loc[cluster].num_articles)
print("Variance: %s" % cluster_variance(
    c2, cluster, distance_measure, target_value))


# The 2nd level clustering for Cluster 5 produced a cluster (**Cluster 4**) that has a lot less variance (0.21 in comparison to 0.53), while still having a decent cluster size (149). Looking at the visual output we can see that the Cluster 4 has a distinct curve when compared to the other clusters. Cluster 4 represents a valid reference population for the **Breeezy 5000**.

# # Conclusion and Outlook

# In the course of this project we developed a clustering algorithm that takes provided sales data as input and generates fitting reference populations for a set of articles. We developed a Python package called *tailor*, which offers functionality to automatically:
# 
# 1. Clean and process data
# 2. Explore and visualize the data
# 3. Run the clustering algorithm on different hierarchical levels
# 4. Evaluate and visualize the results
# 
# Further, the package has been designed to be easily extensible to provide extra functionality or customize the algorithm to a customers needs. In particular methods can be provided that:
# 
# - Use more sophisticated distance measures, e.g.:
#     - Kullback-Leibler divergence
#     - Dynamic-Time-Warping
# - Use a different feature ranking heuristic, e.g.:
#     - Taking the intra-feature variance into account
# - Implement further evaluation techniques, e.g.:
#     - Robustness tests, by classifying articles by their cluster labels
#     - Asses cluster separation, by t-testing the clusters centroids
#     
# In conclusion, we can provide satisfactory results with the current state of the algorithm. Shortcomings can be addressed by providing the mentioned methods. Further limitations can be solved by analyzing a larger dataset, the provided data tracked article data only for 26 weeks.
