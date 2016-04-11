# this file adds title similarity as a feature to the feature set and generates a file for weka to work on 
import feature_get
import similarity
import csv
f1 = open('title_contexts', 'r')
paper_dict = dict()
f2 = open('index_title_map', 'r')
for line in f2:
	parts = line.split(' :: ')
	paper_dict[parts[0].strip()] = (parts[1].strip(), parts[2].strip())
count = 0
all_cits_features = list()
#feature_get.add_new_cues()
for line in f1:
	parts = line.split(' ::: ')
	cit = parts[1].strip()
	pos_cit = parts[2].strip()
	category = parts[3].strip()
	i1 = parts[0].split()[0].strip()
	i2 = parts[0].split()[1].strip()
	if i1 in paper_dict:
		t1 = paper_dict[i1][0]
		t2 = paper_dict[i2][0]
		c1 = paper_dict[i1][1]
		c2 = paper_dict[i2][1]
		same = 0
		if c1.strip() == c2.strip():
			same = 1
		sim = similarity.get_similarity_cosine(t1, t2)
		t = list()
		t.append(same)
		t.append(round(sim,2))
		features = feature_get.textual_features(parts[1]) + feature_get.syntactic_features2(parts[2]) + t 
		features.append(parts[-2].strip())
		all_cits_features.append(features)
		print features
	count += 1
	print  category

with open('weka_op_w2v.csv', 'w') as csvfile:
	csvwriter = csv.writer(csvfile, delimiter = ',')
	fr = list()
	for i in range(0,11):
		fr.append('T'+str(i))
	for i in range(0,7):
		fr.append('S'+str(i))
	fr.append('same')
	fr.append('similarity')
	fr.append('Class')
	csvwriter.writerow(fr)
	for feature in all_cits_features:
		print 'feature', feature
		csvwriter.writerow(feature)
	
print count