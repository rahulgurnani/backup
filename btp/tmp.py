f = open('50_min_count', 'r')
al = list()
for line in f:
	if len(line.strip()) == 0:
		print al
		al = []
		continue
	al.append(line.strip())