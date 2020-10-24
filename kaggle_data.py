import pandas as pd


def kaggle_data():
    with open('DataSetA.csv', encoding='utf8') as input_file:
        data = [d.strip().split(',')[:-1] for d in input_file.readlines()]
    return data

if __name__ == "__main__":
    kaggle_data()