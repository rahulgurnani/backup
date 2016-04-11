import re
import nltk
files = ['P07_1001-50.txt', 'P08_1009-50.txt', 'P08_2001-30.txt']
count = 0

for fle in files:
	f = open('data/'+fle, 'r')
	for line in f:
		if count%100 == 0:
			f2 = open('data/dep_contexts_'+str(count/100), 'w')
		parts = line.split('\t')
		author = '[A-Z]+[a-z-]+'
		space_opt = '(\s)*'
		et_al = 'et al.'
		s = author + space_opt + et_al
		pat1 = re.compile(s)
		line = re.sub(pat1, 'Scientists ',parts[1])
		pat2 = re.compile('e.g.')
		line2 = re.sub(pat2, 'example', line)
		pat2 = re.compile('eg.')
		line = re.sub(pat2, 'e.g.', line)
		pat2 = re.compile('i.e.')
		line2 = re.sub(pat2, 'that is', line2)
		pat2 = re.compile('i.e')
		line2 = re.sub(pat2, 'that is', line2)
		pat2 = re.compile('cf.')
		line2 = re.sub(pat2, 'SOMEThing', line2)
		pat2 = re.compile('etc.')
		line2 = re.sub(pat2, 'exectra', line2)
		pat3 = re.compile('[0-9]+(\.[0-9]+)*')
		line3 = re.sub(pat3, 'Number',line2)
		if line3.count('.') >0 or line3.count('?') > 0:
			continue
		line =  line.replace('( )', 'CITATION')
		if len(line.split()) > 70:
			continue
		if line[-1]!='.':
			line = line.strip() + ' . '
		else:
			print line
		f2.write(line.strip() + '\n')
		count += 1

print count
		#print line
