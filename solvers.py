import string_processing
from config import *
import google_methods

def argmax(l):
	return l.index(max(l))

def argmin(l):
	return l.index(min(l))

def no_data():
	return [1/float(N_OPTIONS)] * N_OPTIONS

def normalize_by_average(scores):
	#no quiero dividir por cero al normalizar si no hay resultados
	if scores == [] or sum(scores) == 0:
		scores = no_data()
	else:
		scores = [score/sum(scores) for score in scores]
	return scores

def count_occurences(haystack, needles):
	if WEIGHTED_SEARCH and len(needles)!=0:
		return len([item for item in haystack if item in needles])/len(needles)
	else:
		return len([item for item in haystack if item in needles])

def matches_in_google_result(google_result, needles):
	r_tokens = string_processing.get_tokens(google_result.snippet
												+ ' ' + google_result.title)
	return count_occurences(r_tokens, needles)

#### D solvers:

def naive_google(question):
	#accepts a question with non-empty question.body.google_results
	scores = []
	for option in question.options:
		matches = sum([matches_in_google_result(result, option.processed)
								for result in question.body.google_results])
		scores.append(matches)
	return normalize_by_average(scores)

def scraping(question):
	#accepts a question with non-empty question.body.scraped_sites
	scores = []
	for scraped_site in question.body.scraped_sites:
		scraped_words = string_processing.get_tokens(scraped_site)
		scores.append([count_occurences(scraped_words, option.processed)
							for option in question.options])
	#esta magia suma por fila. por ej sobre [[1,2],[3,4]] da [4,6]
	scores = [sum(i) for i in zip(*scores)]
	return normalize_by_average(scores)

def simple_decision_tree(question):
	#accepts a question with non-empty question.body.google_results,
	#question.body.scraped_sites
	scores = naive_google(question)
	if max(scores) < 0.5:
		scores = scraping(question)
	return scores

#### O solvers:

def O_googling(question):
	#accepts a question with options having non-empty
	#question.option.google_results
	scores = []
	#para esto quiero romper las comillas
	question.body.totally_processed = question.body.process()
	for option in question.options:
		scores.append(sum([matches_in_google_result(result,
								question.body.totally_processed)
								for result in option.google_results]))
	return scores

def O_scraping(question, include_body=True):
	#accepts a question with options having non-empty
	#question.option.scraped_sites
	scores = []
	for option in question.options:
		needles = option.processed
		if include_body:
			needles += question.body.processed
		scraped_text = string_processing.get_tokens(option.scraped_sites[0])
		scores.append(sum([count_occurences(scraped_text, needles)]))
	return scores
