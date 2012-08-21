"""Template tags for Cards."""

import re

from django import template
from django.template import Template, Variable, TemplateSyntaxError
from ..models import Card
from ..markup import markup_to_django

register = template.Library()

class RenderAsTemplateNode(template.Node):
    def __init__(self, item_to_be_rendered):
        self.item_to_be_rendered = Variable(item_to_be_rendered)

    def render(self, context):
        try:
            actual_item = self.item_to_be_rendered.resolve(context)
            template_text = "{% load cards %}\n" + markup_to_django(actual_item)
            res = Template(template_text).render(context)
            res = re.sub(r'[ \t]+\n', '\n', res)
            return res
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
        text = ""
        if self.text:
            text = self.text.resolve(context)
        if not text and card:
            text = card.name
        if not text:
            text = "{card: %s}" % slug
        if card:
            url = card.get_absolute_url()
        else:
            url = "/admin/cards/card/add/?slug=%s" % slug
        title = "Learn more about %s" % text

        pos = int(context.get('pos', 0))
        if card and card.died and pos > card.died:
            dead_class = ' dead'
        else:
            dead_class = ''
        return "<a href='%s' class='cardlink%s' title='%s'>%s</a>" % (url, dead_class, title, text)

@register.tag
def card(parser, token):
    bits = token.split_contents()
    slug = text = None
    if len(bits) >= 2:
        slug = bits[1]
    if len(bits) >= 3:
        text = bits[2]
    return CardNode(slug, text)
    
