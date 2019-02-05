from config import *
import ocr, question_class, solvers, time, webbrowser

google_url = 'https://www.google.com/search?sclient=psy&hl=en&source=hp&q='

while True:
	input()
	total_time = 0
	tic = time.time()
	data = ocr.read_question()
	question = question_class.Question(data[0], data[1])
	criteria = solvers.argmin if question.is_negative else solvers.argmax
	diff = time.time()-tic
	total_time += diff
	print(diff)
	print()
	print(question)

	#webbrowser.open(str(google_url + question.body.original))

	tic = time.time()
	print()
	#print('Naive google dice:')
	question.body.google_results = question.body.google_search()
	score = solvers.naive_google(question)
	#print(score)
	if max(score) < 0.65:
		print('DUDOSO:', question.options[criteria(score)].original)
		tic = time.time()
		print()
		#print('Scraping dice:')
		self.question.body.scraped_sites = self.question.body.scrape()
		score = solvers.scraping(question)
		if max(score) < 0.65:
			print('DUDOSO', question.options[criteria(score)].original)
		else:
			print(question.options[criteria(score)].original)
		diff = time.time()-tic
		total_time += diff
	else:
		print(question.options[criteria(score)].original)
		#diff = time.time()-tic
		#total_time += diff
		#print(diff)


	#print(diff)
	#print()
	#print('Tiempo total: ', total_time)
