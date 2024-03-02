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