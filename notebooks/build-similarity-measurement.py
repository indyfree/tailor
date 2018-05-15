
# coding: utf-8

# In[1]:


import tailor
import pandas as pd
import matplotlib.pyplot as plt


# # Create initial DataFrame

# In[2]:


raw_df = tailor.load_raw_dataframe()
df_revenue = raw_df[['article_id', 'time_on_sale', 'revenue']]


# ### To give an example, the dataframe looks like this ...

# In[3]:


df_revenue.head()


# # Create a Benchmark Series
# 
# ### Now reshape the dataframes into a format which makes it easier to calculate the mean of each time_on_sale value.  The following steps must be done for each  performance measure.  For now, we will just do it for the dataframe with the column 'revenue' (df_revenue)
# 
# 

# In[4]:


df_pivoted = pd.pivot_table(df_revenue, values='revenue', index='article_id', columns='time_on_sale')
df_reshaped = pd.DataFrame(df_pivoted.to_records()) #cast pivot table into DataFrame 
df_reshaped.head()


# ### Next, calculate the mean of each column. Therefore, you have the mean for each time_on_sale value. This series can be used as a benchmark series. 

# In[5]:


revenue_benchmark = df_reshaped.mean(axis=0)
revenue_benchmark.head()


# ### Drop mean of article ids. It makes no sense and we dont need it 

# In[6]:


revenue_benchmark = revenue_benchmark.drop(revenue_benchmark.index[0])
revenue_benchmark.head()


# ### Cast series into a DataFrame

# In[7]:


df_revenue_benchmark = pd.DataFrame()
df_revenue_benchmark['time_on_sale'] = revenue_benchmark.keys()
df_revenue_benchmark['mean_revenue'] = revenue_benchmark.values
df_revenue_benchmark.head()


# # Calculate distance to Benchmark Series
# 
# ### Merging both DataFrames yields in ...

# In[8]:


result = pd.merge(df_revenue, df_revenue_benchmark, how='left', on='time_on_sale', left_index=False, right_index=True, sort=True, validate='m:1')
result = result.reset_index()
result = result.drop('index', axis=1)
result = result.rename(index=str, columns={'mean_revenue_y':'mean_revenue'})
result.head()


# ### Calculate the distance between revenue and mean_revenue

# In[9]:


result['distance'] = ((result['revenue'] - result['mean_revenue'])**2)**0.5
result.head()


# ### Sum up all distances to get just one value for similiarity measurement

# In[10]:


result = result.groupby('article_id').sum()
result = result.reset_index()
result = result = result.drop(['revenue', 'mean_revenue'], axis=1)
result.head()


# In[11]:


result = result.sort_values('distance', ascending=False)
result.head()


# # First evaluation of the similarity measurement
# 
# ### Let us plot some articles with similiar distances. To find similiar values, I just had a look at the sorted result dataframe

# In[12]:


article_one = raw_df[raw_df['article_id']==902792]
article_two = raw_df[raw_df['article_id']==901825]

plt.plot(article_one['time_on_sale'], article_one['revenue'], 'r')
plt.plot(article_two['time_on_sale'], article_two['revenue'], 'b')


# In[13]:


article_three = raw_df[raw_df['article_id']==900546]
article_four = raw_df[raw_df['article_id']==906171]

plt.plot(article_three['time_on_sale'], article_three['revenue'], 'r')
plt.plot(article_four['time_on_sale'], article_four['revenue'], 'b')


# ### Looks not too bad, but maybe we could split the benchmark series into multiple pieces and calculate the distances to those pieces. That could level out the effect of different shapes on similiar distances.
