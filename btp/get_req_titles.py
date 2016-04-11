import similarity
f1 = open('mas_found_citations', 'r')
f3 = open('acl_mas_mapping', 'r')
mp = dict()
for line in f3:
	words = line.split()
	if words[0].strip() == 'Not':
		continue
	mp[words[0].strip()] = words[1].strip()
files = ['P07_1001-50.txt', 'P08_1009-50.txt', 'P08_2001-30.txt']
mp_acl = dict()
for fle in files:
	f2 = open('data/'+fle, 'r')
	for line in f2:
		parts = line.split('\t')
		if 'P'+ parts[0].strip()[0:7] not in mp:
			continue
		if mp['P'+parts[0].strip()[0:7]] not in mp_acl:
			mp_acl[mp['P'+parts[0].strip()[0:7]]] = list()		
		mp_acl[mp['P'+parts[0].strip()[0:7]]].append((parts[1], parts[2], parts[-3]))
#print len(mp_acl)
papers = dict()
for line in f1:
	citer = line.split()[1].strip()
	mx_sim = 0
	cor_context = tuple()
	for cit in mp_acl[citer]:
		sim = similarity.get_similarity_cosine(line, cit[0])
		if sim > mx_sim:
			cor_context = cit
			mx_sim = sim
	if len(cor_context)!=3:
		continue
	if mx_sim > 0.5:
		print line.strip() + ' ::: ' + cor_context[0].strip() + ' ::: ' + cor_context[1].strip() + ' ::: ' + cor_context[2].strip() + ' ::: ' + str(mx_sim)
		words = line.split()
		papers[words[0].strip()] = 1
		papers[words[1].strip()] = 1
#print len(papers)
f_p = open("cit_papers_req", "w")
for paper in papers:
	f_p.write(paper.strip() + '\n')
