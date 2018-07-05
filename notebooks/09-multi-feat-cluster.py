
# coding: utf-8

# # Initialization

# In[1]:


# Display plots inline
get_ipython().run_line_magic('matplotlib', 'inline')

# Autoreload all package before excecuting a call
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[2]:


import pandas as pd
import numpy as np
import multiprocessing as mp

import tailor
from tailor.clustering import *


# In[3]:


data = tailor.load_data()


# In[4]:


data.sample(10)


# # Code

# In[5]:


get_ipython().run_cell_magic('time', '', '\nsplit_results = cluster.multi_feature_split(data, distance.euclidean, 50)')


# In[6]:


split_results['Clusters'].index


# In[7]:


split_results['Clusters']['5'][0]['Features']


# In[8]:


def get_cluster_parent_name(cluster):
    name = cluster['Name']
    # remove last character until name is the parent cluster's name
    terminate = False
    while not terminate:
        character = name[-1:]
        if ((character == "_") or (character == "")):
            terminate = True
        name = name[:-1]
    return name


# In[9]:


get_ipython().run_cell_magic('time', '', "\n# get all clusters that remained unsplit\nleafs = list()\n\n# iterate through all layers of the clustering\nfor layer in split_results['Clusters'].index:\n    # add all layer leaves and remove leaf parents\n    for add_cluster in split_results['Clusters'][layer]:\n        check_name = get_cluster_parent_name(add_cluster)\n        # iterate until parent cluster is found then remove it\n        for index, check_cluster in enumerate(leafs):\n            if check_cluster['Name'] == check_name:\n                # parent cluster found, remove it\n                del leafs[index]\n                # no more than one parent cluster, therefore exit second for loop\n                break\n        leafs.append(add_cluster)")


# In[10]:


len(leafs)


# In[11]:


get_ipython().run_cell_magic('time', '', '\nnames = list()\n\nfor cluster in leafs:\n    name = cluster[\'Name\']\n    names.append(name)\n# sort by underscore count\nnames.sort(key = lambda s: s.count("_"), reverse=True)')


# In[12]:


names


# In[13]:


len(names)


# In[14]:


get_ipython().run_cell_magic('time', '', "\n# get all clusters that are above min_cluster_size\nparents = list()\n\n# iterate through all layers of the clustering\nfor layer in split_results['Clusters'].index:\n    # add all layer leaves and remove leaf parents\n    for cluster in split_results['Clusters'][layer]:\n        if cluster['Name'] in names:\n            parents.append(cluster)")


# In[15]:


len(parents)


# In[86]:


get_ipython().run_cell_magic('time', '', "\nlength = len(parents)\ndistances = pd.DataFrame(index=range(length),columns=range(length))\ntargets = list()\n\n# dress the clusters for better distance performance\nfor i, cluster in enumerate(parents):\n    # only select the distance relevant slice of the Dataframe\n    target = cluster['DataFrame'].groupby(['time_on_sale']).mean()['article_count']\n    if (len(target) < 26):\n        # fill with 0 for better performance later on\n        target = target.reindex(pd.RangeIndex(26)).fillna(0)\n    targets.append(target)")


# In[98]:


get_ipython().run_cell_magic('time', '', 'length = len(targets)\nfor i, a in enumerate(targets):\n    for k, b in enumerate(reversed(targets)):\n        j = length - 1 - k\n        if j <= i:\n            break\n        else:\n            try:\n                d = distance.euclidean(a.values,b.values)\n                distances[i][j] = d\n                distances[j][i] = d\n            except:\n                print(str(i) + " " + str(k))')


# In[99]:


distances

