from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from cards.models import Card

def home(request):
    cards = Card.objects.all()
    session = request.session
    return render_to_response('cards/home.html', {'cards': cards, 'page': session.get('page'), 'book': session.get('book')})
    
def show_card(request, slug):
    card = Card.objects.get(slug=slug)
    return render_to_response('cards/card.html', {'card': card})
    
BOOKS = (
    ('1', 'A Game of Thrones'),
    ('2', 'A Clash of Kings'),
    ('3', 'A Storm of Swords'),
    ('4', 'A Feast for Crows'),
    ('5', 'A Dance with Dragons'),
    ('6', 'The Winds of Winter'),
    ('7', 'A Dream of Spring'),
)

class PositionForm(forms.Form):
    book = forms.ChoiceField(choices=BOOKS)
    page = forms.IntegerField(min_value=0, max_value=1000)

def settings(request):
    if request.method == 'POST': # If the form has been submitted...
        form = PositionForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            request.session['book'] = form.cleaned_data['book']
            request.session['page'] = form.cleaned_data['page']
            request.session['pos'] = 0
            return HttpResponseRedirect('/settings') # Redirect after POST
    else:
        default_data = {
            'book': request.session.get('book'), 
            'page': request.session.get('page')
        }
        form = PositionForm(default_data) # An unbound form
        
    return render(request, 'cards/settings.html', {
        'form': form,
    })
    
