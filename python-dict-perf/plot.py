import matplotlib.pyplot as plt
import csv
import sys
import os

def readData(fpaths):
	x = []
	means = []
	errs = []
	for p in fpaths:
		with open(p, 'r') as f:
			reader = csv.reader(f, delimiter=',')
			for row in reader:
				x.append(int(row[0]))
				means.append(float(row[1]))
				errs.append(float(row[2]))

	return x, means, errs


if __name__ == "__main__":
	d = int(sys.argv[1])
	if d:
		datasets = ["retail", "OnlineRetailZZ", "RecordLink", "Skin", "chainstoreFIM", "kosarak", "SUSY"]
		colors = ["red", "blue", "orange", "black", "purple", "green", "pink"]
		for i in range(4, len(datasets)):
			lookup_paths = [os.path.join(os. getcwd(), "results_datasets_same_key", f"lookup_{datasets[i]}.csv")]
			insert_paths = [os.path.join(os. getcwd(), "results_datasets_same_key", f"insert_{datasets[i]}.csv")]

			lookup_x, lookup_means, lookup_errs = readData(lookup_paths)
			plt.errorbar(lookup_x, lookup_means, yerr=lookup_errs, color=colors[i], label=datasets[i] + '_lookup')
			# plt.show()

			insert_x, insert_means, insert_errs = readData(insert_paths)
			plt.errorbar(insert_x, insert_means, yerr=insert_errs, color=colors[i], linestyle="dashdot")

		plt.title(f"Python dictionary performance - datasets")
		plt.xlabel("number of items in dict")
		plt.ylabel("sec/1000 executions")

		plt.legend()
		plt.show()
	else:
		lookup_paths = [os.path.join(os. getcwd(), "results", f"lookup1e{i}.csv") for i in range(4, 8)]
		insert_paths = [os.path.join(os. getcwd(), "results", f"insert1e{i}.csv") for i in range(4, 8)]

		plt.title(f"Python dictionary performance - uniform")
		plt.xlabel("number of items in dict")
		plt.ylabel("sec/1000 executions")

		lookup_x, lookup_means, lookup_errs = readData(lookup_paths)
		plt.errorbar(lookup_x, lookup_means, yerr=lookup_errs, color="blue", label='lookup')
		# plt.show()

		insert_x, insert_means, insert_errs = readData(insert_paths)
		plt.errorbar(insert_x, insert_means, yerr=insert_errs, color="red", label='insert')

		plt.legend()
		plt.show()
