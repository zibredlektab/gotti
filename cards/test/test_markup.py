import unittest
from ..markup import *

class MarkupTest(unittest.TestCase):
    def test_passthrough(self):
        m = markup_to_django("hello")
        self.assertEqual(m, "hello")

    def test_simple_card(self):
        m = markup_to_django("Hello, [robert].")
        self.assertEqual(m, 'Hello, {% card "robert" "" %}.')

    def test_card_with_text(self):
        m = markup_to_django("Hello, [robert The King].")
        self.assertEqual(m, 'Hello, {% card "robert" "The King" %}.')

    def test_pos(self):
        m = markup_to_django("Hello, [1020 Cersei my queen].")
        self.assertEqual(m, 'Hello, {% if pos >= 1020 %}Cersei my queen{% endif %}.')

    def test_nested_pos(self):
        m = markup_to_django("Hi, [1020 ten twenty [1021 some more] maybe].")
        self.assertEqual(m, 'Hi, {% if pos >= 1020 %}ten twenty {% if pos >= 1021 %}some more{% endif %} maybe{% endif %}.')

    def test_if(self):
        m = markup_to_django("hi, [if foo == bar]foo is bar[endif].")
        self.assertEqual(m, "hi, {% if foo == bar %}foo is bar{% endif  %}.")

    def test_if_else(self):
        m = markup_to_django("hi, [if foo == bar]foo is bar[else]it's not[endif].")
        self.assertEqual(m, "hi, {% if foo == bar %}foo is bar{% else  %}it's not{% endif  %}.")
