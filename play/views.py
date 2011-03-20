from django.shortcuts import render_to_response
from django.http import HttpResponse

def index(request):
	# return HttpResponse("Hello, world. You're at the index.")
	return render_to_response('play/index.html', {
		'something': 5,
	})
