from django.db import models

class Card(models.Model):
    slug = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True, null=True)
    house = models.CharField(max_length=50, blank=True, null=True)
    body = models.TextField()
    first_appears = models.IntegerField()
    
    def __unicode__(self):
        return self.name
        
    def __repr__(self):
        return "<Card %s>" % self.name