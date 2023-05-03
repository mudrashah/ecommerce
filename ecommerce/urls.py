"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings # --------> this
from django.conf.urls.static import static# --------> this

from myapp.views import  AddressDeleteView, ChangePassView, CheckoutView, CustomerAddressView, DeletewishView, Homeview, ProductInfoView, ProfileView, SigninView, UpdateaddressView, Wishlistview, allproductview,Signupview, logoutView,CartView,Add_to_cartView,pluse_quantity,minus_quantity,DeleteView,clearcart,Add_to_WishView, wishclearcart,OrdersView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',Homeview),
    path('addressupdate/<int:id>/',UpdateaddressView),
    path('addressdelete/<int:id>/',AddressDeleteView),
    path('address/', CustomerAddressView),
    path('signup/',Signupview),
    path('signin/',SigninView),
    path('out/',logoutView),
    path('passchange/',ChangePassView),
    path('profile/',ProfileView),
    path('allproducts/',allproductview),
    path('cart/',CartView),
    path('addtocart/<int:id>/',Add_to_cartView),
    path('plus/<int:id>/',pluse_quantity),
    path('minus/<int:id>/',minus_quantity),
    path('delete/<int:id>/',DeleteView),
    path('clearcart/',clearcart),
    path('wishlist/',Wishlistview),
    path('addtowish/<int:id>/',Add_to_WishView),
    path('del/<int:id>',DeletewishView),
    path('clearwish/',wishclearcart),
    path('checkout/',CheckoutView),
    path('orders/',OrdersView),
    path('proinfo/<int:id>/',ProductInfoView),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # --------> this

