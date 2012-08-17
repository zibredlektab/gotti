from django.shortcuts import redirect, render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from cards.models import Card

from bookdata import BOOKS, BOOK_DICT, EDITIONS, EDITION_DICT, PAGE_NUMS, map_position

def home(request):
    session = request.session
    if 'pos' not in session:
        return HttpResponseRedirect('/settings')
    cards = Card.objects.filter(first__lte=session.get('pos'))
    return render_to_response(
        'cards/home.html', {
            'cards': cards,
            'page': session.get('page'),
            'book': BOOK_DICT[session.get('book')],
            'edition': EDITION_DICT[session.get('edition')],
            'pos': session.get('pos')
        }
    )
    
def show_card(request, slug):
    session = request.session
    card = Card.objects.get(slug=slug)
    return render_to_response(
        'cards/card.html', {
            'card': card,
            'page': session.get('page'),
            'book': BOOK_DICT[session.get('book')],
            'edition': EDITION_DICT[session.get('edition')],
            'pos': session.get('pos')
        }
    )
    
def show_all(request):
    session = request.session
    cards = Card.objects.filter(first__lte=session.get('pos'))
    return render_to_response(
        'cards/allcards.html', {
            'cards': cards,
            'page': session.get('page'),
            'book': BOOK_DICT[session.get('book')],
            'edition': EDITION_DICT[session.get('edition')],
            'pos': session.get('pos')
        }
    )

def yaml_card(request, slug):
    """Deliver a card as a YAML file."""
    on_page = bool(int(request.REQUEST.get('page', '0')))
    card = get_object_or_404(Card, slug=slug)
    mimetype="text/plain" if on_page else "text/yaml"  
    response = HttpResponse(card.as_yaml(), mimetype=mimetype)
    if not on_page:
        response['Content-Disposition'] = 'attachment; filename=%s.yaml' % card.slug
    return response

def export_all(request):
    """Deliver all the cards as YAML."""
    on_page = bool(int(request.REQUEST.get('page', '0')))
    yaml = ['# all the gotti cards']
    for card in Card.objects.all():
        yaml.append('---')
        yaml.append(card.as_yaml())
    mimetype="text/plain" if on_page else "text/yaml"  
    response = HttpResponse("\n".join(yaml), mimetype=mimetype)
    if not on_page:
        response['Content-Disposition'] = 'attachment; filename=gotti.yaml'
    return response

def import_lots(request):
    """Import a bunch of cards."""
    if request.method == "POST":
        form = ImportCardForm(request.POST, request.FILES)
        if form.is_valid():
            for card in Card.from_yaml(request.FILES['yamlfile']):
                card.save()
            return redirect('home')
    else:
        form = ImportCardForm()

    return render(request, 'cards/import.html', {'form': form})

class ImportCardForm(forms.Form):
    yamlfile = forms.FileField(
        label='Select a YAML file',
        help_text='Some Help'
    )


class PositionForm(forms.Form):
    edition = forms.ChoiceField(choices=EDITIONS)
    book = forms.ChoiceField(choices=BOOKS)
    page = forms.IntegerField(min_value=0, max_value=1000)

def settings(request):
    if request.method == 'POST': # If the form has been submitted...
        form = PositionForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            request.session['edition'] = form.cleaned_data['edition']
            request.session['book'] = form.cleaned_data['book']
            request.session['page'] = form.cleaned_data['page']
            request.session['pos'] = map_position(form.cleaned_data['edition'], form.cleaned_data['book'], form.cleaned_data['page'])
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
