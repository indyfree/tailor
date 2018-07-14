
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
import itertools

import tailor
from tailor.clustering import *


# In[3]:


data = tailor.load_data()


# In[4]:


data.sample(10)


# # Code

# In[5]:


min_cluster_size = 50
max_cluster_count = 10
clustering_feature = 'article_count'


# In[6]:


get_ipython().run_cell_magic('time', '', '\nsplit_results = cluster.multi_feature_split(data, distance.euclidean, min_cluster_size)')


# In[7]:


# show the available split layers/depth
split_results['Clusters'].index


# In[8]:


# showcasing how to retrieve the cluster feauteres of the first cluster of the fifth layer
split_results['Clusters']['5'][0]['Features']


# In[9]:


merge_results = pd.Series()
merge_results['Groups'] = pd.Series()
merge_results['Indexes'] = pd.Series()
merge_results['DataFrames'] = pd.Series()


# In[10]:


def get_cluster_parent_name(cluster):
    '''generates the name of the parent cluster'''
    name = cluster['Name']
    # remove last character until name is the parent cluster's name
    terminate = False
    while not terminate:
        character = name[-1:]
        if ((character == "_") or (character == "")):
            terminate = True
        name = name[:-1]
    return name


# In[11]:


def get_leaves(split_results):
    '''retrieves all the unsplit clusters / the leaves of the split tree'''
    leaves = list()
    # iterate through all layers of the clustering
    for layer in split_results['Clusters'].index:
        # add all layer leaves and remove leaf parents
        for add_cluster in split_results['Clusters'][layer]:
            check_name = get_cluster_parent_name(add_cluster)
            # iterate until parent cluster is found then remove it
            for index, check_cluster in enumerate(leaves):
                if check_cluster['Name'] == check_name:
                    # parent cluster found, remove it
                    del leaves[index]
                    # no more than one parent cluster, therefore exit for loop
                    break
            leaves.append(add_cluster)
    return leaves


# In[12]:


get_ipython().run_cell_magic('time', '', '\nclusters = get_leaves(split_results)\nprint(len(clusters))')


# In[13]:


def get_cluster_names(clusters, reversed_sort = False):
    '''retrieves all names of the given clusters'''
    names = list()
    for cluster in clusters:
        name = cluster['Name']
        names.append(name)
    # sort by underscore count
    names.sort(key = lambda s: s.count("_"), reverse=reversed_sort)
    return names


# In[ ]:


get_cluster_names(clusters)


# In[14]:


def get_distance_matrix(targets):
    #calculate distance matrix
    length = len(targets)
    distances = pd.DataFrame(index=range(length),columns=range(length))
    for i, a in enumerate(targets):
        for k, b in enumerate(reversed(targets)):
            j = length - 1 - k
            if j <= i:
                break
            else:
                try:
                    d = distance.euclidean(a.values,b.values)
                    distances[i][j] = d
                    distances[j][i] = d
                except:
                    print(str(i) + " " + str(k))
    return distances


# In[15]:


get_ipython().run_cell_magic('time', '', "\nlength = len(clusters)\ntargets = list()\n\n# dress the clusters for better distance performance\nfor i, cluster in enumerate(clusters):\n    # only select the distance relevant slice of the Dataframe\n    target = cluster['DataFrame'].groupby(['time_on_sale']).mean()[feature]\n    if (len(target) < 26):\n        # fill with 0 until index 25 so all comparison arrays are the same length\n        # this improves performance dramatically\n        target = target.reindex(pd.RangeIndex(26)).fillna(0)\n    targets.append(target)\n\ndistances = get_distance_matrix(targets)")


# In[ ]:


min_index = np.nanargmin(distances[0])
min_value = np.nanmin(distances[0])
print(str(min_index) + " " + str(min_value))


# In[ ]:


print(distances[0][41])
print(distances[41][0])


# In[16]:


def merge_all(distances):
    # get the closest cluster for each cluster
    # generates a Series with pointer lists
    closest_clusters = pd.Series(index=range(len(distances)), dtype='object')
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
    
    print(len(list(set(list(itertools.chain.from_iterable(clean))))))
    print(len(clean))
    
    return clean


# In[17]:


grouped_clusters = merge_all(distances)


# In[18]:


merge_results['Indexes']['0'] = grouped_clusters


# In[19]:


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
        # e.g. '(Abteilung == "Abteilung001") & (WHG == "WHG003")'
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


# In[ ]:


merge_results['DataFrames']['0'][0].sample(5)


# In[ ]:


merge_results['Groups']['0'][0]


# In[ ]:


merge_results['Indexes']['0'][0]


# In[60]:


merge_number = 1
above_min_size = False
clustering_feature = 'article_count'


# In[61]:


while not above_min_size:
    above_min_size = True
    # check whether all clusters are above min_cluster_size
    too_small = list()
    for i, group in enumerate(merge_results['Groups'][str(merge_number - 1)]):
        group_size = merge_results['DataFrames'][str(merge_number - 1)][i]['article_id'].nunique()
        if group_size < min_cluster_size:
            above_min_size = False
            too_small.append(i)
    print(len(too_small))
    
    if not above_min_size:
        # distance matrix generation
        length = len(merge_results['Groups'][str(merge_number - 1)])
        targets = list()
        # dress the clusters for better distance performance
        for i, group in enumerate(merge_results['Groups'][str(merge_number - 1)]):
            # only select the distance relevant slice of the Dataframe
            target = merge_results['DataFrames'][str(merge_number - 1)][i].groupby(['time_on_sale']).mean()[clustering_feature]
            if (len(target) < 26):
                # fill with 0 until index 25 so all comparison arrays are the same length
                # this improves performance dramatically
                target = target.reindex(pd.RangeIndex(26)).fillna(0)
            targets.append(target)
        distances = get_distance_matrix(targets)
        
        
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
        
        print(len(list(set(list(itertools.chain.from_iterable(clean))))))
        
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
        
        clean = list()
        for i, group in new_groups.iteritems():
            sgroup = sorted(group)
            if sgroup not in clean:
                clean.append(sgroup)
        clean = sorted(clean)
        
        print(len(list(set(list(itertools.chain.from_iterable(clean))))))
        
        merge_results['Indexes'][str(merge_number)] = clean
        merge_results['Groups'][str(merge_number)] = list()
        merge_results['DataFrames'][str(merge_number)] = list()
        for i, pointers in enumerate(merge_results['Indexes'][str(merge_number)]):
            group = list()
            dfs = list()
            for pointer in pointers:
                df_temp = merge_results['DataFrames'][str(merge_number-1)][pointer]
                dfs.append(df_temp)
                for cluster in merge_results['Groups'][str(merge_number-1)][pointer]:
                    group.append(cluster)
            merge_results['Groups'][str(merge_number)].append(group)
            # merge the clusters' dataframes to one and add it
            merge_results['DataFrames'][str(merge_number)].append(pd.concat(dfs, sort=True))
        merge_number += 1


# In[62]:


print(merge_results['Indexes'].index)
print(merge_number)


# In[70]:


count = 0
for group in merge_results['Groups']['1']:
    count += len(group)
print(count)
print(len(merge_results['Groups']['1']))


# In[72]:


while len(merge_results['Groups'][str(merge_number - 1)]) > max_cluster_count:
    # distance matrix generation
    length = len(merge_results['Groups'][str(merge_number - 1)])
    targets = list()
    # dress the clusters for better distance performance
    for i, group in enumerate(merge_results['Groups'][str(merge_number - 1)]):
        # only select the distance relevant slice of the Dataframe
        target = merge_results['DataFrames'][str(merge_number - 1)][i].groupby(['time_on_sale']).mean()[clustering_feature]
        if (len(target) < 26):
            # fill with 0 until index 25 so all comparison arrays are the same length
            # this improves performance dramatically
            target = target.reindex(pd.RangeIndex(26)).fillna(0)
        targets.append(target)
    distances = get_distance_matrix(targets)
    clean = merge_all(distances)
    merge_results['Indexes'][str(merge_number)] = clean
    merge_results['Groups'][str(merge_number)] = list()
    merge_results['DataFrames'][str(merge_number)] = list()
    for i, pointers in enumerate(merge_results['Indexes'][str(merge_number)]):
        group = list()
        dfs = list()
        for pointer in pointers:
            df_temp = merge_results['DataFrames'][str(merge_number-1)][pointer]
            dfs.append(df_temp)
            for cluster in merge_results['Groups'][str(merge_number-1)][pointer]:
                group.append(cluster)
        merge_results['Groups'][str(merge_number)].append(group)
        # merge the clusters' dataframes to one and add it
        merge_results['DataFrames'][str(merge_number)].append(pd.concat(dfs, sort=True))
    merge_number += 1


# In[73]:


print(merge_results['Indexes'].index)
print(merge_number)


# In[77]:


count = 0
for group in merge_results['Groups']['3']:
    count += len(group)
print(count)
print(len(merge_results['Groups']['3']))


# In[92]:


for i, df in enumerate(merge_results['DataFrames']['4']):
    for col in df.select_dtypes(include=['category']):
        # print(str(i) + ": " + str(col) + ": " + str(df[col].unique()))
        if "article_id" not in col:
            for characteristic in df[col].unique():
                query_string = str(col) + " == " + '"' + str(characteristic) + '"'
                temp_df = df.query(query_string)
                print(str(i) + ": " + str(characteristic) + ": " + str(temp_df['article_id'].nunique()))
    print("")

