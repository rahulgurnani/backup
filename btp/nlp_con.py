f = open('nlp_cits', 'r')
import re

def replace_citations(line):
	capital_letter = '[A-Z][A-Z]+'
	for m in re.finditer(capital_letter,line):
		line = re.sub(m.group(), m.group().lower(), line)
	bracketed_year = '(\((19|20)[0-9][0-9]\)))'
	year = "(((19|20)[0-9][0-9])" + "|" +bracketed_year
	space = '\s'
	bracketed_cit_opt = '((\s)*\[[0-9,\s]+\])*'
	comma_opt = '(,)*'
	space_opt = '(\s)*'
	author_name = "([A-Z][A-Za-z]+)"
	author_full_name = '(' + author_name + space_opt + ')+'
	authors = author_full_name + '('+  space_opt +comma_opt + space_opt + author_full_name + space_opt +')*'  + '(' + space_opt +'and' + space_opt + author_full_name + space_opt +')*'
	etal_opt = "(et al.)*"
	regex1 =  authors + space_opt +  etal_opt + comma_opt + space_opt + year + bracketed_cit_opt
	pat1 = re.compile(regex1)
	m = re.findall(year, line)
	if len(m)!=0:
		line = re.sub(pat1,'CITATION', line)
	regex2 = '\[[0-9,\s]+\]'
	pat2 = re.compile(regex2)
	line = re.sub(pat2, 'CITATION', line)
	return line

#print replace_citations('17406 5168266 Being the association measure value associated to each n-gram, the only feature available to the system in order to extract multiword lexical unit candidates, most of the approaches proposed in the literature have based their selection process on association measure thresholds like in Church (1990), Daille (1995), Smadja (1996) and Shimohata (1997)')
#print replace_citations(' Recently, Recchia and Jones (2009) compared the performance of LSA to the much simpler technique of pointwise mutual information (PMI; Church  CITATION) as a function of corpus size, while controlling for a host of potential confounds (see also Bullinaria  CITATION)')
#print replace_citations('For example, Bollegala et al. (2007) proposed to measure word similarity using text snippets returned by Web search engines')
f2 = open('final_nlp_cits', 'w')
for line in f:
	line = ' '.join(line.split()[2:])
	f2.write(replace_citations(line).strip() + '\n')

#line  ='205507 {[SECTION]}3. ANALYSIS OF LEARNING PROCESS Morgan'
#print replace_citations(line)