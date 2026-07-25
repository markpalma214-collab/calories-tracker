from django.forms import ModelForm
from .models import CaloriesTracker



class CaloriesForm(ModelForm):
    class Meta:
        model = CaloriesTracker
        fields = '__all__'