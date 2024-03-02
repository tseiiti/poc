from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from .models import Product


class ProductList(ListView):
	model = Product
	queryset = Product.objects.all()
