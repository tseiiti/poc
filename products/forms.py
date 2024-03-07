from django.forms import ModelForm, TextInput, NumberInput, Form, FileField, BooleanField, IntegerField
from .models import Product

text_input = TextInput(attrs = { 'class': 'form-control' })
number_input = NumberInput(attrs = { 'class': 'form-control' })

class ProductForm(ModelForm):
	class Meta:
		model = Product
		fields = '__all__'
		widgets = {
			'code': text_input, 
			'description': text_input, 
			'size': text_input, 
			'quantity': number_input, 
			'unit_price': number_input, 
		}
		labels = {
			'code': 'Código', 
			'description': 'Descrição', 
			'size': 'Tamanho', 
			'quantity': 'Quantidade', 
			'unit_price': 'Preço Unitário', 
		}

class UploadFileForm(Form):
	invoice = FileField()
	confirm = BooleanField(required = False)
	confirm_time = IntegerField(initial=10, required = False)
	