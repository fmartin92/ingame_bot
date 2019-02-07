from config import *
import ocr, question_class, solvers, time, webbrowser, csv, logging, os
from termcolor import colored

google_url = 'https://www.google.com/search?sclient=psy&hl=en&source=hp&q='
log = ''
clear = lambda: os.system('cls')

def pretty_print(question, method_name):
	clear()
	print(question)
	print()
	scores = getattr(question, method_name+'_scores')
	criteria = solvers.argmin if question.is_negative else solvers.argmax
	correct = criteria(scores)
	max_length = 3+max([len(option.original) for option in question.options])
	for (i, opt) in enumerate(question.options):
		string = opt.original + ' '*(max_length - len(opt.original)) + '|'
		string += '|' * (int(60*scores[i]))
		if i == correct:
			print(colored(string, 'green'))
		else:
			print(string)
	print(method_name, scores)
tic = time.time()
with open('.\\data_experiments\\unprocessed_questions'
			+str(tic)[:10]+'.csv', 'w') as question_file:
	questions_writer = csv.writer(question_file, delimiter=';')
	while True:
		i = input()
		print('Buscando...')
		if i == 'exit':
			break

		tic = time.time()
		data = ocr.read_question()
		question = question_class.Question(data[0], data[1])
		criteria = solvers.argmin if question.is_negative else solvers.argmax
		diff = time.time()-tic

		log += str(question) + '\n'
		log += 'Tiempo demorado en procesar pregunta: ' + str(diff) + '\n'
		clear()
		print(question)
		questions_writer.writerow(
			[question.body.original]
			+ [option.original for option in question.options]
			+ [0])

		tic = time.time()
		try:
			question.body.google_results = question.body.google_search()
			question.naive_google_scores = solvers.naive_google(question)
		except:
			print('Crasheo naive_google')
			logging.exception("message")
			break
		diff = time.time()-tic
		log += 'Tiempo demorado en naive_google: ' + str(diff) + '\n'
		pretty_print(question, 'naive_google')

		tic = time.time()
		try:
			question.body.scraped_sites = question.body.scrape()
			question.scraping_scores = solvers.scraping(question)
			question.naive_and_scraping_avg_scores = \
				solvers.naive_and_scraping_avg(question)
		except:
			print('Crasheo scraping')
			logging.exception("message")
			break
		diff = time.time()-tic
		log += 'Tiempo demorado en scraping: ' + str(diff) + '\n'
		pretty_print(question, 'naive_and_scraping_avg')

tic=time.time()
with open('.\\data_experiments\\log'+str(tic)[:10]+'.txt', 'w') as log_file:
	log_file.write(log)
