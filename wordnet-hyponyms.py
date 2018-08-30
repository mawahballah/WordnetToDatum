import nltk
from nltk.corpus import wordnet as wn
import re
import os
from collections import deque
os.chdir(os.getcwd())
from cpyDatumTron import atum, datum, katum, Of, Intersect, Union
doneAntonyms={}
def getExactKatum(synset):
	name=synset.name()
	word=name.split('.')[0]
	wordKatum=wordRoot.find(word)
	if(wordKatum!=None):
		synsetDefinition=synset.definition()
		for instance in wordKatum.I:
			instanceDefinition=definition.of(instance)
			if(instanceDefinition!=None and instanceDefinition.O==synsetDefinition):
				return instance				
	return None

def addHyponyms(synset):	
	exactHypernymKatum=getExactKatum(synset)
	if(exactHypernymKatum!=None):
		for hyponym in synset.hyponyms():
			exactHyponymKatum= getExactKatum(hyponym)
			if exactHyponymKatum!=None:
				exactHyponymKatum._is(exactHypernymKatum,False)

def addExceptions(fileName):
    file=open(fileName,"r")
    for line in file:
        word=line.split(' ')[1]
        exceptionWord=line.split(' ')[0]    
        exceptionKatum = exception.Get(exception.countI + 1)
        wordKatum=wordRoot.Get(word)
        wordKatum._is(exceptionKatum,check=False)
        exceptionKatum.Get(exceptionWord)

def addAntonyms(synset):
	doneAntonyms[synset]=True
	exactSynset=getExactKatum(synset)
	if exactSynset!=None:
		anotnymKatum=antonym.Get(antonym.countI)
		anotnymKatum._is(symmetrical,False)
		exactSynset._is(anotnymKatum,False)
		for anotnym_ in synset.lemmas()[0].antonyms():
			anotnymSynset=getExactKatum(anotnym_.synset())
			if anotnymSynset!=None:
				anotnymSynset._is(anotnymKatum,False)
				doneAntonyms[anotnym_.synset()]=True

katum.load('wordnetonlysynsets.datum', atum())
generalThing = datum.thing
wordnetRoot=generalThing.find("wordnet")
wordRoot=wordnetRoot.find("wordroot")
definition=wordnetRoot.find("definition")
exception = wordnetRoot.Get("exception")
relation=wordnetRoot.Get("relation")
symmetrical=wordnetRoot.Get("symmetrical")
antonym = relation.Get("antonym")

for synset in list(wn.all_synsets()):
	name=synset.name()
	type_=name.split('.')[1]
	if(type_=='s' or type_=='a'or type_=='r'or type_=='v'or type_=='n'):
		if synset.hyponyms()!=None:
			addHyponyms(synset)
		if synset.lemmas()[0].antonyms()!=None:
			if not doneAntonyms.get(synset,False):
				addAntonyms(synset)

addExceptions("noun.exc")
addExceptions("adj.exc")
addExceptions("adv.exc")
addExceptions("verb.exc")
generalThing.save('wordnet-hyponyms-exceptions.datum')
