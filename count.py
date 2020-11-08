f = open('FP-Growth/insert.txt', 'r')
t = []
for line in f:
	t.append(float(line))
f.close()
print(len(t))
print(sum(t)/len(t))

'''
Can
88162
0.00017913555953445376

FP
88162
5.881319742437927e-06
'''