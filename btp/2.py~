import gensim
import re
files = ['P07_1001-50.txt', 'P08_1009-50.txt', 'P08_2001-30.txt']
cues = [['we' ,'our' ,'us' ,'table' ,'figure' ,'paper' ,'algorithm' ,'here'], ['many' ,'some' ,'most' ,'several' ,'number of' ,'numerous' ,'variety' ,'range of' ], ['usually' ,'often' ,'common' ,'commonly' ,'typical' ,'typically' ,'traditional' ,'traditionally' ], ['recent' ,'recently' ,'prior' ,'previous' ,'early' ], ['such as' ,'for example' ,'for instance' ,'e.g.' ], ['may' ,'might' ,'could' ,'would' ,'will' ,'can' ,'should' ], ['suppose' ,'conjecture' ,'want' ,'possible' ], ['following' ,'similar to' ,'motivate' ,'inspired' ,'idea' ,'spirit' ], ['provided by' ,'taken from' ,'extracted from' ,'based on' ,'use' ,'run' ,'apply' ,'extend' ,'measure' ,'evaluate' ,'modify' ,'extract' ], ['compare' ,'differ' ,'deviate' ,'contrast' ,'exceed' ,'outperform' ,'opposed' ,'consistent with' ,'significant' ], ['result' ,'accuracy' ,'precision' ,'performance' ,'baseline' ]]

final_sentences = list()
for fle in files:
	f = open(fle, 'r')
	for line in f:
		cit = str()
		cit = line.split('\t')[1]
		cit = cit.replace('( )', 'CITATION')
		cit = re.sub(r'[^\x00-\x7F]+',' ', cit)
		final_sentences.append(cit)
f2 = open('all_citations', 'w')
for sent in final_sentences:
	f2.write(sent.strip() + '\n')

sentences = gensim.models.word2vec.LineSentence('all_citations')
print "1"
model = gensim.models.Word2Vec(sentences, size = 10, min_count = 10)
print "2"	
temp_positive_cue = []
for word in cues[1]:
	if word in model.vocab.keys():
		temp_positive_cue.append(word)

temp_negative_cue = []
for i in range(0, 11):
	if i == 1: 
		continue
	for word in cues[i]:
		if word in model.vocab.keys():
			temp_negative_cue.append(word)
print temp_positive_cue, temp_negative_cue
print ""
print model.most_similar(positive = ['precision', 'accuracy', 'result'])
