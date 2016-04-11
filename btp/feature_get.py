#Few imports
import pprint   # For proper print of sequences.
import treetaggerwrapper 
import re
import csv
#from sklearn import svm
import numpy as np
import word2vec_experiments2
import parse
#from sklearn.metrics import precision_recall_fscore_support

# this file contains the feature vector cretion for the lablelled data I got.

mapping = { 'BackGround': 0, 'Fundamental': 1, 'Compare': 2, 'NULL': 3 }
# syntactic features 
patterns = [r".*\(\s\)\sVV[DPZN].*", r".*(VHP|VHZ)\sVV.*", r".*VH[DGPZN]\s(RB\s)*VBN.*",
			r".*MD\s(RB\s)*VB(RB\s)* VVN.*", r"[^IW.]*VB[DPZ]\s(RB\s)*VV[ND].*", 
			r"(RB\s)*PP\s(RB\s)*V.*", r".*VVG\s(NP\s)*(CC\s)*(NP\s).*"]

cues = [
['we' ,'our' ,'us' ,'table' ,'figure' ,'paper' ,'algorithm' ,'here'], 
['many' ,'some' ,'most' ,'several' ,'number of' ,'numerous' ,'variety' ,'range of' ], 
['usually' ,'often' ,'common' ,'commonly' ,'typical' ,'typically' ,'traditional' ,'traditionally' ], 
['recent' ,'recently' ,'prior' ,'previous' ,'early' ], 
['such as' ,'for example' ,'for instance' ,'e.g.', 'example', 'instance' ], 
['may' ,'might' ,'could' ,'would' ,'will' ,'can' ,'should' ], 
['suppose' ,'conjecture' ,'want' ,'possible' ], 
['following' ,'similar to' ,'motivate' ,'inspired' ,'idea' ,'spirit' ], 
['provided by' ,'taken from' ,'extracted from' ,'based on' ,'use' ,'run' ,'apply' ,'extend' ,'measure' ,'evaluate' ,'modify' ,'extract' ], 
['compare' ,'differ' ,'deviate' ,'contrast' ,'exceed' ,'outperform' ,'opposed' ,'consistent with' ,'significant' ], 
['result' ,'accuracy' ,'precision' ,'performance' ,'baseline' ]
]
"""
subject_cue_opt = ['section', 'subsection', 'experiment', 'result', 'work']
quantity_cue_opt = ['various',  'prevalent',  'particularly', 'diverse', 'intensive']
frequency_cue_opt = ['highly', 'generally', 'effectively', 'particularly']
tense_cue_opt = ['promising', 'innovative', 'existing', 'led', 'developing']
example_cue_opt = ['others', 'overview', 'review']
suggest_cue_opt = ['cannot', 'does', 'must']
hedge_cue_opt = ['notice', 'wish', 'conclude', 'remark', 'necessary', 'prove', 'convenient']
idea_cue_opt = ['parallels', 'reformulate', 'alternate']
basis_cue_opt= ['basic', 'build', 'derive', 'adopt']
compare_cue_opt = ['simpler', 'desirable', 'preferred']
result_cue_opt = ['improvement', 'f-measure', 'perplexity']
"""
def add_new_cues():
	global cues
	new_cues = word2vec_experiments2.similar_cues(cues)
	merged_cues = list()
	for i in range(0,len(new_cues)):
		merged_cues.append(new_cues[i]+cues[i])
	cues = merged_cues
	print merged_cues

def textual_features(citation):
	text_feature = list()
	for cue in cues:
		count = 0
		for word in cue:
			count += citation.lower().count(word)
		text_feature.append(count)
	
	return text_feature
	
def physical_features(citation):
	return citation.count('( )')

# syntactic features
def syntactic_features(citation):
	tagger = treetaggerwrapper.TreeTagger(TAGLANG='en', TAGDIR = '/usr/', TAGPARFILE = '/usr/bin/english-utf8.par')
	try:
		tags = tagger.tag_text(u""+citation)
	except UnicodeDecodeError:
		return []
	s = ""
	for tag in tags:
		tg = tag.split('\t')[1]
		s = s+ tg + ' '
	s = s.strip()
	syntactic_feature = [0]*7
	for i in range(0,7):
		if re.search(patterns[i], s) != None:
			syntactic_feature[i] += 1

	return syntactic_feature

def syntactic_features2(tagged_sentence):
	syntactic_feature = [0]*7
	for i in range(0,7):
		if re.search(patterns[i], tagged_sentence) != None:
			syntactic_feature[i] += 1
	return syntactic_feature

class Citation(object):
	"""docstring for Citation"""
	def __init__(self, line):
		parts = line.split('\t')
		self.valid = 0
		if len(parts) > 4:
			self.citation_class = parts[-3]
			self.text_feature = textual_features(parts[1])
			self.syntactic_feature = syntactic_features2(parts[2])
			self.category = parts[-3].strip()
			self.num_citations = parts[1].count('( )')
			if len(self.syntactic_feature) == 7:
				self.valid = 1


def check_right(line):
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
			return False
		line =  line.replace('( )', 'CITATION')
		if len(line.split()) > 70:
			return False
		return True

add_new_cues()
# script to use the above code
count = 0
files = ['P07_1001-50.txt', 'P08_2001-30.txt', 'P08_1009-50.txt']
citations = list()
for fle in files:
	f = open('data/' +fle,'r')
	for line in f:
		citation = Citation(line)
		if citation.valid == 1:
			if check_right(line):
				citations.append(citation)
				
data = list()
target = list()
print len(citations)
new_features = parse.get_all_features()
#print new_features
with open('op_word2vec.csv', 'w') as csvfile:
	csvwriter = csv.writer(csvfile, delimiter = ',')
	fr = list()
	for i in range(0,11):
		fr.append('T'+str(i))
	for i in range(0,7):
		fr.append('S'+str(i))
	for i in range(0,len(new_features[0])):
		fr.append('NF'+str(i))
	fr.append('num_citations')
	fr.append('Class')

	csvwriter.writerow(fr)
	count = 0
	for citation in citations:
		fv = citation.text_feature + citation.syntactic_feature + new_features[count]
		count += 1
		fv.append(citation.num_citations)
		
		fv.append(citation.category)
		data.append(fv[0:-2])
		target.append(citation.category)
		csvwriter.writerow(fv)

"""
 #using svm
clf = svm.SVC()

clf.fit(data, target)

till = 250
a1= target[0:till]
a2= clf.predict(data[0:till])
print precision_recall_fscore_support(a1, a2, average = 'weighted')
count = 0
for i in range(0, till):
	if a1[i] == a2[i]:
		count += 1
print count

f = open('P08_2001-30.txt','r')
citations = list()
for line in f:
	citation = Citation(line)
	if citation.valid == 1:
		citations.append(citation)
data = list()
target = list()
print len(citations)
for citation in citations:
	fv = citation.text_feature + citation.syntactic_feature 
	fv.append(citation.num_citations)
	
	fv.append(citation.category)
	data.append(fv[0:-2])
	target.append(citation.category)

till = 250
a1= target[0:till]
a2= clf.predict(data[0:till])
print precision_recall_fscore_support(a1, a2, average = 'weighted')
count = 0
for i in range(0, till):
	if a1[i] == a2[i]:
		count += 1
print count
"""