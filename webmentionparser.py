from PTengine.webmentiontoolsX import UrlInfo

class WebmentionParser():
	
	def __init__(self, source, target):
		self.source = source
		self.target = target
		self.mention_info = UrlInfo(source)

## Really can't decide how to separate implementation of parser from the Django objects things!
