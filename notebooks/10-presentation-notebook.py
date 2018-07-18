
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#About-the-Project" data-toc-modified-id="About-the-Project-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>About the Project</a></span><ul class="toc-item"><li><span><a href="#The-Customer" data-toc-modified-id="The-Customer-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>The Customer</a></span></li><li><span><a href="#The-Task" data-toc-modified-id="The-Task-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>The Task</a></span></li><li><span><a href="#The-Goal" data-toc-modified-id="The-Goal-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>The Goal</a></span></li></ul></li><li><span><a href="#Data-Introduction" data-toc-modified-id="Data-Introduction-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Data Introduction</a></span><ul class="toc-item"><li><span><a href="#Example-of-the-Raw-Data" data-toc-modified-id="Example-of-the-Raw-Data-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>Example of the Raw Data</a></span></li><li><span><a href="#Feature-Overview" data-toc-modified-id="Feature-Overview-2.2"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>Feature Overview</a></span></li><li><span><a href="#Consistency-Checks" data-toc-modified-id="Consistency-Checks-2.3"><span class="toc-item-num">2.3&nbsp;&nbsp;</span>Consistency Checks</a></span></li><li><span><a href="#Visualization-of-the-Raw-Data" data-toc-modified-id="Visualization-of-the-Raw-Data-2.4"><span class="toc-item-num">2.4&nbsp;&nbsp;</span>Visualization of the Raw Data</a></span></li></ul></li><li><span><a href="#Data-Processing" data-toc-modified-id="Data-Processing-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Data Processing</a></span></li><li><span><a href="#Data-Exploration" data-toc-modified-id="Data-Exploration-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Data Exploration</a></span><ul class="toc-item"><li><span><a href="#Example-of-the-Processed-Data" data-toc-modified-id="Example-of-the-Processed-Data-4.1"><span class="toc-item-num">4.1&nbsp;&nbsp;</span>Example of the Processed Data</a></span></li><li><span><a href="#Visualization-of-the-Processed-Data" data-toc-modified-id="Visualization-of-the-Processed-Data-4.2"><span class="toc-item-num">4.2&nbsp;&nbsp;</span>Visualization of the Processed Data</a></span></li></ul></li><li><span><a href="#The-Clustering-Algorithm" data-toc-modified-id="The-Clustering-Algorithm-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>The Clustering Algorithm</a></span><ul class="toc-item"><li><span><a href="#Inter-Feature-Variance" data-toc-modified-id="Inter-Feature-Variance-5.1"><span class="toc-item-num">5.1&nbsp;&nbsp;</span>Inter-Feature Variance</a></span></li><li><span><a href="#Similarity-Measure" data-toc-modified-id="Similarity-Measure-5.2"><span class="toc-item-num">5.2&nbsp;&nbsp;</span>Similarity Measure</a></span><ul class="toc-item"><li><span><a href="#Normalization" data-toc-modified-id="Normalization-5.2.1"><span class="toc-item-num">5.2.1&nbsp;&nbsp;</span>Normalization</a></span></li></ul></li><li><span><a href="#The-First-Idea" data-toc-modified-id="The-First-Idea-5.3"><span class="toc-item-num">5.3&nbsp;&nbsp;</span>The First Idea</a></span><ul class="toc-item"><li><span><a href="#Outline-of-the-Algorithm" data-toc-modified-id="Outline-of-the-Algorithm-5.3.1"><span class="toc-item-num">5.3.1&nbsp;&nbsp;</span>Outline of the Algorithm</a></span></li><li><span><a href="#Plotting-the-Clusters" data-toc-modified-id="Plotting-the-Clusters-5.3.2"><span class="toc-item-num">5.3.2&nbsp;&nbsp;</span>Plotting the Clusters</a></span></li></ul></li><li><span><a href="#The-Second-Approach" data-toc-modified-id="The-Second-Approach-5.4"><span class="toc-item-num">5.4&nbsp;&nbsp;</span>The Second Approach</a></span></li></ul></li><li><span><a href="#Outlook" data-toc-modified-id="Outlook-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>Outlook</a></span></li></ul></div>

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

# In[10]:


df = data.load_data()
df.head(10)


# In[11]:


df.dtypes


# ## Visualization of the Processed Data

# In[12]:


plot_articles(df, [900001, 900002, 900030], 'article_count')
plot_articles(df, [900001, 900002, 900030], 'avq');


# In comparison to the raw data, you can see that the graphs no longer looks that messy. It is easier to identify which graphs are similar. Moreover we see that we removed seasonal effects by grouping the daily sales to weeks.

# # The Clustering Algorithm

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


# ## Similarity Measure

# Each clustering algorithm needs to define a similarity measure, also called "distance", to cluster similar items together. In our case "similar" articles are articles, that showed similar selling behavior while being on sale in the shops of the customer. The dataset yields measures for the number of articles sold over time (*article count*) the generated *revenue* and the sales quota in comparison to the stock (_avq_, _Abverkaufsquote_). So in the use-case of our customer similar articles are the ones that have a similar curve of *revenue*, *article_count* or *avq* over time.  

# When we look at two pairs of articles we can see that the distance is lower when the curves are closer to each other

# In[17]:


plot_articles(df, [900001, 900080], 'article_count')
a = df.loc[df.article_id == 900001].set_index('time_on_sale')['article_count']
b = df.loc[df.article_id == 900080].set_index('time_on_sale')['article_count']
print("distance: ", distance.absolute(a, b))


# In[18]:


plot_articles(df, [900001, 900050], 'article_count')
a = df.loc[df.article_id == 900001].set_index('time_on_sale')['article_count']
b = df.loc[df.article_id == 900050].set_index('time_on_sale')['article_count']
print("distance: ", distance.absolute(a, b))


# ### Normalization

# One problem remains: If we look at the at the upper graph we can see that the two curves are far apart, but they have a somehow similar shape. Here it is crucial that we __normalize__ the curves. Normalized values allow the comparison of corresponding normalized values for different observations.
# 
# We chose to normalize the article curves with the **Standardized Moment**, the process is also called **standardization**. This kind of normalization is typically a division by the *standard deviation*. This has the advantage that such normalized moments differ only in other properties than variability, which facilitates e.g. comparison of shape.

# If we look at the same articles, but plot and calculate the distance with the normalized values we can see that the 
# two articles are now much closer.The distance measure is now implicitly taking the *shape* into account, when calculating the absolute distance between the normalized values.

# In[19]:


plot_articles(df, [900001, 900050], 'norm_article_count')
a = df.loc[df.article_id == 900001].set_index(
    'time_on_sale')['norm_article_count']
b = df.loc[df.article_id == 900050].set_index(
    'time_on_sale')['norm_article_count']
print("distance: ", distance.absolute(a, b))


# ## The First Idea

# The general idea of the clustering algorithm is to split the article population into the characteristics of each feature. Afterwards "similar" characteristics are merged together to clusters. These clusters can then be split by a different feature. This is a way of hierarchical clustering: With each considered feature the number of clusters increases and the size of the clusters diminishes.
# 
# 
# In the end we will have clusters that look similar to this:
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
# Note: The features don't have to be split the same way across all cluster. See e.g. _Cluster 1.1_ vs. _Cluster 2.1_.  The feature color has been split differently. E.g. "Red and blue Adidas shoes are similar, but red Nikes and Rebooks are not similar to blue Nikes and Rebooks"
# 
# The challenge is a) to rank the features in the best order we want to consider them (e.g. first _Brand_ then _Color_) and b) find similar behaving characteristics (e.g. blue and red Adidas are similar).

# ### Outline of the Algorithm

# #### Set Clustering Parameters

# In[20]:


# Use standardized article count as measure for clustering
target_value = 'norm_article_count'
min_cluster_size = 50
# We want to observe all features available
features = ['color', 'brand', 'Abteilung', 'WHG', 'WUG', 'season', 'month']
# Use absolute distance between the curves as similarity measure
distance_measure = distance.absolute


# #### Rank the Features

# In[21]:


feats = ranking.rank_features(df, distance_measure, features, target_value)
feats


# We can see here that 'WUG' is the most informative feature for us. The **inter-feature variance** is the highest, which means that the single 'WUG's are far apart from each other, thus making good cluster candidates

# #### Building First Clusters (Level 1)

# We start building clusters using the most informative feature.

# In[23]:


get_ipython().run_cell_magic('time', '', '\n# Select important feature\nfeat = feats.iloc[0].feature\n\n# Build Cluster at Level 1\nc1 = build_clusters(df, feat, distance_measure, target_value)')


# In[24]:


cluster_characteristics(c1, feat)


# After first clustering step, we can see that some big clusters (0, 1, 3) and several small clusters have been formed. Since we want to generate clusters, that fulfill a minimum sample size, we now need to merge clusters that fall under the `min_cluster_size` with the respective closest cluster.
# We also see that the first clustering step has taken 18 minutes, which should be improvable.

# In[26]:


get_ipython().run_cell_magic('time', '', '\nc1 = merge_min_clusters(c1, feat, min_cluster_size,\n                        distance.absolute, target_value)')


# In[27]:


cluster_characteristics(c1, feat)


# We can see now that only clusters above the `min_cluster_size` remain. All other clusters have been merged with neighboring clusters. Additionally, the time needed for the merging is negligible compared to the initial clustering step. 

# ### Plotting the Clusters

# Visualizing the results we can see that the mean curves of the clusters are quite different. They follow a similar trend but have different course over time.

# In[28]:


plot_feature_characteristics(c1, 'cluster', target_value);


# #### Principal Component Analysis

# Principal Component Analysis (PCA) is a common technique for feature reduction and visualization of multi-dimensional data in 2D. PCA transform the data onto new "orthogonal" axis, along the axis where there is the largest variance in the original data (the revenue curve with the 26 dimensions, one for each day). Time-series data is not the main use-case for PCA, but nevertheless we can see more than 50% of the variance explained by the first two components. 
# 
# Using PCA for visualization, and plotting the individual articles for the clusters we can see that PCA does not seem to be suitable for our data. However, when we select certain clusters a distinction can be made, which should provide some validation to our methods.

# In[31]:


plot_cluster_pca(c1, [0, 1, 3, 5, 7, 10, 14, 27, 64], target_value);


# In[42]:


plot_cluster_pca(c1, [5, 14, 64], target_value);


# #### Applied to a Use Case

# To make the clustering process more tangible we assume that we are a fashion retailer and want to introduce a new special edition shoe **Breeezy 5000** into our shops. Beforehand, we want to know how many shoes need to be produced how quickly. To satisfy this need we use the **norm_article_count** clustering to find a suitable target set for initial inventory prediction. By looking at the **article count curve** of a shoe within the cluster a decent starting point should be made.
# 
# 
# We assume the following attributes for our **Breeezy 5000**:
# - brand: **Skuld**
# - color: **mittelbraun**
# - Abteilung: **Abteilung005**
# - WHG: **WHG014**
# - WUG: **WUG073**
# - month: **August**
# - season: **Sommer**

# The first clustering step produced clusters that are characterized by *WUG*. We can use reference population for our new shoe, by finding the cluster, which groups articles that have the same *WHG* as the **Breeezy 5000**.
# In this case its *Cluster 0*, which includes WUG073.
# 
# We further want to inspect the cluster size and variance of *Cluster 0*:

# In[43]:


print("Number of articles: %s" %
      cluster_characteristics(c1, feat).loc[0].num_articles)
print("Variance: %s" % cluster_variance(c1, 0, distance_measure, target_value))


# Our shoe is in a relatively large cluster, where the variance is larger than 1. We believe that we can find a better reference population by clustering further:

# #### Redefine the Article Population

# In[44]:


# We looking to Cluster 0
c2 = c1.loc[c1.cluster == 0]


# #### Cluster with the Next Feature

# In[45]:


# For simplicity we define a function for a clustering step
def cluster_step(c):
    feats = ranking.rank_features(c, distance_measure, features, target_value)
    feat = feats.iloc[0].feature
    print("Splitting on feature '%s'." % feat)
    c = build_clusters(c, feat, distance_measure, target_value)
    c = merge_min_clusters(c, feat, min_cluster_size,
                           distance.absolute, target_value)
    return (c, feat)


# In[50]:


get_ipython().run_cell_magic('time', '', '\nc2, feat = cluster_step(c2)')


# In[51]:


cluster_characteristics(c2, feat)


# In[54]:


print("Number of Articles: %s" %
      cluster_characteristics(c2, feat).loc[51].num_articles)
print("Variance: %s" % cluster_variance(
    c2, 51, distance_measure, target_value))


# In[55]:


plot_feature_characteristics(c2, 'cluster', target_value);


# The second level clustering for cluster 0 produced a cluster (51) that has a lot less variance (0.611 in comparison to 1.13), while still having a decent cluster size (81). Looking at the visual output we can see that the **Cluster 51** has a distinct curve when compared to the other clusters.

# While the normalized article_count is used by the algorithm, the raw article_count would be used to determine the real inventory size:

# In[57]:


plot_feature_characteristics(c2, 'cluster', 'article_count');


# ## The Second Approach

# Since the first algorithm is taking too much time for the single-feature-clustering and one has to manually iterate through the levels of clustering, a second try has been made. 
# 
# While the basic idea to split the data based on *inter-feature-variance* and merge *similar* clusters together is still driving the clustering, the second approach splits the data for all available features first - before any merging has taken place. 
# 
# The merging itself also changed to a more efficient version, while approach number one only merges two clusters before recalculating distances, approach number two merges every cluster to its closest neighbor and recalculates distances afterwards. 
# 
# These changes in combination with a new data structure result in superior performance. Additionally, not only *min_cluster_size* is taken into account, but also *max_cluster_count*.
# 
# Besides the efficiency improvement, small subgroups (e.g. from split level 4 and 6) of e.g. split level 1 cluster 0 and cluster 2 can be merged, taking a step away from pure hierarchical clustering, which could be seen as a less restrictive approach and therefore considered beneficial for cluster quality. However, this also dilutes the feature specificity of the clusters, the first approach results in clusters that are 100% identified by a certain feature characteristic combination.

# In[58]:


# Use standardized article count as measure for clustering
target_value = 'norm_article_count'
min_cluster_size = 50
max_cluster_count = 10
# Use absolute distance between the curves as similarity measure
distance_measure = distance.absolute


# Note that this approach automatically uses all categorical features available, therefore there is no need to specify the features.

# In[61]:


get_ipython().run_cell_magic('time', '', '# suppress the print output\n%%capture\n# all steps of both the splitting and the merging are returned\nsplit_results, merge_results = cluster.multi_feature(df, distance_measure, target_value, min_cluster_size, max_cluster_count);')


# The second approach is much faster!

# In[62]:


# show the available layers of the merging process
print(merge_results['Groups'].index)


# In[69]:


assigned_df = multi_feature_cluster.get_cluster_dataframe(merge_results, 4, df)
plot_feature_characteristics(assigned_df, 'cluster', target_value);


# However, with max_cluster_count = 10 the algorithm merges until only two clusters are left, so let's see what the merge layer above looks like:

# In[70]:


assigned_df2 = multi_feature_cluster.get_cluster_dataframe(merge_results, 3, df)
plot_feature_characteristics(assigned_df2, 'cluster', target_value);


# The 13 resulting cluster should be better suited for practice, however, we still need to find out which cluster we want to put our **Breeezy 5000** in:

# In[71]:


multi_feature_cluster.show_cluster_characteristics(df, merge_results, 3, 0.90)


# **Breeezy 5000**:
# 
# - brand: **Skuld**
# - color: **mittelbraun**
# - Abteilung: **Abteilung005**
# - WHG: **WHG014**
# - WUG: **WUG073**
# - month: **August**
# - season: **Sommer**  
# 
# We can see that cluster 11 has 97% of all **Skuld** articles and since no other feature of our **Breeezy 5000** has a higher percentage in any of the clusters we would choose cluster 11 as a reference point.

# An interesting feature of this approach is the identification of relevant clustering features, apparently **WUG** and **brand** can be excellent identifiers for article behavior. Since not all characteristics of WUG and brand are shown in the list, the approach also identifies WUGs and brands that **without a characteristic combination** are not defining article behavior (e.g. WUG073).
# 
# This also shows the weakness of the second approach, as a new article might not be easy to put in a cluster, in the worst case the article feature characteristics are all represented in multiple clusters with relatively low percentages. We also see that cluster 10 and 12 have no characteristic that is represented more than 90% (the parameter used) within those clusters, which could mean that these clusters are bad reference points.
# 
# Cluster 10 and 12 might have characteristic combinations that are only represented in these clusters. Due to time constraints it is currently not possible to check for these combinations.

# # Outlook

# While both approaches work, have their validity and provide usable results, each of them has certain strengths and weaknesses. Due to the project's constraints in time and environment, the algorithms have not been tested in practice, especially against experienced human retailer's decisions. Therefore, the next step would be to test these algorithms in-depth with statistical measures and against real-life practices, possibly resulting in further optimization.  

# Both algorithms could be expanded in their functionality, the first one is not fully automated, the second one is missing identification of cluster-defining characteristic combinations. <br>

# The provided data has been sufficient to serve as a basis for creating an algorithm, however, the restriction to 26 weeks for each article limits the results, since the clustering is only based upon a fraction of an article's lifetime. This restriction also affects the usability of the algorithms, as the full dataset will result in longer run-times. If the run-times in a real-world-setting prove to be impractically long the algorithms need to be revised. <br><br>

# Overall, we consider variance as the determining factor for splitting time-series-clusters and absolute distance in combination with standardization for merging time-series-clusters a success.
