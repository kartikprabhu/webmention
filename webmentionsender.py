from urlparse import urljoin
from PTengine.webmentiontoolsX import WebmentionSend


def send_mentions(article_url, article_contents, default_domain):
    #parse the contents of file now & look for a links and get their hrefs
    from bs4 import BeautifulSoup, SoupStrainer
    link_list = BeautifulSoup(article_contents, parse_only=SoupStrainer('a'))
    #start sending mentions to each; default site is mine (?)
    for link in link_list:
        WebmentionSend(article_url, urljoin(default_domain, link['href'])).send()
