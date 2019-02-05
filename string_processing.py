#!/usr/bin/env python
# -*- coding: utf-8 -*-

#para instalar nltk
#pip install nltk
#para las dependencias, dentro del interprete de python:
#>>> import nltk
#>>> nltk.download('stopwords') <- stopwords
#>>> nltk.download('punkt') <- tokenizer

from nltk.corpus import stopwords
from nltk import word_tokenize
from string import punctuation
from difflib import SequenceMatcher

def extract_quoted(s):
	quote = s[s.index('"'):]
	return quote[:quote.index('"')-1]

def get_tokens(s):
	s = s.lower()
	s = s.translate(str.maketrans('', '', punctuation+'¿¡')) #elimina puntuacion
	s = s.translate(str.maketrans('áéíóú','aeiou')) #elimina tildes
	return word_tokenize(s)

def max_overlap(s1,s2):
	# devuelve el largo del mayor substring comun de s1 y s2
    s = SequenceMatcher(None, s1, s2)
    match = s.find_longest_match(0, len(s1), 0, len(s2))
    return match.size
