from urlparse import urlparse
from PTengine.webmentiontoolsX import WebmentionSend


def send_mentions(article_url, article_contents, history_set=set()):
	#parse the contents of file now & look for a links and get their hrefs
	from bs4 import BeautifulSoup, SoupStrainer
	link_list = BeautifulSoup(article_contents, parse_only=SoupStrainer('a'))
	#start sending mentions to each; default site is mine (?)
	current_set = set()
	for link in link_list:
		url = link['href']
		url_parsed = urlparse(url)
		if  url and url != '' and url_parsed[0] != '' and url_parsed[1] !='':
			current_set.add(url)
	#send mentions to everything that is in disjoint union (XOR) of sets. i.e. newly added mentions and old mentions removed
	for url in current_set ^ history_set:
		WebmentionSend(article_url, url).send()

	#return new mention set
	return current_set
