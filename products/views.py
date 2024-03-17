from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Product
from .forms import ProductForm, UploadFileForm

from PIL import Image
import pytesseract
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located as pres

from openai import OpenAI
import json
import os

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CONTENT = "Peço que me informe quais são as descrições de produtos, código, valor unitário, " \
				+ "tamanho, quantidade pedida e as cores das roupas que estão na nota fiscal a " \
				+ "seguir de forma direta e precisa. A saída das informações deverá ser somente " \
				+ "o array no formato JSON. Cada atributo deve ter uma chave, sendo, " \
				+ "COD: para o código, " \
				+ "DSC: para a descrição, " \
				+ "COR: para cor, " \
				+ "QTD: para quantidade pedida, " \
				+ "TAM: para o tamanho e " \
				+ "VAL: para o valor unitário. " \
				+ "Segue a nota fiscal: "

class ProductHandler():
	def setup(self, confirm, confirm_time, url_list):
		self.driver = webdriver.Chrome()
		self.confirm = confirm == "on"
		self.wait = WebDriverWait(self.driver, int(confirm_time))
		self.url_list = url_list
	
	def teardown(self):
		self.driver.quit()

	def handle(self, code, description, color, size, quantity, unit_price):
		self.driver.get(self.url_list)
		self.driver.set_window_size(1200, 1000)
		self.driver.find_element(By.LINK_TEXT, "Novo Registro").click()
		self.driver.find_element(By.ID, "id_code").click()
		self.driver.find_element(By.ID, "id_code").send_keys(code)
		self.driver.find_element(By.ID, "id_description").click()
		self.driver.find_element(By.ID, "id_description").send_keys(description)
		self.driver.find_element(By.ID, "id_color").click()
		self.driver.find_element(By.ID, "id_color").send_keys(color)
		self.driver.find_element(By.ID, "id_size").click()
		self.driver.find_element(By.ID, "id_size").send_keys(size)
		self.driver.find_element(By.ID, "id_quantity").click()
		self.driver.find_element(By.ID, "id_quantity").send_keys(quantity)
		self.driver.find_element(By.ID, "id_unit_price").click()
		self.driver.find_element(By.ID, "id_unit_price").send_keys(unit_price)

		print(code, description, color, size, quantity, unit_price)
		if self.confirm:
			try:
				self.wait.until(pres((By.LINK_TEXT, "Novo Registro")))
				return
			except:
				pass
		print(self.confirm)
		self.driver.find_element(By.CSS_SELECTOR, "button.btn-primary").click()

def handle_file(file, use_gpt, confirm, confirm_time, url_list):
	print("escaneando a imagem...")
	image = Image.open(file)
	text = pytesseract.image_to_string(image, lang='por').strip()

	handler = ProductHandler()
	handler.setup(confirm, confirm_time, url_list)
	
	if use_gpt == "on": 
		print("identificando dados com gpt...")
		# com gpt
		client = OpenAI(api_key = OPENAI_API_KEY)
		completion = client.chat.completions.create(
			model = "gpt-3.5-turbo",
			messages = [
				{ "role": "user", "content": CONTENT + text }
			],
			temperature = 0.2
		)
		itens = json.loads(completion.choices[0].message.content)
	else: 
		print("identificando dados pela posição dos textos...")
		# sem gpt
		texts = text.split('\n')
		id_ini = texts.index('CÓDIGO DESCRIÇÃO DO PRODUTO / SERVIÇO TAMANHO QUANTIDADE VALOR UNITÁRIO VALOR TOTAL')
		id_fim = texts.index('DADOS ADICIONAIS')
		itens = []
		for i in range(id_ini + 1, id_fim):
			txts = texts[i].split()
			if len(txts) > 5:
				iten = {}
				iten['COD'] = txts[0]
				iten['DSC'] = ' '.join(txts[1:-4])
				iten['COR'] = ''
				iten['TAM'] = txts[-4]
				iten['QTD'] = txts[-3]
				iten['VAL'] = txts[-2]
				itens.append(iten)

	print("cadastro automático pelo selenium...")
	for iten in itens:
		handler.handle(iten['COD'], iten['DSC'], iten['COR'], iten['TAM'], iten['QTD'], iten['VAL'])
	handler.teardown()

def from_image(request):
	form = UploadFileForm()
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			use_gpt = request.POST.get("use_gpt")
			confirm = request.POST.get("confirm")
			confirm_time = request.POST.get("confirm_time")
			url_list = request.build_absolute_uri().replace(str(reverse_lazy('products:from_image')), str(reverse_lazy('products:list')))
			handle_file(request.FILES['invoice'], use_gpt, confirm, confirm_time, url_list)
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
