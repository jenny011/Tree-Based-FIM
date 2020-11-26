import numpy as np
import matplotlib.pyplot as plt
from os import path

def getData(fpath):
	f = open(fpath, 'r')
	ret = []
	for line in f:
		if line != "\n":
			ret.append(line.rstrip().split(','))
	for i in range(len(ret)):
		ret[i][0] = int(ret[i][0])
		ret[i][1] = float(ret[i][1])
	f.close()
	return ret


def processData(fpath):
	ret = {}
	for i in range(11):
		performance = "performance" + f'{i+1:02}' + '.txt'
		perfpath = path.join(fpath, performance)
		data = getData(perfpath)
		for i in range(len(data)):
			if data[i][0] in ret:
				ret[data[i][0]].append(data[i][1])
			else:
				ret[data[i][0]] = [data[i][1]]
	for k in ret.keys():
		maximum = max(ret[k])
		minimum = min(ret[k])
		ret[k].remove(maximum)
		ret[k].remove(minimum)
	return ret


def calcData(data):
	means = {}
	error = {}
	for k, v in data.items():
		means[k] = np.mean(v)
		error[k] = np.std(v)
	return list(data.keys()), list(means.values()), list(error.values())


def dataForPlot(exp, data):
	fpath = path.join(".", exp, "exp", data)
	raw = processData(fpath)
	return calcData(raw)


def plot(ylabel, x, fpGrowth, efpGrowth, canTree, ecanTree):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_xlabel('minsup(%)', fontsize = 12)
	ax.set_ylabel(ylabel, fontsize = 12)

	# ax.axis([0, 5, 0, 35])
	ax.errorbar(x, fpGrowth, yerr = efpGrowth, color="r", elinewidth=1, capsize=3)
	#ax.errorbar(x, canTree, yerr = ecanTree, color="b", elinewidth=1, capsize=3)
	ax.errorbar(x, canTree, yerr = ecanTree, color="g", elinewidth=1, capsize=3)
	plt.show()



if __name__ == '__main__':
	data = "retail"
	x, fpGrowth, efpGrowth = dataForPlot("fpGrowth", data)
	x, canTree, ecanTree = dataForPlot("canTree", data)

	plot("speed(second)", x, fpGrowth, efpGrowth, canTree, ecanTree)


    # FP-Growth

    # CanTree

    # Freno




