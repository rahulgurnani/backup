import gensim
import re
import nltk

files = ['all_citations', 'final_nlp_cits_w2v']
sentences = gensim.models.word2vec.LineSentence('final_nlp_cits_w2v')
#model = gensim.models.Word2Vec(sentences, size = 10, min_count = 50)
#model.save('model1')
model = gensim.models.Word2Vec.load('model1')

def all_present(cue):
	temp_cue = list()
	for word in cue:
		if word in model.vocab.keys():
			temp_cue.append(word)
	return temp_cue
def similar_cues(cues):
	count = 0
	all_new_cues = list()
	for cue in cues:
		new_cue = list()
		sim_words = model.most_similar(positive = all_present(cue), topn=20)
		for word in sim_words:
			w1 = nltk.word_tokenize(word[0])
			if w1[0].lower() not in cue and len(w1[0])>1:
				new_cue.append(str(w1[0].lower()))
		all_new_cues.append(new_cue)
		count += 1
	return all_new_cues

#print similar_cues()