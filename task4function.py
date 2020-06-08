#!/usr/bin/env python
# coding: utf-8

# In[6]:
import pandas as pd
from tqdm import tqdm



def calculate_edit_distance(word1, word2):
    return sum([0 if i==j else 1 for i,j in zip(word2,word1)])

class ResultNode:

    def __init__(self, data, distance):
        self.data = data
        self.distance = distance

class TreeNode:

    def __init__(self, data):
        self.data = data
        self.child_node_dict = {}

    def put(self, chars):
        distance = calculate_edit_distance(chars, self.data)
        if distance == 0:
            return
        keys = self.child_node_dict.keys()
        if distance in keys:
            self.child_node_dict[distance].put(chars)
        else:
            self.child_node_dict[distance] = TreeNode(chars)

    def query(self, target_char, n):
        results = []
        keys = self.child_node_dict.keys()
        distance = calculate_edit_distance(target_char, self.data)
        if distance <= n:
            results.append(ResultNode(self.data, distance))
        # if distance != 0:
        for query_distance in range(max(distance - n, 1), distance + n + 1):
            if query_distance not in keys:
                continue
            value_node = self.child_node_dict[query_distance]
            results += value_node.query(target_char, n)
        return results

    def get_all_data(self):
        results = []
        keys = self.child_node_dict.keys()
        values = self.child_node_dict.values()
        results += [node.data for node in values]
        for key in keys:
            value_node = self.child_node_dict[key]
            results += value_node.get_all_data()
        return results


class BKTree:

    def __init__(self, root_chars):
        self.root_node = TreeNode(root_chars)

    def put(self, chars):
        self.root_node.put(chars)

    def query(self, target_char, n):
        if self.root_node is None:
            return ResultNode(target_char, 0)
        else:
            queries = self.root_node.query(target_char, n)
            if len(queries) == 0:
                return []
            else:
                # queries.sort(key=lambda x: x.distance, reverse=False)
                return queries

    def get_all_data(self):
        if self.root_node is None:
            return []
        else:
            return self.root_node.get_all_data()


if __name__ == '__main__':

    data = pd.read_csv('Task4_database.csv')
    data = data.values.tolist()
    tree = BKTree([0 for i in range(65)])
    for row in tqdm(data[1:]):
        tree.put(row[1:])
    import pickle
    with open('tree.bin','wb') as f:
        pickle.dump(tree,f)




