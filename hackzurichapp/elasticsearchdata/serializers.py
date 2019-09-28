# from django.contrib.auth.models import User, Group
from rest_framework import serializers

from elasticsearchdata.models import ElasticSearchData

class ElasticSearchDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElasticSearchData
        fields = '__all__'
        