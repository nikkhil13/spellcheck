from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import re, collections
global NWORDS

def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('C:\Users\NIKKHIL13\Desktop\SpellCheck\spellcheck\\train_data.txt').read()))
#print NWORDS

def home(request):
	return render(request, 'index.html')


alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
	return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(request):
	word = ""
	answer = ""
	word = request.body

	if word.startswith('"') and word.endswith('"'):
		word = word[1:-1]
	word = word.strip()
	if len(word) < 3:
		answer = word
		#answer = answer.strip()
	else:
	#print word
		candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
		answer = max(candidates, key=NWORDS.get)
	answer = answer.strip()
	print len(answer)
	print len(word)
	#print(len(answer))
	return HttpResponse(answer)
	