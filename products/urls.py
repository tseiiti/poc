from django.urls import path
from .views import ProductList, ProductCreate, ProductUpdate, ProductDetail, ProductDelete, from_image

app_name = "products"
urlpatterns = [
  path("list/",            ProductList.as_view(),   name="list"),
  path("create/",          ProductCreate.as_view(), name="create"),
  path("update/<int:pk>/", ProductUpdate.as_view(), name="update"),
  path("detail/<int:pk>/", ProductDetail.as_view(), name="detail"),
  path("delete/<int:pk>/", ProductDelete.as_view(), name="delete"),
  path("from_image/", from_image, name="from_image"),
]
