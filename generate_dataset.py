import random


def generate_data(item_num: int, max_set_element: int, data_num: int):
    r"""Generate data."""
    if max_set_element > item_num:
        raise ValueError('`max_set_element` must small than `item_num`.')
    dataset = []
    # Define element list.
    element_list = [i for i in range(item_num)]
    for i in range(data_num):
        # Define this set element number.
        set_element = random.randint(1, max_set_element+1)

        # generate dataset
        dataset.append(set(random.sample(element_list, k=set_element)))

    return dataset
