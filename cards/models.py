from django.db import models
from django.core.urlresolvers import reverse
from cards.yamlhelp import mapping, quoted, literal, yaml

class Card(models.Model):
    slug = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True, null=True)
    house = models.CharField(max_length=50, blank=True, null=True)
    body = models.TextField()
    first = models.IntegerField()
    died = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return self.name
        
    def __repr__(self):
        return "<Card: %s>" % self.name

    def get_absolute_url(self):
        return reverse('show_card', kwargs={'slug': self.slug})

    def as_yaml(self):
        """Return a YAML string representing this card."""
        return yaml.dump(mapping([
            ("slug", self.slug.encode('ascii')),
            ("name", quoted(self.name)),
            ("title", quoted(self.title)),
            ("house", quoted(self.house)),
            ("first", self.first),
            ("died", self.died),
            ("body", literal(self.body)),
            ]), indent=4)

    @classmethod
    def from_yaml(cls, yaml_file):
        """Create cards from yaml."""
        docs = yaml.safe_load_all(yaml_file)
        for doc in docs:
            card, new = cls.objects.get_or_create(slug=doc['slug'], defaults=doc)
            card.name = doc['name']
            card.title = doc.get('title', '')
            card.house = doc.get('house', '')
            card.first = int(doc['first'])
            card.died = int(doc['died'])
            card.body  = doc['body']
    		
            yield card

