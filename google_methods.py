import requests
from config import *
from googleapiclient.discovery import build
#seguir los pasos de https://stackoverflow.com/questions/37083058/programmatically-searching-google-in-python-using-custom-search
#from googlesearch import search
#pip install google
from bs4 import BeautifulSoup
#pip install beautifulsoup4
from google import google
#pip install git+https://github.com/abenassi/Google-Search-API

class Google_Result:
	def __init__(self, title, snippet, url):
		self.title = title
		self.snippet = snippet
		self.url = url

def api_search(query):
	#quizas no es buena idea inicializar el servicio cada vez que se corre esto
	service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
	results = service.cse().list(q=query, cx=GOOGLE_CSE_ID, lr='lang_es',
									num=MAX_GOOGLE_RESULTS).execute()
	try:
		return [Google_Result(item['title'], item['snippet'], item['link'])
					for item in results['items']]
	except: #esto crashea si no hay resultados
		return []

def non_api_search(query):
	results = google.search(query, lang='es')
	return [Google_Result(item.name, item.description, item.link)
				for item in results]

def search(query):
	return api_search(query) if USE_GOOGLE_API else non_api_search(query)

def scrape(url):
	# titulo + texto de una webpage
	hdr = {'User-Agent': 'Mozilla/5.0'}
	#req = urllib2.Request(url,headers=hdr)
  	#page = urllib2.urlopen(req)
	try:
		page = requests.get(url).text
		soup = BeautifulSoup(page, "html.parser")
		for script in soup(["script", "style"]):
			script.decompose()    # rip it out
		text = soup.get_text()
		# break into lines and remove leading and trailing space on each
		lines = (line.strip() for line in text.splitlines())
		# break multi-headlines into a line each
		chunks = (phrase.strip() for line in lines
						for phrase in line.split("  "))
		# drop blank lines
		text = '\n'.join(chunk for chunk in chunks if chunk)
		return (soup.title.text + " \n " + text )
	except:
		return ''
