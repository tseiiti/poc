from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Product
from .forms import ProductForm, UploadFileForm

from PIL import Image
import pytesseract
from selenium import webdriver
from selenium.webdriver.common.by import By

class ProductHandler():
	def setup(self):
		self.driver = webdriver.Chrome()
	
	def teardown(self):
		self.driver.quit()

	def handle(self, code, description, size, quantity, unit_price):
		self.driver.get('http://localhost:8000/products/list/')
		self.driver.set_window_size(1200, 800)
		self.driver.find_element(By.LINK_TEXT, "Novo Registro").click()
		self.driver.find_element(By.ID, "id_code").click()
		self.driver.find_element(By.ID, "id_code").send_keys(code)
		self.driver.find_element(By.ID, "id_description").click()
		self.driver.find_element(By.ID, "id_description").send_keys(description)
		self.driver.find_element(By.ID, "id_size").click()
		self.driver.find_element(By.ID, "id_size").send_keys(size)
		self.driver.find_element(By.ID, "id_quantity").click()
		self.driver.find_element(By.ID, "id_quantity").send_keys(quantity)
		self.driver.find_element(By.ID, "id_unit_price").click()
		self.driver.find_element(By.ID, "id_unit_price").send_keys(unit_price)
		self.driver.find_element(By.CSS_SELECTOR, "button.btn-primary").click()

def handle_file(f):
	image = Image.open(f)
	text = pytesseract.image_to_string(image, lang='por')
	texts = text.split('\n')
	id_ini = texts.index('CÓDIGO DESCRIÇÃO DO PRODUTO / SERVIÇO TAMANHO QUANTIDADE VALOR UNITÁRIO VALOR TOTAL')
	id_fim = texts.index('DADOS ADICIONAIS')
	handler = ProductHandler()
	handler.setup()
	for i in range(id_ini + 1, id_fim):
		txts = texts[i].split()
		if len(txts) > 5:
			code = txts[0]
			description = ' '.join(txts[1:-4])
			size = txts[-4]
			quantity = txts[-3]
			unit_price = txts[-2]
			# total = txts[-1]
			handler.handle(code, description, size, quantity, unit_price)
	handler.teardown()

def from_image(request):
	form = UploadFileForm()
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			handle_file(request.FILES['invoice'])
			return redirect('products:list')

	return render(request, 'products/from_image.html', { 'form': form })

class ProductList(ListView):
	model = Product
	queryset = Product.objects.all()

class ProductCreate(CreateView):
	model = Product
	form_class = ProductForm
	success_url = reverse_lazy('products:list')
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Cadastrar Produto'
		return context

class ProductUpdate(UpdateView):
	model = Product
	form_class = ProductForm
	success_url = reverse_lazy('products:list')
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Atualizar Produto'
		return context

class ProductDetail(DetailView):
	queryset = Product.objects.all()

class ProductDelete(DeleteView):
	queryset = Product.objects.all()
	success_url = reverse_lazy('products:list')
