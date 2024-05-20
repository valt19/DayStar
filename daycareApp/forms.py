from django.forms import ModelForm
from .models import *
from django import forms

# user forms
class Sitter_regForm(ModelForm):
    class Meta:
        model = Sitter
        fields = ['gender']
        fields = '__all__'



class Baby_regForm(ModelForm):
    class Meta:
        model = Baby
        fields = '__all__'


class Item_sellForm(ModelForm):   # item sellling form
    class Meta:
        model = ItemSelling
        fields = ['baby', 'doll_name', 'quantity', 'amount_paid']


class Item_regForm(ModelForm):       # item registration form
    class Meta:
        model = AddItem
        fields = '__all__'

class BabyPaymentForm(ModelForm):   #baby payment form
    class Meta:
        model = BabyPayment
        fields = '__all__'

class SitterPaymentForm(ModelForm):   #Sitter payment form
    class Meta:
        model = SitterPayment
        fields = '__all__'

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields = ['amount_paid'].disabled = True


class Addmore(ModelForm):  #adding item form
    class Meta:
        model = AddItem
        fields = ['quantity']