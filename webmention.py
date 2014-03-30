from django.http import HttpResponse 
from PTengine.webmentiontoolsX import UrlInfo
from PTengine.models import Response

def find_target_obj(target_url):
	from urlparse import urlparse
	import re
	url_match=re.match(r'^/article/(?P<slug>[-a-zA-Z0-9]+)/?$', urlparse(target_url).path)
	if not url_match:
		return None
	from PTengine.models import Article
	return Article.objects.filter(slug=url_match.group('slug'))[0]

def find_mention(target_obj, source):
	# find if a mention already exists with target_obj and source
	mention = Response.objects.filter(response_to=target_obj, original_url=source)
	if mention:
		return mention[0]
	else:
		return None

def save_mention(mention, source_info, target_url, target_obj):
	if not mention:
		mention = Response()
	#code to save a mention
	mention.author = source_info.author()
	if not mention.author:
		mention.author = 'Anon'
	mention.author_url = source_info.author_url()
	mention.pub_date = source_info.pubDate()
	if not mention.pub_date:
		from datetime import datetime
		mention.pub_date = datetime.now()
	mention.content = source_info.snippetWithLink(target_url).encode('utf-8')
	mention.response_to=target_obj
	mention.original_title=source_info.title().encode('utf-8')
	mention.original_url=source_info.url
	mention.save()

def delete_mention(mention):
	mention.delete()

def encode_reply(reply):
	html_content = """<!DOCTYPE html>
<html lang="en">
  <head>
    <title>WebMention</title>
  </head>
  <body>
    <p>%s</p>
  </body>
</html>""" % reply['reason']
	return HttpResponse(status=reply['status'], content_type='text/html', content=html_content)
	## reason_phrase not supported in Django 1.5

def parse_mention(source, target):
	## check if source target are well-defined
	target_obj = find_target_obj(target)
	if target_obj:
		## fetch source info.
		source_info = UrlInfo(source)
		## HERE CHECK IF SOURCE IS RETRIVED CORRECTLY OR NOT
		if source_info.error:
			return {'status': 400, 'reason': 'Source URL could not be retrieved'}
		else:
			##check if a mention already exists
			mention = find_mention(target_obj, source)
			# check if source links to target in any way
			if source_info.linksTo(target):
				# ADD/SAVE TO DB
				save_mention(mention, source_info, target, target_obj)
				return {'status': 202, 'reason': 'Webmention accepted.', 'body': 'RETURN WEBMENTION URL'}
			else:
				if mention:
					#if no link & mention exists then delete it
					delete_mention(mention)
					return {'status': 202, 'reason': 'Webmention deleted'}
				# else return error
				return {'status': 400, 'reason': 'Source URL does not contain a link to the target URL'}
	else:
		return {'status': 400, 'reason': 'target URL not found or does not accept webmentions'}

def post_mention(accept_header, source, target):
	#don't defrag source and target

	if source and target:
			reply_response = parse_mention(source, target)
	else:
		reply_response = {'status': 400, 'reason': 'URL not specified for source or target'}

	return encode_reply(reply_response)
