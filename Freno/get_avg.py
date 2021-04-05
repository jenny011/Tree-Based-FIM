import csv
import numpy as np

def get_avg(fpath):
    s = []
    with open(fpath, 'r') as fperf:
        reader = csv.reader(fperf)
        for row in reader:
            s.append(float(row[1]))
    return np.mean(s)

if __name__ == "__main__":
    for i in range(1,5):
        print(i, get_avg(f'retail_perf0{i}.csv'))
