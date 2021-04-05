import matplotlib.pyplot as plt
import numpy as np
import csv

def readData(fpath):
    d = {}
    with open(fpath, 'r') as f:
         csv_reader = csv.reader(f, delimiter=',')
         for row in csv_reader:
             k = int(row[0])
             v = float(row[1])
             if k in d:
                 d[k].append(v)
             else:
                 d[k] = [v]
    for k in d.keys():
        d[k] = np.mean(d[k])
    return d

data = readData("retail_perf_cache.csv")
plt.plot([k for k in data.keys()], [v for v in data.values()])
plt.show()
