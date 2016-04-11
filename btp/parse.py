import operator
f = open('all_deps', 'r')
mp = dict()
sorted_x = list()
sorted_y = list()
def parser(line):
	a = line.find('(')
	b = line.find(')')
	words =line[a+1:b].split(',')
	parts = words[0].split('-')
	first = parts[0]
	parts = words[1].split('-')
	second = parts[0]
	tup = (line[0:a].strip(), first.strip(), second.strip())
	return tup
def get_max_count():
	global sorted_x
	global sorted_y
	for line in f:
		if line.count('CITATION')>0:
			tup = parser(line)
			if tup not in mp:
				mp[tup] = 1
			else:
				mp[tup] += 1
	sorted_x = sorted(mp.items(), key=operator.itemgetter(1))
	sorted_x.reverse()
	mp2 = dict()
	for x in sorted_x[:20]:
		print x[0]
		mp2[x[0][0]] = 1
	sorted_y = sorted(mp2.items(), key=operator.itemgetter(0))
def get_all_features():
	get_max_count()
	features = [0] * 10
	all_features = list()
	f = open('all_deps', 'r')
	for line in f:
		if len(line.strip()) == 0:
			all_features.append(features)
			features = [0] * 10
		if line.count('CITATION')>0:
			for i in range(0,10):
				if sorted_y[i][0] == parser(line)[0]:
					features[i] += 1

	return all_features

