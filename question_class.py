import string_processing, google_methods
from nltk.corpus import stopwords
from config import *
from threading import Thread

quantifiers = ['ultimo', 'ultima', 'grande', 'mayor', 'pequeño', 'pequeña',
				'menor','extenso', 'extensa', 'largo', 'larga', 'primero',
				'primera']

class Question_Part:
	def google_search(self):
		return google_methods.search(' '.join(self.processed))

	def scrape(self, n=5, timeout=1):
		urls = [resultado.url for resultado in self.google_results][:n]
		results = []
		def append_result(url):
			results.append(google_methods.scrape(url))
		threads = [Thread(target=append_result, args=(url,)) for url in urls]
		for thread in threads:
			thread.start()
		for thread in threads:
			thread.join(timeout)
		return results

	def find_wiki_article(self):
		for result in self.google_results:
			if 'es.wikipedia.org' in result.url:
				return result.url
		return ''

	def process(self, tokenize_quotes=False):
		tokens = string_processing.get_tokens(self.original)
		stop_words = stopwords.words('spanish')
		filtered = [word for word in tokens if word not in stop_words]

		#normalmente las comillas aparecen encerrando titulos o cosas que
		#quiero googlear verbatim; en ese caso extraigo todo el quote como un
		#solo token y elimino las repeticiones
		if tokenize_quotes and '"' in self.original:
			quote = string_processing.extract_quoted(self.original)
			quote_tokens = string_processing.get_tokens(quote)
			filtered = [word for word in filtered
							if word not in quote_tokens] + [quote]

		return filtered

	def __init__(self, text, tokenize_quotes=False, get_queries=False):
		text.translate(str.maketrans('“”','""'))
		self.original = text
		self.processed = self.process(tokenize_quotes)
		if get_queries:
			self.google_results = self.google_search()
			self.scraped_sites = self.scrape()

class Question:
	def classify(self):
		if [word for word in self.body.processed if word in quantifiers] != []:
			return 'C'
		if 'cuál de ' in self.body.original.lower():
			return 'O'
		return 'D'

	def __str__(self):
		return self.body.original + '\n' + ' - '.join([opt.original
													for opt in self.options])

	def __repr__(self):
		return self.body.original + '\n' + ' - '.join([opt.original
													for opt in self.options])

	def decide_negative(self):
		lowered = self.body.original.lower()
		if ' no ' in lowered or ' nunca ' in lowered:
			quotes = ''
			if '"' in lowered:
				quotes = string_processing.extract_quoted(lowered)
			if ' no ' in quotes or ' nunca ' in quotes:
				return False
			else:
				return True
		else:
			return False

	def __init__(self, body, options):
		self.body = Question_Part(body, tokenize_quotes=True)
		self.options = [Question_Part(option) for option in options]

		#esto elimina las palabras compartidas por todas las opciones
		shared_tokens = []
		for option_token in self.options[0].processed:
			shared = True
			for option in self.options:
				if option_token not in option.processed:
					shared = False
			if shared:
				shared_tokens.append(option_token)
		for option in self.options:
			option.processed = [token for token in option.processed
										if token not in shared_tokens]
		self.question_type = self.classify()
		self.is_negative = self.decide_negative()
