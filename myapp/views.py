from django.shortcuts import render,redirect

# Create your views here.
import razorpay
from myapp.models import Cart, CustomeraddressModel, Maincategories, Order, Wishlist, products, subcategories
from .form import   CustomeraddressForm, PassChangeForm, SignupForm, UserProfileChangeForm
from .form import SigninForm
from django.contrib import messages
from django.contrib.auth import authenticate,logout,login
# from django.contrib.auth import authenticate,login,logout

def ProductInfoView(request, id):
    get_product = products.objects.get(id=id)
    item_exist = Cart.objects.filter(product__id=id).exists()
    cart_count = Cart.objects.filter(user=request.user).count()
    context = {'get_product': get_product,
               'item_exist': item_exist, 'cart_count': cart_count}
    return render(request, 'proinfo.html', context)


def OrdersView(request):
    cust_order = Order.objects.filter(user=request.user)
    context = {'cust_order': cust_order}
    return render(request, 'orders.html', context)

 
def CheckoutView(request):
    cart_count = Cart.objects.filter(user=request.user).count()
    cart_items = Cart.objects.filter(user=request.user)
    all_address = CustomeraddressModel.objects.filter(user=request.user)
    # totals count -----
    sub_total = 0
    ship_charge = 70
    GST = 0
    grand_total = 0
    # get data for order
    usr = request.user
    get_address_id = request.GET.get('add')

    for i in cart_items:
        sub_total += i.prod_total()
        GST = (sub_total*10)/100
        gst = int(GST)
        grand_total = sub_total + ship_charge + gst
        print(grand_total, "ggggggggggggggggggggggggggggg")
    # Pament Start
    amount = (grand_total)*100
    client = razorpay.Client(
        auth=("rzp_test_5WA2UMpp4ZMAUc", "m72NmVlTQTxpbtSfdMCiGkp9"))
    payment = client.order.create(
        {'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    # Pament End
    if get_address_id:
        address = CustomeraddressModel.objects.get(id=get_address_id)
        for i in cart_items:
            order_data = Order(
                user=usr,
                customer=address,
                product=i.product,
                quantity=i.quantity

            )
            order_data.save()
        cart_items.delete()
    context = {'cart_count': cart_count, 'cart_items': cart_items, 'sub_total': sub_total,
               'ship_charge': ship_charge, 'GST': gst, 'grand_total': grand_total, 'all_address': all_address,
               'payment': payment}
    return render(request, 'checkout.html', context)



def AddressDeleteView(request, id):
    address = CustomeraddressModel.objects.get(id=id)
    address.delete()
    messages.error(request, 'address Successfully delete')
    return redirect('/address/')


def UpdateaddressView(request, id):
    address = CustomeraddressModel.objects.all()  # Show data of Student Table
    set_address = CustomeraddressModel.objects.get(id=id)
    if request.method == 'POST':
        form = CustomeraddressForm(
            request.POST, request.FILES, instance=set_address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student Successfully Updated')
            return redirect('/address/')
    else:
        form = CustomeraddressForm(instance=set_address)
    context = {'form': form, 'address': address}
    return render(request, 'address.html', context)


def CustomerAddressView(request):
    all_address = CustomeraddressModel.objects.filter(user=request.user)
    if request.user.is_authenticated:
        form = CustomeraddressForm(instance=request.user)
        context = {'form': form}
        if request.method == 'POST':
            form = CustomeraddressForm(request.POST)
            if form.is_valid():
                fm = form.save(commit=False)
                fm.user = request.user
                fm.save()

                messages.info(request, 'Address Successfully Added')
                return redirect('/address/')
        else:
            form = CustomeraddressForm(instance=request.user)
        context = {'form': form, 'all_address': all_address}
        return render(request, 'address.html', context)
    else:
        messages.info(request, '☹︎ Please Login First')
        return redirect('/signin/')



def Homeview(request):
    data = Maincategories.objects.all()
    sub = subcategories.objects.all()
    pro = products.objects.filter(discount__gt=60)
    subpro= products.objects.filter(ate__name="Western wear")
    subin= products.objects.filter(ate__name="Indian & Fusion wear")
    subfi= products.objects.filter(ate__name="Fashion accessories")
    subof= products.objects.filter(ate__name="Women's Footware")
    subo= products.objects.filter(ate__name="Sports wear")
    subio= products.objects.filter(ate__name="topwear")
    subbo= products.objects.filter(ate__name="Bottomwear")
    subao= products.objects.filter(ate__name="Men's Footware")
    subyo= products.objects.filter(ate__name="Sports & Active wear")
    subho= products.objects.filter(ate__name="Fashion Accessories")
    context={'data':data,'sub':sub,'pro':pro, 'subpro':subpro, 'subin':subin, 'subfi':subfi, 'subof':subof, 'subo':subo, 'subio':subio, 'subbo':subbo, 'subao':subao, 'subyo':subyo, 'subho':subho}
    return render(request,'home.html',context)

def DeleteView(request, id):
    get_item = Cart.objects.get(id=id)
    get_item.delete()
    get_name = get_item.product.name
    messages.error(request, f'{get_name} - Successfully delete')
    return redirect('/cart/')
def DeletewishView(request, id):
    get_item = Wishlist.objects.get(id=id)
    get_item.delete()
    get_name = get_item.product.name
    messages.error(request, f'{get_name} - Successfully delete')
    return redirect('/wishlist/')

def clearcart(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_items.delete()
    messages.error(request, 'Cart Successfully Cleared')
    return redirect('/cart/')
def wishclearcart(request):
    cart_items = Wishlist.objects.filter(user=request.user)
    cart_items.delete()
    messages.error(request, 'Cart Successfully Cleared')
    return redirect('/wishlist/')
def pluse_quantity(request, id):
    get_item = Cart.objects.get(id=id)
    if get_item:
        get_item.quantity += 1
        get_item.save()
        return redirect('/cart/')


def minus_quantity(request, id):
    get_item = Cart.objects.get(id=id)
    if get_item:
        get_item.quantity -= 1
        get_item.save()
        if get_item.quantity == 0:
            get_item.delete()
        return redirect('/cart/')

def Add_to_cartView(request, id):
    user = request.user
    prod = products.objects.get(id=id)
    item_exist = Cart.objects.filter(product=prod).exists()

    if item_exist:
        get_item = Cart.objects.get(product__id=id)
        get_item.quantity += 1
        get_item.save()
        return redirect('/cart/')
    else:
        product = products.objects.get(id=id)
    Cart(user=user, product=product).save()
    return redirect('/cart/')

def Add_to_WishView(request, id):
    user = request.user
    prod = products.objects.get(id=id)
    item_exist = Wishlist.objects.filter(product=prod).exists()

    if item_exist:
        get_item = Wishlist.objects.get(product__id=id)
        get_item.quantity += 1
        get_item.save()
        return redirect('/wishlist/')
    else:
        product = products.objects.get(id=id)
    Wishlist(user=user, product=product).save()
    return redirect('/wishlist/')


def Wishlistview(request):
    cart_items = Wishlist.objects.filter(user=request.user)
    context = {'cart_items':cart_items}
    return render(request, 'wishlist.html', context)


def CartView(request):
    cart_count = Cart.objects.filter(user=request.user).count()
    cart_items = Cart.objects.filter(user=request.user)

    sub_total = 0
    ship_charge = 70
    GST = 0
    grand_total = 0
    for i in cart_items:
        sub_total += i.prod_total()
        GST = (sub_total*10)/100
    grand_total = sub_total + ship_charge + GST

    context = {'cart_count': cart_count, 'cart_items': cart_items, 'sub_total': sub_total,'ship_charge': ship_charge, 'GST': GST, 'grand_total':grand_total}
    return render(request, 'cart.html', context)

         
def allproductview(request):
    
    data = Maincategories.objects.all()
    sub = subcategories.objects.all()
    pro = products.objects.all()
    all_categories = Maincategories.objects.all()
    all_products = products.objects.all()
  
    get_cat_id = request.GET.get('catesid')
    if get_cat_id:
        all_products = products.objects.filter(mte__id=get_cat_id)

    get_id = request.GET.get('subid')
    if get_id:
        all_products = products.objects.filter(ate__id=get_id)
    

    get_product_name = request.GET.get('byname')
    if get_product_name:
        all_products = products.objects.filter(
            name__icontains=get_product_name)

  
    context = {'all_categories': all_categories, 'all_products': all_products,
               'data':data,'sub':sub,'pro':pro}
    return render(request, 'allproducts.html', context)

# User Signup
def Signupview(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            usrname= form.cleaned_data['username']
            form.save() 
            messages.success(request,f'{usrname} Successfully Registred')
            return redirect("/home/")
        else:
            pass
    else:
        form = SignupForm()
  
    return render(request, 'signup.html', {'form': form})


def SigninView(request):
    form = SigninForm()
    if request.method == 'POST':
        uname = request.POST['uname']
        upass = request.POST['upass']
        user = authenticate(username=uname,password=upass)
        print("========",user)
        if user is None:
            messages.error(request,'Please Enter Correct Credinatial')
            return redirect('/signin/')
        else:
            login(request,user)
            messages.success(request,'Login Successful')
        return redirect('/home/')
    else:
        if request.user.is_authenticated:
            return redirect('/home/')
        else:
            return render(request,'signin.html',{'form':form})


def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'You are Successfully Logged Out !')
        return redirect('/signin')
    else:
        messages.info(request, 'Please Login First')
    return redirect('/signin')




# User Password Change
def ChangePassView(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PassChangeForm(user = request.user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Password Successfully Changed')
        else:
            form = PassChangeForm(user =request.user)
            
        context= {'form':form,}
        return render(request,'passchange.html',context)
    else:
        messages.info(request, '☹︎ Please Login First')
    return redirect('/signin/')


# User Profile Update
def ProfileView(request):
    if request.user.is_authenticated:
        form =UserProfileChangeForm(instance=request.user)
        context = {'form':form}
        if request.method == 'POST':
            form =UserProfileChangeForm(request.POST,instance=request.user)
            if form.is_valid():
                form.save()
                messages.info(request,'Profile Successfully Updated')
                return redirect('/profile/')
            else:
                form =UserProfileChangeForm(instance=request.user)
                user_data = request.user
                context = {'form':form,'user_data':user_data}
                return render(request,'profile.html',context)
        
        return render(request,'profile.html',context)
    else:
        messages.info(request, '☹︎ Please Login First')
        return redirect('/signin')

