
# coding: utf-8

# # Initialization

# In[1]:


# Display plots inline
get_ipython().run_line_magic('matplotlib', 'inline')

# Autoreload all package before excecuting a call
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[22]:


import pandas as pd
import numpy as np
import multiprocessing as mp
import itertools

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


# In[16]:


get_ipython().run_cell_magic('time', '', "\nlength = len(clusters)\ndistances = pd.DataFrame(index=range(length),columns=range(length))\ntargets = list()\n\n# dress the clusters for better distance performance\nfor i, cluster in enumerate(clusters):\n    # only select the distance relevant slice of the Dataframe\n    target = cluster['DataFrame'].groupby(['time_on_sale']).mean()['article_count']\n    if (len(target) < 26):\n        # fill with 0 until index 25 so all comparison arrays are the same length\n        # this improves performance dramatically\n        target = target.reindex(pd.RangeIndex(26)).fillna(0)\n    targets.append(target)")


# In[17]:


get_ipython().run_cell_magic('time', '', 'length = len(targets)\nfor i, a in enumerate(targets):\n    for k, b in enumerate(reversed(targets)):\n        j = length - 1 - k\n        if j <= i:\n            break\n        else:\n            try:\n                d = distance.euclidean(a.values,b.values)\n                distances[i][j] = d\n                distances[j][i] = d\n            except:\n                print(str(i) + " " + str(k))')


# In[18]:


distances


# In[19]:


min_index = np.nanargmin(distances[0])
min_value = np.nanmin(distances[0])
print(str(min_index) + " " + str(min_value))


# In[20]:


distances[0][41]


# In[23]:


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
        # loner check
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
                    # add own index to target
                    cluster_groups[target].append(i)
                    # sanity check whether looping is required
                    if (type(pointers) is list):
                        # multiple entries we can loop
                        for x in pointers:
                            if (x not in cluster_groups[target]):
                                cluster_groups[target].append(x)
                    else:
                        print(pointers)
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
        target = group[0]
        if target in cluster_groups.index:
            cluster_groups[target].append(i)
            cluster_groups = cluster_groups.drop(i) 

# dress up the group list        
merged_groups = list()
for i, group in cluster_groups.iteritems():
    # replace target with own index
    temp = group
    temp.append(i)
    temp = sorted(list(set(temp)))
    merged_groups.append(temp)
merged_groups = sorted(merged_groups)

print(len(list(set(list(itertools.chain.from_iterable(merged_groups))))))

# merge connected groups and remove duplicates
for i, group_a in enumerate(merged_groups):
    for k, group_b in enumerate(merged_groups):
        if k is not i:
            for x in group_a:
                if x in set(group_b):
                    merged_groups[i] = list(set(group_a).union(set(group_b)))
                    # both will point to the same list
                    merged_groups[k] = merged_groups[i]
                    
clean = list()
for group in merged_groups:
    sgroup = sorted(group)
    if sgroup not in clean:
        clean.append(sgroup)
clean = sorted(clean)


# In[24]:


len(clean)


# In[25]:


len(list(set(list(itertools.chain.from_iterable(clean)))))


# In[26]:


clean


# In[27]:


data.query('Abteilung == "Abteilung001"')


# In[28]:


merge_results = pd.Series()
merge_results['Groups'] = pd.Series()
merge_results['Indexes'] = pd.Series()
merge_results['DataFrames'] = pd.Series()


# In[29]:


merge_results['Indexes']['0'] = clean


# In[30]:


merge_results['Groups']['0'] = list()
merge_results['DataFrames']['0'] = list()
for i, pointers in enumerate(merge_results['Indexes']['0']):
    group = list()
    dfs = list()
    for pointer in pointers:
        cluster = clusters[pointer]
        group.append(cluster)
        # retrieving the relevant part of the original dataframe since the cluster dataframe has missing columns
        query_string = ""
        # building the query string
        for feature, characteristic in cluster['Features'].iteritems():
            query_string = query_string + " & " + "(" + feature + " == " + '"' + characteristic + '"' + ")"
        # remove first " & "
        query_string = query_string[3:]
        # select the dataframe part
        df_temp = data.query(query_string)
        dfs.append(df_temp)
    merge_results['Groups']['0'].append(group)
    # merge the clusters' dataframes to one and add it
    merge_results['DataFrames']['0'].append(pd.concat(dfs, sort=True))


# In[31]:


merge_results['DataFrames']['0'][0]


# In[32]:


merge_results['Groups']['0'][0]


# In[33]:


merge_results['Indexes']['0'][0]


# In[34]:


too_small = list()
for i, group in enumerate(merge_results['Groups']['0']):
    group_size = merge_results['DataFrames']['0'][i]['article_id'].nunique()
    if group_size < 50:
        too_small.append(i)
print(len(too_small))
print(too_small)


# In[35]:


get_ipython().run_cell_magic('time', '', "\nlength = len(merge_results['Groups']['0'])\ndistances = pd.DataFrame(index=range(length),columns=range(length))\ntargets = list()\n\n# dress the clusters for better distance performance\nfor i, group in enumerate(merge_results['Groups']['0']):\n    # only select the distance relevant slice of the Dataframe\n    target = merge_results['DataFrames']['0'][i].groupby(['time_on_sale']).mean()['article_count']\n    if (len(target) < 26):\n        # fill with 0 until index 25 so all comparison arrays are the same length\n        # this improves performance dramatically\n        target = target.reindex(pd.RangeIndex(26)).fillna(0)\n    targets.append(target)")


# In[36]:


get_ipython().run_cell_magic('time', '', 'length = len(targets)\nfor i, a in enumerate(targets):\n    for k, b in enumerate(reversed(targets)):\n        j = length - 1 - k\n        if j <= i:\n            break\n        else:\n            try:\n                d = distance.euclidean(a.values,b.values)\n                distances[i][j] = d\n                distances[j][i] = d\n            except:\n                print(str(i) + " " + str(k))')


# In[37]:


distances


# In[38]:


# get the closest group for each group that is too small
# generates a Series with pointer lists
closest_groups = pd.Series(index=range(length), dtype='object')
for i in too_small:
    target_index = np.nanargmin(distances[i]).item()
    # only one value now, but we will add values later
    closest_groups[i] = list()
    closest_groups[i].append(target_index)

    
relevant_groups = closest_groups

relevant_groups = relevant_groups.dropna()

print(len(relevant_groups))

check_temp = list()
for index, value in relevant_groups.iteritems():
    check_temp.append(index)
    check_temp.extend(value)

print(len(list(set(check_temp))))


# In[39]:


# generate initial groups by adding the index to the target
for i, group in relevant_groups.iteritems():
    if group is not np.nan:
        # first value is the initial closest group
        target = group[0]
        # sanity check
        if target in relevant_groups.index:
            relevant_groups[target].append(i)
        else:
            # targeting group outside of too_small
            # add own index to own group to not be a loner
            group.append(i)
        

# merge until there are only loners and groups with a pointer loop  
# a pointer loop is when two groups point towards each other, even over multiple groups in between
finished = False 
while not finished:
    finished = True
    
    # merge dependencies
    for i, group in relevant_groups.iteritems():
        # ignore loners
        if len(group) > 1:
            # first value is the initial closest cluster
            target = group[0]
            # sanity check
            if target in relevant_groups.index:
                # rest of the values are pointers added by dependent groups
                pointers = group[1:]
                try:
                    # check whether this is a dependent group without a pointer loop
                    if (target not in pointers):
                        # still dependent groups left, we need to iterate at least one more time
                        finished = False
                        # add own index to target
                        relevant_groups[target].append(i)
                        # sanity check whether looping is required
                        if type(pointers) is list:
                            # multiple entries we can loop
                            for x in pointers:
                                if (x not in relevant_groups[target]):
                                    relevant_groups[target].append(x)
                        else:
                            print(pointers)
                            relevant_groups[target].append(pointers[0])
                        # dependent group is spent, create loner
                        relevant_groups[i] = list()
                        relevant_groups[i].append(target)
                except:
                    print("shit's on fire, yo")
                    print(str(i) + " " + str(group) + " " + str(target) + " " + str(pointers))

# clear loners
for i, group in relevant_groups.iteritems():
    if (len(group) <= 1):
        target = group[0]
        if target in relevant_groups.index:
            relevant_groups[target].append(i)
            relevant_groups = relevant_groups.drop(i)         

# dress up the group list        
sorted_groups = list()
for i, group in relevant_groups.iteritems():
    # replace target with own index
    temp = group
    temp.append(i)
    temp = sorted(list(set(temp)))
    sorted_groups.append(temp)
sorted_groups = sorted(sorted_groups)

# merge connected groups and remove duplicates
for i, group_a in enumerate(sorted_groups):
    for k, group_b in enumerate(sorted_groups):
        if k is not i:
            for x in group_a:
                if x in set(group_b):
                    sorted_groups[i] = list(set(group_a).union(set(group_b)))
                    # both will point to the same list
                    sorted_groups[k] = sorted_groups[i]              
clean = list()
for group in sorted_groups:
    sgroup = sorted(group)
    if sgroup not in clean:
        clean.append(sgroup)
clean = sorted(clean)

print(len(list(set(list(itertools.chain.from_iterable(sorted_groups))))))
print(len(list(set(list(itertools.chain.from_iterable(clean))))))


# In[41]:


new_groups = pd.Series(index=range(length), dtype='object')

# initialize with own index
for i in new_groups.index:
    if i not in too_small:
        new_groups[i] = list()
        new_groups[i].append(i)

# include the newly generated groups
for i, group in enumerate(clean):
    found = False
    for x in group:
        if x not in too_small:
            # found target group that already was big enough
            found = True
            try:
                # merge groups
                temp = list()
                temp.extend(group)
                temp.extend(new_groups[x])
                temp = sorted(list(set(temp)))
                new_groups[x] = temp
            except:
                print(x)
                print(new_groups[x])
                print(group)
            break
    if not found:
        # add new group only made of merged too_small groups
        new_groups[group[0]] = group

new_groups = new_groups.dropna()

print(len(list(set(list(itertools.chain.from_iterable(new_groups.values))))))

clean = list()
for i, group in new_groups.iteritems():
    sgroup = sorted(group)
    if sgroup not in clean:
        clean.append(sgroup)
clean = sorted(clean)

print(len(list(set(list(itertools.chain.from_iterable(clean))))))


# In[46]:


print(len(clean))
print(clean)


# In[42]:


merge_results['Indexes']['1'] = clean


# In[43]:


# TODO merge_results['Groups']['1'] = list()
merge_results['DataFrames']['1'] = list()
for i, pointers in enumerate(merge_results['Indexes']['1']):
    # TODO group = list()
    dfs = list()
    for pointer in pointers:
        df_temp = merge_results['DataFrames']['0'][pointer]
        dfs.append(df_temp)
    # TODO merge_results['Groups']['1'].append(group)
    # merge the clusters' dataframes to one and add it
    merge_results['DataFrames']['1'].append(pd.concat(dfs, sort=True))


# In[44]:


too_small = list()
for i, group in enumerate(merge_results['Indexes']['1']):
    group_size = merge_results['DataFrames']['1'][i]['article_id'].nunique()
    if group_size < 50:
        too_small.append(i)
print(len(too_small))
print(too_small)


# In[45]:


len(merge_results['Indexes']['1'])

