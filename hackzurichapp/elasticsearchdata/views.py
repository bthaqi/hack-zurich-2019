from django.shortcuts import render

from rest_framework import viewsets

from .serializers import ElasticSearchDataSerializer
from .models import ElasticSearchData

# Create your views here.
class ElasticSearchDataViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = ElasticSearchData.objects.all()
    serializer_class = ElasticSearchDataSerializer
    