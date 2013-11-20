webmention
==========

A Python implementation of the [webmention](https://github.com/converspace/webmention) protocol.

At present:

*	webmentiontoolsX extends [vrypan's webmention-tools](https://github.com/vrypan/webmention-tools) to return author name, author url, accept text/html response if sending a webmention.
*	webmention.py contains functions to parse, check and save a webmention as responses in a particular Django website.


To do
======

1.	retrieve author info using p-author and h-card.
2.	create self-contained object implementation of webmention parsing independent of Django implementation.
