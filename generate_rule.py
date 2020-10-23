from itertools import combinations

def generate_rule(frequency_table, min_conf, dataset_len):
    rule_set = {}
    for item_set, count in frequency_table.items():
        # print('ori:', item_set)
        if len(item_set) == 1:
            continue
        for length in range(1, len(item_set)):
            subsets = combinations(item_set, length)
            for subset in subsets:
                item_set = list(item_set)
                subset = list(subset)
                item_set.sort()
                subset.sort()
                conf = frequency_table[tuple(item_set)] / frequency_table[tuple(subset)]
                if conf > min_conf:
                    key = tuple([tuple(subset), tuple(set(item_set)-set(subset))])
                    rule_set[key] = tuple([conf, frequency_table[tuple(item_set)]/dataset_len])
    table = rule_set
    table = sorted(table.items(), key=lambda x: x[1][0])
    for key, value in table:
        print(key[0], '=>', key[1], ': conf:', value[0],', sup:', value[1])
    print(len(rule_set))
    return rule_set