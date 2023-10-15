from django.forms import ModelForm
from .models import City


class CityNameForm(ModelForm):
    class Meta:
        model = City
        fields = '__all__'