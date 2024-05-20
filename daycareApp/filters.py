import django_filters
from . models import *

class BabyFilter(django_filters.FilterSet):
    class Meta:
        model = Baby
        fields = ['name']