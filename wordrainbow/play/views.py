from django.shortcuts import render_to_response
from django.http import HttpResponse

import playmode

def index(request, w=None, mode="identify"):
    """Documentation"""
    request.session['name'] = 'bob'
    print request.session
    return HttpResponse(w.word_get_related('fish'))
    
