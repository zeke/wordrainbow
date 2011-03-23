* http://stackoverflow.com/questions/550632/favorite-django-tips-features

wordrainbow / gomer / 1d3baf57f57254b5c430200e729037e9dea9d87493f3a16b4

https://github.com/zeke/wordrainbow

$ python
Python 2.6.1 (r261:67515, Jun 24 2010, 21:47:49)
[GCC 4.2.1 (Apple Inc. build 5646)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from wordnik import Wordnik
>>> w = Wordnik(api_key="9554cd51b3ae7593536040047c20e2ac3ce71b2fd01cf1a27")
>>> w.word_get("cat")
'{"canonicalForm":"cat","word":"cat"}'
>>>