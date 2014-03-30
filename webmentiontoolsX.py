from urlparse import urljoin
from webmentiontools.urlinfo import UrlInfo
from webmentiontools.send import WebmentionSend

import requests

class UrlInfo(UrlInfo):
	def author(self):
		if self.data.has_key('author'):
			return self.data['author']

		#try using meta name=author tag
		author = self.soup.find('meta',attrs={'name':'author'})
		if author:
			self.data['author'] = author['content']
			return self.data['author']

		#try using anything with rel=author tag
		author = self.soup.find(True, attrs={'rel':'author'})
		if author:
			self.data['author'] = author['content']
			return self.data['author']

		# try using p-author or h-card

		#default return none
		return None

	def author_url(self):
		if self.data.has_key('author_url'):
			return self.data['author_url']

		# try hrf from rel=author
		author_url = self.soup.find(True, attrs={'rel':'author'})
		if author_url:
			self.data['author_url'] = urljoin( self.url, author_url['href'])
			return self.data['author_url']

		# try href of rel=me
		author_url = self.soup.find(True, attrs={'rel':'me'})
		if author_url:
			self.data['author_url'] = urljoin( self.url, author_url['href'])
			return self.data['author_url']

		# try using p-author or h-card

		#default retrn none
		return None

class WebmentionSend(WebmentionSend):
	def _notifyReceiver(self):
		payload = {'source': self.source_url, 'target': self.target_url}
		headers = {'Accept': 'text/html, application/json'}
		r = requests.post(self.receiver_endpoint, data=payload, headers=headers)
		self.r = r ## for debug purposes
		if r.status_code != 202:
			self.error = {
				'code':'RECEIVER_ERROR',
				'request': 'POST %s (with source=%s, target=%s)' %(self.receiver_endpoint, self.source_url, self.target_url),
				'http_status': r.status_code,
			}
			if r.headers['content-type'] == 'application/json':
				response = r.json()
				self.error['error'] = response.get('error','')
				self.error['error_description'] = response.get('error_description','')
			elif r.headers['content-type'] == 'text/html':
				self.error['error'] = r.reason
				self.error['error_description'] = r.content
			return False
		else:
			return True
