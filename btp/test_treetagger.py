# tagset : https://www.sketchengine.co.uk/penn-treebank-tagset/
import pprint   # For proper print of sequences.
import treetaggerwrapper 
import re
#1) build a TreeTagger wrapper:
tagger = treetaggerwrapper.TreeTagger(TAGLANG='en', TAGDIR = '/usr/', TAGPARFILE = '/usr/bin/english-utf8.par')
line1 = u"Fox ( ) showed that cohesion is held in the vast majority of cases for English-French"
line2 = u"while Cherry and Lin ( ) have shown it to be a strong feature for word alignment"
line3 = u"Inducing features for taggers by clustering has been tried by several researchers ( )."
line4 = u"For example, the likelihood of those generative procedures can be accumulated to get the likelihood of the phrase pair ( )."
line5 = u"Our experimental set-up is modeled after the human evaluation presented in ( )."
line6 = u"We use Conditional Random Fields (CRFs) ( ) to perform this tagging."
line7 = u"Following ( ), we provide the annotators with only short sentences: those with source sentences between 10 and 25 tokens long."
tags = tagger.tag_text(line7)
s = ""
print tags
for tag in tags:
	tg = tag.split('\t')[1]
	pprint.pprint(tg)
	s = s+ tg + ' '

print s
# syntactic features 


patterns = [r".*\(\s\)\sVV[DPZN].*", r".*(VHP|VHZ)\sVV.*", r".*VH[DGPZN]\s(RB\s)*VBN.*",
			r".*MD\s(RB\s)*VB(RB\s)* VVN.*", r"[^IW.]*VB[DPZ]\s(RB\s)*VV[ND].*", 
			r"(RB\s)*PP\s(RB\s)*V.*", r".*VVG\s(NP\s)*(CC\s)*(NP\s).*"]
for pattern in patterns:
	print pattern, re.search(pattern, s)

