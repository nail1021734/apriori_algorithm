from read_IBM_Data import IBM_data
from itertools import combinations
from generate_rule import generate_rule

def apriori_algorithm(Dataset, min_support):
    min_support = min_support * len(Dataset)
    print(min_support)
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
        frequency_item.update(new_frequency)
    return frequency_item


if __name__ == "__main__":
    dataset = IBM_data()
    f = apriori_algorithm(dataset, min_support=0.2)
    generate_rule(f, 0.3)
