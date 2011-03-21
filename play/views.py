from django.shortcuts import render_to_response
from django.http import HttpResponse
from wordnik import Wordnik

def index(request):
	# return HttpResponse("Hello, world. You're at the index.")
	w = Wordnik(api_key="1d3baf57f57254b5c430200e729037e9dea9d87493f3a16b4")
	return HttpResponse(w.word_get_related('fish'))
	# return render_to_response('play/index.html', {
	# 	'result': result,
	# })
