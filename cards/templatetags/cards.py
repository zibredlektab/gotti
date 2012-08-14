"""Template tags for Cards."""

from django import template
from django.template import Template, Variable, TemplateSyntaxError
from ..models import Card

register = template.Library()

class RenderAsTemplateNode(template.Node):
    def __init__(self, item_to_be_rendered):
        self.item_to_be_rendered = Variable(item_to_be_rendered)

    def render(self, context):
        try:
            actual_item = self.item_to_be_rendered.resolve(context)
            template_text = "{% load cards %}\n" + actual_item
            return Template(template_text).render(context)
        except template.VariableDoesNotExist:
            return ''

@register.tag
def render_as_template(parser, token):
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError(
            "'%s' takes only one argument"
            " (a variable representing a template to render)" % bits[0]
        )
    return RenderAsTemplateNode(bits[1])

class PosNode(template.Node):
    def __init__(self, pos, nodelist):
        self.pos = int(pos)
        self.nodelist = nodelist
        
    def render(self, context):
        pos = int(context.get('pos', 0))
        print "Comparing %r >= %r" % (pos, self.pos)
        if pos >= self.pos:
            output = self.nodelist.render(context)
        else:
            output = ""
        return output
       
@register.tag 
def pos(parser, token):
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError("pos takes one argument")
    pos = bits[1]
    nodelist = parser.parse(('endpos',))
    parser.delete_first_token()
    return PosNode(pos, nodelist)

class CardNode(template.Node):
    def __init__(self, slug, text=None):
        self.slug = Variable(slug)
        self.text = Variable(text) if text else None
        
    def render(self, context):
        slug = self.slug.resolve(context)
        try:
            card = Card.objects.get(slug=slug)
        except Card.DoesNotExist:
            card = None
        if self.text:
            text = self.text.resolve(context)
        elif card:
            text = card.name
        else:
            text = "{card: %s}" % slug
        if card:
            url = card.get_absolute_url()
        else:
            url = "/admin/cards/card/add/?slug=%s" % slug
        title = "Learn more about %s" % text
        return '[%s](%s "%s")' % (text, url, title)        

@register.tag
def card(parser, token):
    bits = token.split_contents()
    slug = text = None
    if len(bits) >= 2:
        slug = bits[1]
    if len(bits) >= 3:
        text = bits[2]
    return CardNode(slug, text)
    
