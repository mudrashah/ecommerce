
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class CustomeraddressModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    email = models.EmailField()
    mobile = models.IntegerField()
    counrty = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    pincode = models.IntegerField()
    add1 = models.CharField(max_length=200)
    add2 = models.CharField(max_length=200)


    def __str__(self):
        return self.fname
        
class Maincategories(models.Model):
    name = models.CharField(max_length=122)
    def __str__(self):
        return self.name
class subcategories(models.Model):
    mcate = models.ForeignKey(Maincategories,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=122)
    def __str__(self):
            return self.name
class products(models.Model):
       mte = models.ForeignKey(Maincategories,on_delete=models.CASCADE,null=True,blank=True)
       ate = models.ForeignKey(subcategories,on_delete=models.CASCADE,null=True,blank=True)
       name = models.CharField(max_length=122)
       image = models.ImageField('image/product')
       og_price = models.IntegerField(default=0)
       discount = models.IntegerField(default=0)
       discount_price = models.IntegerField(default=0)
       sell_price = models.IntegerField(default=0)

       def __str__(self):
            return self.name


       def discounted_price(self):
            return (self.og_price * self.discount)/100
    
       def selling_price(self):
            return (self.og_price - self.discounted_price())

       def save(self, *args, **kwargs):
         self.discount_price = self.discounted_price()
         self.sell_price = self.selling_price()
         super(products, self).save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product= models.ForeignKey(products,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name

    def prod_total(self):
        return (self.product.sell_price * self.quantity)

class Wishlist(models.Model):
     user = models.ForeignKey(User,on_delete=models.CASCADE)
     product= models.ForeignKey(products,on_delete=models.CASCADE)
     quantity = models.IntegerField(default=1)

     def __str__(self):
        return self.product.name

     def prod_total(self):
        return (self.product.sell_price * self.quantity)


step = (('Pending','Pending'),('Accepted','Accepted'),('Packing','Packing'),('Shipping','Shipping'),('Deliverd','Deliverd'))

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomeraddressModel,on_delete=models.CASCADE)
    product = models.ForeignKey(products,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=step,max_length=200,default='Pending')

    @property
    def product_total(self):
        return (self.quantity)*(self.product.sell_price)

       