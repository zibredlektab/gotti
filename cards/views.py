from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from cards.models import Card

def home(request):
    session = request.session
    if 'pos' not in session:
        return HttpResponseRedirect('/settings')
    cards = Card.objects.filter(first_appears__lte = session.get('pos'))
    return render_to_response(
        'cards/home.html', {
            'cards': cards,
            'page': session.get('page'),
            'book': BOOK_DICT[session.get('book')],
            'pos': session.get('pos')
        }
    )
    
def show_card(request, slug):
    card = Card.objects.get(slug=slug)
    return render_to_response(
        'cards/card.html', {
            'card': card,
            'pos': request.session.get('pos'),
        }
    )
    
BOOKS = [
    ('1', 'A Game of Thrones'),
    ('2', 'A Clash of Kings'),
    ('3', 'A Storm of Swords'),
    ('4', 'A Feast for Crows'),
    ('5', 'A Dance with Dragons'),
    ('6', 'The Winds of Winter'),
    ('7', 'A Dream of Spring'),
]

BOOK_DICT = dict(BOOKS)

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
            request.session['pos'] = map_position(form.cleaned_data['book'], form.cleaned_data['page'])
            return HttpResponseRedirect('/') # Redirect after POST
    else:
        default_data = {
            'book': request.session.get('book'), 
            'page': request.session.get('page')
        }
        form = PositionForm(default_data) # An unbound form
        
    return render(request, 'cards/settings.html', {
        'form': form,
    })
    
PAGE_NUMS = {
    '1': {
        'base': 1000,
        'pages': [1]
        },
    '2': {
        'base': 2000,
        'pages': [1]
        },
    '3': {
        'base': 3000,
        'pages': [1, 18, 43, 53, 67, 75, 91, 105, 122, 133, 146, 161, 173, 188, 202, 220, 227, 236, 254, 273, 298, 311]
        },
    '4': {
        'base': 4000,
        'pages': [1]
        },
    '5': {
        'base': 5000,
        'pages': [1]
        },
    '6': {
        'base': 6000,
        'pages': [1]
        },
    '7': {
        'base': 7000,
        'pages': [1]
        }
    
    }
           
def map_position(book, page):
    # list of chapter page numbers for each book
    # use list as determined by book number
    # look for entry in list that is higher than page num
    # prepend book num to index in list, return
    booklist = PAGE_NUMS[book]
    pos = 0
    for i, num in enumerate(booklist['pages']):
        if num > page:
            pos = i
            break
    else:
        pos = i+1
        
    pos += booklist['base']
    return pos
    