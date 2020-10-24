from read_IBM_Data import IBM_data
from itertools import combinations
from generate_rule import generate_rule
from tqdm import tqdm
from kaggle_data import kaggle_data
import time
import matplotlib.pyplot as plt

def apriori_algorithm(Dataset, min_support):
    min_support = min_support * len(Dataset)
    # print(min_support)
    max_len = max([len(data) for data in Dataset])
    frequency_item = {}
    for i in range(1, max_len+1):
        new_frequency = {}
        for data in Dataset:
            itemset = combinations(data, i)
            for items in itemset:
                items = list(items)
                items.sort()
                items = tuple(items)
                if items in new_frequency:
                    new_frequency[items] += 1
                else:
                    items_subset = combinations(items, i-1)
                    subset_exist = True
                    for subset in items_subset:
                        subset = list(subset)
                        subset.sort()
                        subset = tuple(subset)
                        if subset not in frequency_item:
                            subset_exist = False
                            break
                    if subset_exist or i == 1:
                        new_frequency[items] = 1
        for key, value in new_frequency.copy().items():
            if value < min_support:
                del new_frequency[key]
        if new_frequency == {}:
            break
        else:
            frequency_item.update(new_frequency)
    return frequency_item

# def apriori_algorithm2(Dataset, min_support):
#     min_support = min_support * len(Dataset)
#     # print(min_support)
#     max_len = max([len(data) for data in Dataset])
#     frequency_item = {}
#     last_new_frequency = None
#     for i in range(1, max_len+1):
#         new_frequency = {}
#         itemset = set()
#         if i == 1:
#             for transaction in Dataset:
#                 for item in transaction:
#                     if item in new_frequency:
#                         new_frequency[item] += 1
#                     else:
#                         new_frequency[item] = 1
#             frequency_item.update(new_frequency)
#             last_new_frequency = new_frequency
#         else:
#             # print(last_new_frequency)
#             for key, value in last_new_frequency.items():
#                 if type(key) == int:
#                     itemset.add({key})
#                 else:
#                     itemset.add(set(key))
#             itemset = combinations(itemset, i)

#             for items in itemset:
#                 for transaction in Dataset:
#                     items = list(items)
#                     items.sort()
#                     items = tuple(items)
#                     if items in new_frequency:
#                         new_frequency[items] += 1
#                     else:
#                         items_subset = combinations(items, i-1)
#                         subset_exist = True
#                         for subset in items_subset:
#                             subset = list(subset)
#                             subset.sort()
#                             subset = tuple(subset)
#                             if subset not in frequency_item:
#                                 subset_exist = False
#                                 break
#                         if subset_exist or i == 1:
#                             new_frequency[items] = 1
#             for key, value in new_frequency.copy().items():
#                 if value < min_support:
#                     del new_frequency[key]
#             if new_frequency == {}:
#                 break
#             else:
#                 frequency_item.update(new_frequency)
#                 last_new_frequency = new_frequency
#     return frequency_item


if __name__ == "__main__":
    timelist = []
    suplist = []
    dataset = kaggle_data()
    # print(dataset)
    for c in tqdm(range(2, 20, 1)):
        timelist.append([])
        suplist.append([])
        for s in range(2, 20, 1):
            # Set min support and conf
            sup = s / 20
            conf = c / 20
            # print(sup)
            # Run FP_Growth
            start = time.time()
            frequency_table = apriori_algorithm(dataset, sup)
            rule = generate_rule(frequency_table, conf, len(dataset))
            total_time = time.time()-start

            # Record time
            timelist[-1].append(total_time)
            suplist[-1].append(sup)

            # Save result
            frequency_table = sorted(frequency_table.items(), key=lambda x:x[1])
            with open(f'log/s_{sup:.3f}_c_{conf:.3f}.txt','w',encoding='utf8') as output_file:
                for key, value in frequency_table:
                    # print(f'{value} : {key}')
                    output_file.write(f'{value} : {key}\n')

                rule = sorted(rule.items(), key=lambda x: x[1][0])
                for key, value in rule:
                    # print(f'{key[0]} => {key[1]} : conf:{value[0]}, support{value[1]}')
                    output_file.write(f'{key[0]} => {key[1]} : conf:{value[0]}, support{value[1]}\n')

        # Draw graph
        plt.plot(suplist[-1], timelist[-1],label = f'conf = {conf:.3f}')
    plt.legend()
    plt.xlabel('support')
    plt.ylabel('time')
    plt.show()
    # dataset = IBM_data()
    # f = apriori_algorithm(dataset, min_support=0.1)
    # print(generate_rule(f, 0.3,len(dataset)))
