from generate_dataset import generate_data
from itertools import combinations
from generate_rule import generate_rule
from read_IBM_Data import IBM_data

class Hashnode():
    def __init__(self):
        self.children = {}
        self.bucket = {}
        self.isleaf = True


class HashTree():
    def __init__(self, max_child_num, max_bucket_num):
        self.root = Hashnode()
        self.max_bucket_num = max_bucket_num
        self.max_child_num = max_child_num
        self.frequency_table = {}
        self.min_support = None

    def recursive_insert(self, now_node, itemset, item_index, cnt):
        if item_index == len(itemset):
            if itemset in now_node.bucket:
                now_node.bucket[itemset] += cnt
            else:
                now_node.bucket[itemset] = cnt
            return
        # print(itemset)
        if now_node.isleaf:
            if itemset in now_node.bucket:
                now_node.bucket[itemset] += cnt
            else:
                now_node.bucket[itemset] = cnt
                if len(now_node.bucket) > self.max_bucket_num:
                    for old_itemset, frequency in now_node.bucket.items():
                        hash_key = self.hash(old_itemset[item_index])
                        if hash_key not in now_node.children:
                            now_node.children[hash_key] = Hashnode()
                        self.recursive_insert(
                            now_node.children[hash_key], old_itemset, item_index+1, frequency)
                    now_node.isleaf = False
                    del now_node.bucket
        else:
            hash_key = self.hash(itemset[item_index])
            if hash_key not in now_node.children:
                now_node.children[hash_key] = Hashnode()
            self.recursive_insert(
                now_node.children[hash_key], itemset, item_index+1, cnt)

    def insert_dataset(self, dataset):
        for transaction in dataset:
            itemsets = combinations(transaction, self.max_child_num)
            for itemset in itemsets:
                itemset = list(itemset)
                itemset.sort()
                self.recursive_insert(self.root, tuple(itemset), 0, 1)

    def hash(self, value):
        return value % self.max_child_num

    # def dfs_support_calc(self, now_node, itemset, item_index):
    #     if now_node.isleaf:
    #         if itemset in now_node.bucket:
    #             now_node.bucket[itemset] += 1
    #     else:
    #         hash_key = self.hash(itemset[item_index])
    #         self.dfs_support_calc(now_node.children[hash_key], itemset, item_index+1)

    # def support_calc(self, dataset):
    #     for transaction in dataset:
    #         itemsets = combinations(transaction, self.max_child_num)
    #         for itemset in itemsets:
    #             self.dfs_support_calc(self.root, itemset, 0)

    def dfs_find_F_table(self, now_node):
        if now_node.isleaf:
            for itemset, cnt in now_node.bucket.items():
                if cnt >= self.min_support:
                    self.frequency_table[itemset] = cnt
        else:
            for child in now_node.children.values():
                self.dfs_find_F_table(child)

    def find_F_table(self, min_support):
        self.min_support = min_support
        self.dfs_find_F_table(self.root)
        return self.frequency_table


def apriori_algorithm(dataset, min_support):
    frequency_table = {}
    gen_frequency_table = None
    itemset_size = 1
    min_support = len(dataset) * min_support
    while True:
        hashtree = HashTree(
            max_child_num=itemset_size,
            max_bucket_num=5
        )
        hashtree.insert_dataset(dataset)
        gen_frequency_table = hashtree.find_F_table(min_support=min_support)
        if not gen_frequency_table:
            break
        if itemset_size != 1:
            for itemset, _ in gen_frequency_table.copy().items():
                sub_sets = combinations(itemset, itemset_size-1)
                for sub_set in sub_sets:
                    if sub_set not in frequency_table:
                        del gen_frequency_table[itemset]
                        break

        frequency_table.update(gen_frequency_table)
        itemset_size += 1
    return frequency_table


if __name__ == "__main__":
    dataset = IBM_data()
    # print(dataset)
    # print(dataset)
    fre_table = apriori_algorithm(dataset=dataset, min_support=0.2)
    rule = generate_rule(fre_table, 0.3)
    # print(rule.keys())