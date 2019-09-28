from django.db import models

# Create your models here.
class ElasticSearchData(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')