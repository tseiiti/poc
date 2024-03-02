from django.contrib import admin
from django.urls import path, include
from products.views import ProductList

urlpatterns = [
	path('', ProductList.as_view(), name = 'index'),
	path('admin/', admin.site.urls),
	path("products/", include("products.urls")),
]
