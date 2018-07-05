
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


get_ipython().run_cell_magic('time', '', "\n# get all clusters based on the name\nclusters = list()\n\n# iterate through all layers of the clustering\nfor layer in split_results['Clusters'].index:\n    # add all layer leaves and remove leaf parents\n    for cluster in split_results['Clusters'][layer]:\n        if cluster['Name'] in names:\n            clusters.append(cluster)")


# In[15]:


len(clusters)


# In[101]:


get_ipython().run_cell_magic('time', '', "\nlength = len(clusters)\ndistances = pd.DataFrame(index=range(length),columns=range(length))\ntargets = list()\n\n# dress the clusters for better distance performance\nfor i, cluster in enumerate(clusters):\n    # only select the distance relevant slice of the Dataframe\n    target = cluster['DataFrame'].groupby(['time_on_sale']).mean()['article_count']\n    if (len(target) < 26):\n        # fill with 0 until index 25 so all comparison arrays are the same length\n        # this improves performance dramatically\n        target = target.reindex(pd.RangeIndex(26)).fillna(0)\n    targets.append(target)")


# In[103]:


get_ipython().run_cell_magic('time', '', 'length = len(targets)\nfor i, a in enumerate(targets):\n    for k, b in enumerate(reversed(targets)):\n        j = length - 1 - k\n        if j <= i:\n            break\n        else:\n            try:\n                d = distance.euclidean(a.values,b.values)\n                distances[i][j] = d\n                distances[j][i] = d\n            except:\n                print(str(i) + " " + str(k))')


# In[104]:


distances


# In[112]:


min_index = np.nanargmin(distances[0])
min_value = np.nanmin(distances[0])
print(str(min_index) + " " + str(min_value))


# In[114]:


distances[0][41]


# In[339]:


# get the closest cluster for each cluster
# generates a Series with pointer lists
closest_clusters = pd.Series(index=range(length), dtype='object')
for i in distances.index:
    target_index = np.nanargmin(distances[i]).item()
    # only one value now, but we will add values later
    closest_clusters[i] = list()
    closest_clusters[i].append(target_index)

    
cluster_groups = closest_clusters
    
# generate initial groups by adding the index to the target
for i, group in cluster_groups.iteritems():
    # first value is the initial closest cluster
    target = group[0]
    cluster_groups[target].append(i)

# merge until there are only loners and groups with a pointer loop  
# a pointer loop is when two cluster point towards each other, even over multiple cluster between
finished = False 
while not finished:
    finished = True
    
    # merge dependencies
    for i, group in cluster_groups.iteritems():
        # ignore loners
        if len(group) > 1:
            # first value is the initial closest cluster
            target = group[0]
            # rest of the values are pointers added by dependent groups
            pointers = group[1:]
            try:
                # check whether this is a dependent group without a pointer loop
                if (target not in pointers):
                    # still dependent groups left, we need to iterate at least one more time
                    finished = False
                    # sanity check whether looping is required
                    if ((pointers is list) or (pointers is tuple)):
                        # multiple entries we can loop
                        for x in pointers:
                            if (x not in cluster_groups[target]):
                                cluster_groups[target].append(x)
                    elif len(pointers) > 0:
                        cluster_groups[target].append(pointers[0])
                    # dependent group is spent, create loner
                    cluster_groups[i] = list()
                    cluster_groups[i].append(target)
            except:
                print("shit's on fire, yo")
                print(str(i) + " " + str(group) + " " + str(target) + " " + str(pointers))

# clear loners
for i, group in cluster_groups.iteritems():
    if (len(group) <= 1):
        cluster_groups = cluster_groups.drop(i) 

# dress up the group list        
merged_groups = list()
for i, group in cluster_groups.iteritems():
    # replace target with own index
    temp = group
    temp[0] = i
    temp = sorted(temp)
    merged_groups.append(temp)
merged_groups = sorted(merged_groups)

# merge connected groups and remove duplicates
for i, group_a in enumerate(merged_groups):
    if group_a is not None:
        for k, group_b in enumerate(merged_groups):
            if k != i:
                for x in group_a:
                    if group_b is not None:
                        if x in set(group_b):
                            group_a = sorted(list(set(group_a).union(set(group_b))))
                            merged_groups[k] = None
clean = list(filter(lambda x: x is not None, merged_groups))


# In[340]:


len(clean)


# In[341]:


clean

