import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pymongo
import unicodedata

def unicodeToAscii(string):
	if string == None:
		return None
	unicodedata.normalize('NFKD', string).encode('ascii','ignore')

def scrapePhonePage(url):
	client = MongoClient('localhost', 27017)
	db = client['gsmarena']
	collection = db['phones_test']
	if collection.find_one({'url': url}) != None:
		return None


	error = False
	page = requests.get(url)
	soup = BeautifulSoup(page.content)
	a = soup.find_all('tr')
	name = soup.find_all('h1', class_='specs-phone-name-title')
	camera = [t.find_all('td')[1] for t in a if len(t.find_all('th')) and t.find_all('th')[0].get_text() == 'Camera']
	battery = [t.find_all('td')[1] for t in a if len(t.find_all('th')) and t.find_all('th')[0].get_text() == 'Battery']
	memory = [t.find_all('td')[1] for t in a if len(t.find_all('td', class_='ttl')) and t.find_all('td', class_='ttl')[0].get_text() == 'Internal']

	try:
		name = name[0].string
	except IndexError:
		name = ""
		error = True
	if not error:
		unicodeToAscii(name)
	error = False

	try:
		camera = camera[0].string
	except IndexError:
		error = True
		camera = 5
	if not error:
		unicodeToAscii(camera)
	error = False

	try:
		battery = battery[0].string
	except IndexError:
		error = True
		battery = 2000
	if not error:
		unicodeToAscii(battery)
	error = False

	try:
		memory = memory[0].string
	except IndexError:
		memory = "10, 1"
		error = True
	if not error:
		unicodeToAscii(memory)
	error = False

	if memory != None:
		memory = [int(s) for s in memory.split() if s.isdigit()]
		ram = min(memory) if len(memory) else 1
		storage = max(memory) if len(memory) else 5
	else:
		ram = 1
		storage = 1

	if camera != None:
		camera = [int(s) for s in camera.split() if s.isdigit()]
		camera = max(camera) if len(camera) else 5
	else:
		camera = 5

	if battery != None:
		battery = [int(s) for s in battery.split() if s.isdigit()]
		battery = max(battery) if len(battery) else 2000
	else:
		battery = 2000

	if int(ram) > 100:
		ram = float(int(ram)/1024)

	if int(storage) > 100:
		storage = float(int(storage)/1024)

	if int(camera) > 20:
		camera = 5

	if int(battery) < 1000:
		battery = 1500

	document = {
		'name':    name,
		'url':     url,
		'camera':  camera,
		'battery': battery,
		'ram':     ram,
		'storage': storage
	}

	return collection.insert_one(document).inserted_id

def scrapeBrandUrls():
	url = 'http://www.gsmarena.com/makers.php3'
	baseurl = 'http://www.gsmarena.com/'
	page = requests.get(url)
	soup = BeautifulSoup(page.content)
	a = soup.find_all('tr')
	urls = [(baseurl + t.find_all('a')[1].get('href')) for t in a]

	client = MongoClient('localhost', 27017)
	db = client['gsmarena']
	collection = db['brands_test']

	document = {
		'brand_urls': urls
	}
	return collection.insert_one(document).inserted_id


def scrapePhoneUrls(url1):
	page = requests.get(url1)
	soup = BeautifulSoup(page.content)
	a = soup.find_all('div', class_='makers')

	urls = a[0].find_all('a')
	urlset = [url.get('href') for url in urls]

	client = MongoClient('localhost', 27017)
	db = client['gsmarena']
	collection = db['phoneurls_test']
	document = {
		'brand_url': url1,
		'phone_urls': urlset
	}
	return collection.insert_one(document).inserted_id if not collection.find_one({'brand_url': url1}) else None

######### Now the main script to download all data
######### first set up the database and define indices

client = MongoClient('localhost', 27017)
db = client['gsmarena']
collection = db['phoneurls_test']
collection.create_index([('brand_url', pymongo.ASCENDING)], unique=True)
collection = db['phones_test']
collection.create_index([('url', pymongo.ASCENDING)], unique=True)

######### Now start filling up the database 

print 'scraping mobile brands'
scrapeBrandUrls()
collection = db['brands_test']
brandurls = collection.find()[0]['brand_urls']

print 'scraping for phone urls for each brand'
for brandurl in brandurls:
	print 'scraping ' + brandurl
	scrapePhoneUrls(brandurl)

collection = db['phoneurls_test']
gsmarena_url = 'http://www.gsmarena.com/'
phoneurls = collection.find()

print 'scraping phone pages'

for i in phoneurls:
	for phurl in i['phone_urls']:
		print 'scraping ' + gsmarena_url + phurl
		scrapePhonePage(gsmarena_url + phurl)







