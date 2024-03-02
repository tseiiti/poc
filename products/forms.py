from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = '__all__'
	
	code = forms.CharField(label = 'Código')
	description = forms.CharField(label = 'Descrição')
	size = forms.CharField(label = 'Tamanho')
	quantity = forms.IntegerField(label = 'Qunatidade')
	unit_price = forms.FloatField(label = 'Preço Unitário')
