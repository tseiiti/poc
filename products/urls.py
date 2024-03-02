from django.urls import path
from .views import ProductList

app_name = "products"
urlpatterns = [
  path("list/", ProductList.as_view(),   name="list"),
  # path("signup", views.signup, name="signup"),
  # path("signin", views.signin, name="signin"),
  # path("signout", views.signout, name="signout"),
  # path('admin/', admin.site.urls),
  # path("example/", include("example.urls")),
]
