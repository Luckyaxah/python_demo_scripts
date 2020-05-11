import lxml.html
import requests
import html,time,csv
import chardet
import pandas as pd
from urllib import robotparser
import urllib.request as urllib2
import re

# urllib2在pyhton3中变为urllib.request

rp = robotparser.RobotFileParser()
rp.set_url('https://www.dytt8.net/robots.txt')
rp.read()
# page.encoding = 'gbk'

def download(url, user_agent='wswp', num_retries =2):
	print('Downloading:', url)
	headers = {'user_agent': user_agent}
	request = urllib2.Request(url, headers = headers)
	try:
		html = urllib2.urlopen(request).read().decode('GBK','ignore')
	except urllib2.URLError as e:
		print('Download error:', e.reason)
		html = None
		if num_retries > 0:
			if hasattr(e, 'code') and 500 <= e.code < 600 :
				# retry 5XX HTTP errors
				return download(url, user_agent, num_retries - 1)

	return html


class Throttle:
	"""
	Add a delay between downloads to the same domain
	"""
	def __init(self, delay):
		self.delay = delay
		self.domains = {}

	def wait(self, url):
		domain = urlparse.urlparse(url).netloc
		if self.delay > 0 and last_accessed is not None:
			sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
			if sleep_secs > 0:
				# domain has been accessed recently
				# so need to sleep
				time.sleep(sleep_secs)
		# update the last accessed time
		self.domains[domain] = datetime.datetime.now()

def get_link():

	# url = 'http://www.ygdy8.net/html/gndy/oumei/list_7_{}.html'
	url = 'http://www.ygdy8.net/html/gndy/rihan/list_6_{}.html'

	data = {}
	name = []
	# film_url = []
	# for n in range(1,207):
	for n in range(1,36):
		html_text = download(url.format(str(n)))
		time.sleep(1)
		tree = lxml.html.fromstring(html_text) # parse the HTML
		fixed_html = lxml.html.tostring(tree ,pretty_print=True)

		td = tree.cssselect('a.ulink')
		# print(fixed_html)
		print(len(td))
		for td_one in td:

			if td_one.attrib['href'] not in ["/html/gndy/jddy/index.html","/html/gndy/dyzz/index.html"]:
				name.append([td_one.text_content(),td_one.attrib['href'],n])
				# film_url.append(td_one.attrib['href'])
			# print(td_one.text_content())
			# print(td_one.attrib['href'])
		# data["{}".format(n)]=[name,film_url]	
	CSV_columnName=['title','ref_url','page']

	writer = pd.DataFrame(columns = CSV_columnName, data = name)
	writer.to_csv('/Users/leqi/Desktop/dytt_film_rihan.csv',encoding ='UTF-8')
	# print(name)
	# writer.writerow(name)

	# print(data)


	# print(dir(td[0]))
	# print(len(td))
	# print(type(td[0]))
	# movie_info = td[19].text_content()
	# print(movie_info)
	# print(html_text)
def get_score():
	root_link = 'http://www.ygdy8.net'
	# movie_ref_link = '/html/gndy/jddy/index.html'
	# url = root_link+movie_ref_link
	df = pd.read_csv('/Users/leqi/Desktop/dytt_film_rihan.csv')
	score_list = []
	# for i in range(0,5150):
	for i in range(0,870):
	# for i in range(0,1):
		url = root_link+df['ref_url'][i]

		# print(df['ref_url'][i])
		# print(url)
		# url = 'http://www.ygdy8.net/html/gndy/dyzz/20170529/54074.html'
		html_text = download(url)
		time.sleep(0.01)
		score_list_temp = []
		if html_text is not None:

			tree = lxml.html.fromstring(html_text) # parse the HTML
			fixed_html = lxml.html.tostring(tree ,pretty_print=True)
			td = tree.cssselect('div#Zoom ')
			try:
				score_list_temp.append(re.findall('[Ii][Mm][Dd][Bb]评分[ \u3000\xa0]+(.*?)/10',td[0].text_content())[0])
			except IndexError as inderr:
				# print('IMDB评分 error')
				score_list_temp.append([])
			try:	
				score_list_temp.append(re.findall('豆瓣评分[ \u3000\xa0]+(.*?)/10',td[0].text_content())[0])
			except IndexError as inderr:
				# print('豆瓣评分 error')
				score_list_temp.append([])
			# print(td[0].text_content())
			# print(re.findall('IMD[Bb]评分(.*?)/10',td[0].text_content()))
			# print(re.findall('豆瓣评分\u3000(.*?)/10',td[0].text_content()))
			# print(len(td))
			print(score_list_temp)
			score_list_temp.append(df['title'][i])
		else :
			score_list_temp=[[],[],df['title'][i]]
		score_list.append(score_list_temp)
	print(score_list)


	CSV_columnName=['IMDB评分','豆瓣评分','title']

	writer = pd.DataFrame(columns = CSV_columnName, data = score_list)
	# writer.to_csv('/Users/leqi/Desktop/dytt_film1.csv',encoding ='UTF-8')
	writer.to_csv('/Users/leqi/Desktop/dytt_film1_rihan.csv',encoding ='UTF-8')



if __name__ == '__main__':
	# get_link()
	get_score()

	pass
