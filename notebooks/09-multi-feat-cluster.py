
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


# In[37]:


def get_cluster_parent_name(cluster):
    name = cluster['Name']
    # remove last character until name is the parent cluster's name
    terminate = False
    while not terminate:
        character = name[-1:]
        if ((character == "_") or (character == "0") or (character == "")):
            terminate = True
        name = name[:-1]
    return name


# In[38]:


get_ipython().run_cell_magic('time', '', "\n# get all clusters that remained unsplit\nleafs = list()\n\n# iterate through all layers of the clustering\nfor layer in split_results['Clusters'].index:\n    # add all layer leaves and remove leaf parents\n    for add_cluster in split_results['Clusters'][layer]:\n        check_name = get_cluster_parent_name(add_cluster)\n        # iterate until parent cluster is found then remove it\n        for index, check_cluster in enumerate(leafs):\n            if check_cluster['Name'] == check_name:\n                # parent cluster found, remove it\n                del leafs[index]\n                # no more than one parent cluster, therefore exit second for loop\n                break\n        leafs.append(add_cluster)")


# In[39]:


len(leafs)


# In[29]:


get_ipython().run_cell_magic('time', '', '\nnames = list()\n\nfor cluster in leafs:\n    name = cluster[\'Name\']\n    # remove last character until name is the parent cluster\'s name\n    found_underscore = False\n    while not found_underscore:\n        character = name[-1:]\n        if character == "_":\n            found_underscore = True\n        name = name[:-1]\n    names.append(name)\n# only save uniques by converting to set \nnames = set(names)')


# In[40]:


names


# In[41]:


len(names)


# In[42]:


get_ipython().run_cell_magic('time', '', "\n# get all clusters that are above min_cluster_size\nparents = list()\n\n# iterate through all layers of the clustering\nfor layer in split_results['Clusters'].index:\n    # add all layer leaves and remove leaf parents\n    for cluster in split_results['Clusters'][layer]:\n        if cluster['Name'] in names:\n            parents.append(cluster)")


# In[43]:


len(parents)


# In[45]:


get_ipython().run_cell_magic('time', '', "\nlength = len(parents)\ndistances = np.ndarray(shape=(length,length))\n\nfor i, a in enumerate(parents):\n    a_curve = a['DataFrame'].set_index('time_on_sale')\n    for k, b in enumerate(parents):\n        if k <= i:\n            continue\n        b_curve = b['DataFrame'].set_index('time_on_sale')\n        d = distance.euclidean(a_curve['article_count'], b_curve['article_count'])\n        distances[i][k] = d\n        distances[k][i] = d ")


# In[46]:


distances

