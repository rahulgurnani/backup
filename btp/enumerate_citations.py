f = open('/home/rahul/Desktop/btp/acl_mas_mapping', 'r')
f2 = open('/home/rahul/Public/cited_citer_context_dump', 'r')
papers = dict()
for line in f:
	words = line.split()
	if words[0].strip() != 'Not':
		papers[words[1].strip()] = 1
print len(papers)
f3 = open('/home/rahul/Desktop/btp/mas_found_citations', 'w')
for line in f2:
	words = line.split()
	if words[1].strip() in papers:
		print line.strip()
		f3.write(line.strip() + '\n')
