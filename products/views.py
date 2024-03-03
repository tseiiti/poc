from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm


class ProductList(ListView):
	model = Product
	queryset = Product.objects.all()

class ProductCreate(CreateView):
	model = Product
	form_class = ProductForm
	success_url = reverse_lazy("products:list")
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Cadastrar Produto'
		return context

class ProductUpdate(UpdateView):
	model = Product
	form_class = ProductForm
	success_url = reverse_lazy("products:list")
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Atualizar Produto'
		return context

class ProductDetail(DetailView):
	queryset = Product.objects.all()

class ProductDelete(DeleteView):
	queryset = Product.objects.all()
	success_url = reverse_lazy("products:list")
