import re
import collections

def IBM_data():
    dataset = {}
    with open('ibm-5000.txt', 'r', encoding='utf8') as input_file:
        data = [re.sub(r'\s+', ' ', d) for d in input_file.readlines()]
    data = [d.strip().split(' ')[1:] for d in data]
    # print(data)
    for i in data:
        if i[0] in dataset:
            dataset[i[0]].append(i[1])
        else:
            dataset[i[0]] = [i[1]]
        # print([item for item, count in collections.Counter(i).items() if count > 1])
    # for i in list(dataset.values()):
    #     print(i)
    # print(type(list(dataset.values())[0]))
    return list(dataset.values())
