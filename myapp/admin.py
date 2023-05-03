from django.contrib import admin
from .models import  Maincategories, products, subcategories,Cart,Wishlist,Order,CustomeraddressModel
# Register your models here.


@admin.register(Maincategories)
class MaincategoriesAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(subcategories)
class subcategoriesAdmin(admin.ModelAdmin):
    list_display = ("name", "mcate")




@admin.register(products)
class productsAdmin(admin.ModelAdmin):
    list_display = ["sell_price", "discount_price", "discount", "og_price", "image", "name", "ate", "mte"][::-1]



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("quantity", "product", "user")


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("quantity", "product", "user")



@admin.register(CustomeraddressModel)
class CustomeraddressModelAdmin(admin.ModelAdmin):
    list_display = ("add2", "add1", "pincode", "city", "state", "counrty", "mobile", "email", "lname", "fname", "user")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["status", "order_date", "quantity", "product", "customer", "user"][::-1]
