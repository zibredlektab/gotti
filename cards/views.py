from django.shortcuts import redirect, render, render_to_response, get_object_or_404
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
            'edition': EDITION_DICT[session.get('edition')],
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


BOOKS = [
    ('1', 'A Game of Thrones'),
    ('2', 'A Clash of Kings'),
    ('3', 'A Storm of Swords'),
    ('4', 'A Feast for Crows'),
    ('5', 'A Dance with Dragons'),
    ('6', 'The Winds of Winter'),
    ('7', 'A Dream of Spring'),
]

EDITIONS = [
    ('US-P', 'US Paperback'),
    ('US-H', 'US Hardcover'),
    ('UK-P', 'UK Paperback'),
    ('UK-H', 'UH Hardcover'),
    ('K', 'Kindle'),
    ('EPUB', 'ePub'),
]

BOOK_DICT = dict(BOOKS)
EDITION_DICT = dict(EDITIONS)

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
    
PAGE_NUMS = {
    'US-P': {
        '1': {
            'base': 1000,
            'pages': [1, 13, 22, 28, 39, 49, 58, 68, 76, 86, 93, 99, 109, 118, 128, 139, 153, 160, 165, 176, 190, 203, 215, 226, 237, 250, 259, 272, 283, 293, 305, 324, 338, 351, 359, 378, 385, 396, 410, 424, 431, 444, 452, 462, 472, 480, 489, 501, 515, 523, 530, 542, 552, 568, 583, 595, 607, 618, 628, 638, 652, 665, 675, 694, 702, 716, 729, 741, 751, 762, 772, 785, 798]
            },
        '2': {
            'base': 2000,
            'pages': [1, 30, 38, 53, 70, 81, 93, 107, 122, 136, 145, 164, 187, 203, 211, 228, 243, 261, 279, 289, 307, 323, 334, 354, 377, 397, 413, 422, 433, 444, 455, 470, 485, 495, 507, 519, 528, 537, 547, 557, 574, 587, 604, 624, 634, 649, 663, 675, 698, 709, 720, 736, 750, 762, 772, 783, 800, 811, 819, 837, 844, 852, 861, 870, 885, 904, 916, 931, 942, 956]
            },
        '3': {
            'base': 3000,
            'pages': [1, 18, 33, 43, 53, 67, 75, 91, 105, 122, 133, 146, 161, 173, 188, 202, 220, 227, 236, 254, 273, 285, 298, 311, 331, 344, 355, 367, 382, 395, 405, 413, 425, 441, 460, 474, 488, 503, 517, 530, 545, 556, 571, 590, 603, 620, 637, 648, 659, 670, 686, 693, 706, 711, 722, 738, 755, 774, 793, 799, 809, 832, 842, 857, 868, 883, 894, 912, 927, 946, 960, 977, 996, 1011, 1027, 1042, 1053, 1062, 1074, 1087, 1098, 1116]
            },
        '4': {
            'base': 4000,
            'pages': [1, 23, 42, 65, 80, 101, 124, 140, 164, 184, 206, 226, 244, 263, 283, 306, 322, 338, 362, 379, 398, 424, 444, 467, 490, 517, 537, 557, 584, 608, 634, 656, 674, 694, 718, 740, 754, 778, 800, 819, 838, 864, 897, 917, 940, 959]
            },
        '5': {
            'base': 5000,
            'pages': [0]
            },
        '6': {
            'base': 6000,
            'pages': [0]
            },
        '7': {
            'base': 7000,
            'pages': [0]
            }
        },
    'US-H': {
        '1': {
            'base': 1000,
            'pages': [0]
            },
        '2': {
            'base': 2000,
            'pages': [0]
            },
        '3': {
            'base': 3000,
            'pages': [0]
            },
        '4': {
            'base': 4000,
            'pages': [0]
            },
        '5': {
            'base': 5000,
            'pages': [0]
            },
        '6': {
            'base': 6000,
            'pages': [0]
            },
        '7': {
            'base': 7000,
            'pages': [0]
            }
        },
    'UK-P': {
        '1': {
            'base': 1000,
            'pages': [0]
            },
        '2': {
            'base': 2000,
            'pages': [0]
            },
        '3': {
            'base': 3000,
            'pages': [0]
            },
        '4': {
            'base': 3000,
            'pages': [0]
            },
        '5': {
            'base': 4000,
            'pages': [0]
            },
        '6': {
            'base': 5000,
            'pages': [0]
            },
        '7': {
            'base': 6000,
            'pages': [0]
            },
        '8': {
            'base': 7000,
            'pages': [0]
            }
        },
    'UK-H': {
        '1': {
            'base': 1000,
            'pages': [0]
            },
        '2': {
            'base': 2000,
            'pages': [0]
            },
        '3': {
            'base': 3000,
            'pages': [0]
            },
        '4': {
            'base': 4000,
            'pages': [0]
            },
        '5': {
            'base': 5000,
            'pages': [0]
            },
        '6': {
            'base': 6000,
            'pages': [0]
            },
        '7': {
            'base': 7000,
            'pages': [0]
            }
        },
    'K': {
        '1': {
            'base': 1000,
            'pages': [0]
            },
        '2': {
            'base': 2000,
            'pages': [0]
            },
        '3': {
            'base': 3000,
            'pages': [0]
            },
        '4': {
            'base': 4000,
            'pages': [0]
            },
        '5': {
            'base': 5000,
            'pages': [0]
            },
        '6': {
            'base': 6000,
            'pages': [0]
            },
        '7': {
            'base': 7000,
            'pages': [0]
            }
        },
    'EPUB': {
        '1': {
            'base': 1000,
            'pages': [0]
            },
        '2': {
            'base': 2000,
            'pages': [0]
            },
        '3': {
            'base': 3000,
            'pages': [0]
            },
        '4': {
            'base': 4000,
            'pages': [0]
            },
        '5': {
            'base': 5000,
            'pages': [0]
            },
        '6': {
            'base': 6000,
            'pages': [0]
            },
        '7': {
            'base': 7000,
            'pages': [0]
            }
        }
    }
           
def map_position(edition, book, page):
    # list of chapter page numbers for each book
    # use list as determined by book number
    # look for entry in list that is higher than page num
    # prepend book num to index in list, return
    booklist = PAGE_NUMS[edition][book]
    pos = 0
    for i, num in enumerate(booklist['pages']):
        if num > page:
            pos = i
            break
    else:
        pos = i+1
        
    pos += booklist['base']
    return pos
    
