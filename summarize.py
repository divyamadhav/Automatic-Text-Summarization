import nltk
from nltk.corpus import stopwords
from string import punctuation
from operator import itemgetter

fi = open("input.txt", "r")
text = fi.read()
print(" The original paragraph is : \n")
print(text)
print()
newtext = text.lower()
text = nltk.sent_tokenize(text)

#getting the list of stopwords
stopWords = stopwords.words('english')
pt = list(punctuation)
for i in pt:
	stopWords.append(i)

sent = nltk.sent_tokenize(newtext)

tokens = []
title = sent[0]
titletokens = nltk.word_tokenize(title)
sent = sent[1:]


for i in range(len(sent)):
	words = nltk.word_tokenize(sent[i])
	filtered = []
	for w in words:
		if w not in stopWords:
			filtered.append(w)
	tokens.append(filtered)

#print(" Tokens in the input are : ")
#print(tokens)

#scores for all sentences except title
scores = []
for i in range(len(sent)):
	scores.append([])

#--------------------------------------------------------------------------------------------------------------------------------------
# 1) Sentence Location

scores[0].append(1.0)
scores[1].append(0.8)
scores[2].append(0.6)
scores[3].append(0.4)
scores[4].append(0.2)

for i in range(5, len(sent)):
	scores[i].append(0)

#--------------------------------------------------------------------------------------------------------------------------------------
# 2) Sentence Length

maxlength = max(len(s) for s in sent)
for i in range(len(sent)):
	scores[i].append(len(sent[i])/maxlength)

#--------------------------------------------------------------------------------------------------------------------------------------
# 3) Term Frequency

frequencies = []
maxf = []
for i in range(len(sent)):
	f = []
	for w in tokens[i]:
		freq = 0
		for j in range(len(sent)):
			freq += tokens[j].count(w)
		f.append(freq)
	frequencies.append(f)
	maxf.append(max(f))

maxfreq = max(maxf)

for i in range(len(sent)):
	tf = []
	j = 0
	for w in tokens[i]:
		tf.append(frequencies[i][j]/maxfreq)
	scores[i].append(sum(tf)/len(tf))

#--------------------------------------------------------------------------------------------------------------------------------------
# 4) TF-IDF
# For our examples, TF-IDF is same as TF because we use only one document in corpus

for i in range(len(sent)):
	tf = []
	j = 0
	for w in tokens[i]:
		tf.append(frequencies[i][j]/maxfreq)
	scores[i].append(sum(tf)/len(tf))

#--------------------------------------------------------------------------------------------------------------------------------------
# 5) Sentence resemblence to Title

for i in range(len(sent)):
	count = 0
	for w in titletokens:
		if w in tokens[i]:
			count += 1
	scores[i].append(count/(len(sent[i])+len(titletokens)))

#--------------------------------------------------------------------------------------------------------------------------------------
# 6) Sentence centrality

for i in range(len(sent)):
	count = 0
	for w in tokens[i]:
		c = 0
		for j in range(len(sent)):
			if i!=j :
				if w in tokens[j]:
					c += 1
		if c!=0:
			count += 1
	scores[i].append(count/len(tokens))

#--------------------------------------------------------------------------------------------------------------------------------------
# 7) Sentence inclusion of emphasis words

emphasis = ["very" , "amazingly" , "remarkably" , "especially", "certainly", "crucially", "truly", "really", "exceptionally", "particularly", "specifically", "seriously", "importantly", "surely", "extremely", "incredibly", "absolutely", "quite", "highly", "indeed"]

for i in range(len(sent)):
	count = 0
	for w in tokens[i]:
		if w in emphasis:
			count += 1
	scores[i].append(count/len(sent[i]))

#--------------------------------------------------------------------------------------------------------------------------------------
# 8) Sentence inclusion of name entities

for i in range(len(sent)):
	count = 0
	tags = nltk.pos_tag(tokens[i])
	for a,b in tags :
		if b == "NNP":
			count += 1
	scores[i].append(count/len(sent[i]))

#--------------------------------------------------------------------------------------------------------------------------------------
# 9) Sentence inclusion of numeric data

for i in range(len(sent)):
	count = 0
	for w in tokens[i]:
		if w.isdigit() == True:
			count += 1
	scores[i].append(count/len(sent[i]))

#--------------------------------------------------------------------------------------------------------------------------------------
wt = [14,3,1,5,4,13,12,11,2]
total = []

for i in range(len(sent)):
	s = 0
	for j in range(len(wt)):
		s += wt[j]*scores[i][j]
	total.append(s)

#print(scores)
#print(total)

n = int(input(" How many lines of summary : "))
large = max(total)

final = []
for i in range(len(total)):
	final.append([])
	final[i].append(total[i])
	final[i].append(i)

#print(final)
final.sort()
final.reverse()
final = final[0:n]
#print(final)
final.sort(key=itemgetter(1))
#print(final)

for i in range(n):
	print(text[final[i][1]+1], end='')

print()
