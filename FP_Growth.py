from generate_dataset import generate_data
from itertools import combinations
from generate_rule import generate_rule
from read_IBM_Data import IBM_data


class Node:
    def __init__(self, parent, item, frequency):
        self.children = []
        self.parent = parent
        self.item = item
        self.frequency = frequency
        self.nodelink = None


class Tree:
    def __init__(self, min_supprot, data_size):
        r"""
        frequency_table={'item' : 'frequency'}
        """
        self.root = Node(parent=None, item=None, frequency=0)
        self.frequency_table = {}
        # self.min_supprot = min_supprot
        self.header_table = {}
        self.data_size = data_size
        self.min_supprot = min_supprot * data_size
        # h_keys = list(frequency_table.keys())
        # self.sorted_header = sorted(
        #     h_keys,
        #     key=lambda x : frequency_table[x],
        #     reverse=True
        # )

    def sort_transaction(self, transaction):
        return sorted(
            transaction,
            key=lambda x: self.frequency_table[x],
            reverse=True
        )

    def create_FPTree(self, dataset):
        # Count item frequency.
        for transaction in dataset:
            for item in transaction:
                if item not in self.frequency_table:
                    self.frequency_table[item] = 1
                else:
                    self.frequency_table[item] += 1
        # Delete the item that frequency less than min support.
        for item, value in self.frequency_table.copy().items():
            if value < self.min_supprot:
                del self.frequency_table[item]

        for transaction in dataset:
            for item in transaction.copy():
                if item not in self.frequency_table.keys():
                    transaction.remove(item)
            t = self.sort_transaction(transaction)
            self.insert_sorted_transaction(
                now_node=self.root, transaction=t, index=0)

    def insert_sorted_transaction(self, now_node, transaction, index):
        if index == len(transaction):
            return

        # If child has this item.
        for child in now_node.children:
            if transaction[index] == child.item:
                child.frequency += 1
                self.insert_sorted_transaction(
                    now_node=child,
                    transaction=transaction,
                    index=index+1
                )
                return

        # If child no this item.
        new_node = Node(parent=now_node, item=transaction[index], frequency=1)
        now_node.children.append(new_node)

        # Add new node to header table
        if transaction[index] not in self.header_table.keys():
            self.header_table[transaction[index]] = new_node
        else:
            cur_node = self.header_table[transaction[index]]
            while cur_node.nodelink is not None:
                cur_node = cur_node.nodelink
            cur_node.nodelink = new_node

        self.insert_sorted_transaction(
            now_node=new_node, transaction=transaction, index=index+1)
        return

    def dfs(self, node):
        for child in node.children:
            print(child.item, ':', child.frequency)
            self.dfs(child)
        return

    def find_frequency_patten(self):
        frequency_pattern = {}
        key_list = list(self.frequency_table.keys())
        key_list = sorted(key_list, key=lambda x: self.frequency_table[x])

        for item in key_list:
            now_node = self.header_table[item]
            now_node_frequency = now_node.frequency
            while now_node is not None:
                prefix = []
                up_node = now_node.parent
                while up_node.parent is not None:
                    prefix.append(up_node.item)
                    up_node = up_node.parent
                for i in range(len(prefix)+1):
                    element_sets = combinations(set(prefix), i)
                    for element_set in element_sets:
                        element_set = list(element_set)
                        element_set.append(item)
                        element_set.sort()
                        # print('item', item, ',element:', element_set)
                        element_set = tuple(element_set)
                        if element_set in frequency_pattern.keys():
                            frequency_pattern[element_set] += now_node.frequency
                        else:
                            frequency_pattern[element_set] = now_node.frequency
                now_node = now_node.nodelink

            for key, value in frequency_pattern.copy().items():
                if value < self.min_supprot:
                    del frequency_pattern[key]
        return frequency_pattern


if __name__ == "__main__":
    dataset = IBM_data()
    tree = Tree(min_supprot=0.39, data_size=len(dataset))
    tree.create_FPTree(dataset)
    tree.dfs(tree.root)
    print(tree.find_frequency_patten())
    table= tree.find_frequency_patten()
    table = sorted(table.items(), key=lambda x:x[1])
    for key, value in table:

        print(key, ':', value)
    rule = generate_rule(tree.find_frequency_patten(), 0.6, len(dataset))
