import pandas as pd
from tqdm import tqdm
import pickle
import random
import pickle
import json
from task4function import *
with open('tree.bin','rb') as f:
    tree = pickle.load(f)

def main():
    data = pd.read_csv('Task4_database.csv').values.tolist()
    # data = pd.read_csv('Task4_database.csv').values.tolist()
    saver = {}
    print("over")
    for row in tqdm(data[200:300]):
        saver[tuple(row)] = tree.query(row[1:],3)
        if saver[tuple(row)]:
            print(saver[tuple(row)])
    with open('result2.bin','wb') as f:
        pickle.dump(saver,f)

if __name__ == '__main__':
    main()
