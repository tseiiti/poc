from django.urls import path
from .views import ProductList, ProductCreate

app_name = "products"
urlpatterns = [
  path("list/",   ProductList.as_view(),   name="list"),
  path("create/", ProductCreate.as_view(), name="create"),
]
