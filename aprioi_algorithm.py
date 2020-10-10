from generate_dataset import generate_data


def support_calc(dataset, L):
    result = []
    for subset in L:
        count = 0
        for data in dataset:
            if subset.issubset(data):
                count+=1
        result.append({
            'set' : subset,
            'sup' : count
        })
    return result


# def conf_calc(data, C):
#     return result

# def lift_calc(data):

# def aprioi_algorithm(dataset, min_support, min_conf):
#     result_itemset=[]



if __name__ == "__main__":
    dataset = generate_data(3, 2, 3)
    for i in dataset:
        print(i)
    L = [{0,1},{1},{2}]
    print(support_calc(dataset,L))

