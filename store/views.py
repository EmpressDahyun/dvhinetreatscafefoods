from itertools import product
from math import prod
from multiprocessing import context
from urllib import response
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from tomlkit import datetime
from store.forms import DeliveryForm,  OrderSlipForm, ReservationForm
from .models import *
from django.contrib import messages
from django.views import View
import decimal
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.mail import EmailMessage

# Create your views here.

def home(request):
    categories = Category.objects.filter(is_active=True, is_featured=True)[:3]
    products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    not_products = Product.objects.filter(is_active=False, is_featured=True)[:8]
    context = {
        'categories': categories,
        'products': products,
        'not_products': not_products,
    }
    return render(request, 'store/index.html', context)

def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    not_products = Product.objects.filter(is_active=False, id=product.id)
    related_products = Product.objects.exclude(id=product.id).filter(is_active=True, category=product.category)
    context = {
        'product': product,
        'related_products': related_products,
        'not_products': not_products,
    }
    return render(request, 'store/detail.html', context)

def all_categories(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'store/categories.html', {'categories':categories})

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(is_active=True, category=category)
    categories = Category.objects.filter(is_active=True)
    not_products = Product.objects.filter(is_active=False, category=category)
    context = {
        'category': category,
        'products': products,
        'categories': categories,
        'not_products': not_products,
    }
    return render(request, 'store/category_products.html', context)

def gallery_view(request):
    gallery = Gallery.objects.all()
    context = {
        'gallery': gallery,
    }
    return render(request, 'store/gallery.html', context)

def location_view(request):
    return render(request, 'store/location.html')

def aboutus_view(request):
    return render(request, 'store/about_us.html')

@login_required
def profile(request):
    delivery_information = DeliveryInformation.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    reservations = Reservation.objects.filter(user=request.user)
    order_item = OrderItem.objects.filter(user=request.user)
    return render(request, 'account/profile.html', {'delivery_information':delivery_information, 'orders':orders, 'reservations':reservations,'order_items':order_item})

@method_decorator(login_required, name='dispatch')
class DeliveryView(View):
    def get(self, request):
        form = DeliveryForm()
        return render(request, 'account/add_address.html', {'form': form})

    def post(self, request):
        form = DeliveryForm(request.POST)
        if form.is_valid():
            user=request.user
            recipient_name = form.cleaned_data['recipient_name']
            phone_number = form.cleaned_data['phone_number']
            telephone_number = form.cleaned_data['telephone_number']
            barangay = form.cleaned_data['barangay']
            landmark = form.cleaned_data['landmark']
            street_name = form.cleaned_data['street_name']
            city = form.cleaned_data['city']
            reg = DeliveryInformation(user=user, recipient_name=recipient_name, phone_number=phone_number,telephone_number=telephone_number,barangay=barangay,landmark=landmark,street_name=street_name,city=city)
            reg.save()
            messages.success(request, "New Delivery Address Added Successfully.")
        return redirect('store:home')

@method_decorator(login_required, name='dispatch')
class ReservationView(View):
    def get(self, request):
        form = ReservationForm()
        return render(request, 'store/reservation.html', {'form': form})
    
    def post(self, request):
        form = ReservationForm(request.POST)
        if form.is_valid():
            user=request.user
            phone_number = form.cleaned_data['phone_number']
            telephone_number = form.cleaned_data['telephone_number']
            pax = form.cleaned_data['pax']
            event_name = form.cleaned_data['event_name']
            event_type = form.cleaned_data['event_type']
            event_time = form.cleaned_data['event_time']
            event_time_end = form.cleaned_data['event_time_end']
            event_date = form.cleaned_data['event_date']
            remarks = form.cleaned_data['remarks']
            reg = Reservation(user=user, phone_number=phone_number,telephone_number=telephone_number, pax=pax, event_name=event_name, event_type=event_type, event_time=event_time,event_time_end=event_time_end ,event_date=event_date, remarks=remarks)
            reg.save()
            messages.success(request, "Reservation Added Successfully!")
        else:
            messages.warning(request, "The Scheduled Date Is Already Taken!")
        return redirect('store:profile')

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = OrderSlipForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = OrderSlipForm
    return render (request, 'store/order_slip.html',{'form' : form})

@login_required
def remove_address(request, id):
    a = get_object_or_404(DeliveryInformation, user=request.user, id=id)
    a.delete()
    messages.success(request, "Delivery Address removed.")
    return redirect('store:profile')

@login_required
def remove_reservation(request, id):
    r = get_object_or_404(Reservation, user=request.user, id=id)
    r.delete()
    messages.success(request, "Reservation removed.")
    return redirect('store:profile')

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    item_already_in_cart = Cart.objects.filter(product=product_id, user=user)
    if item_already_in_cart:
        cp = get_object_or_404(Cart, product=product_id, user=user)
        cp.quantity += 1
        cp.save()
    else:
        Cart(user=user, product=product).save()
    
    return redirect('store:cart')

@login_required
def cart(request):
    user = request.user
    cart_products = Cart.objects.filter(user=user)


    amount = decimal.Decimal(0)
    delivery_fee = decimal.Decimal(50)

    cp = [p for p in Cart.objects.all() if p.user==user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount

    # Customer Addresses
    delivery_addresses = DeliveryInformation.objects.filter(user=user)

    context = {
        'cart_products': cart_products,
        'amount': amount,
        'delivery_fee': delivery_fee,
        'total_amount': amount + delivery_fee,
        'delivery_addresses': delivery_addresses,
    }
    return render(request, 'store/cart.html', context)

@login_required
def remove_cart(request, cart_id):
    if request.method == 'GET':
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
        messages.success(request, "Item removed from Cart.")
    return redirect('store:cart')

@login_required
def remove_favorites(request, favorites_id):
    if request.method == 'GET':
        c = get_object_or_404(Favorites, id=favorites_id)
        c.delete()
        messages.success(request, "Item remove from Favorites.")
    return redirect('store:favorites')

@login_required
def plus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        cp.quantity += 1
        cp.save()
    return redirect('store:cart')

@login_required
def minus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        if cp.quantity == 1:
            cp.delete()
        else:
            cp.quantity -= 1
            cp.save()
    return redirect('store:cart')

@login_required
def favorite_view(request):
    user = request.user
    favorite_products = Favorites.objects.filter(user=user)
    context = {
        'favorite_products': favorite_products,
    }
    return render(request, 'store/favorites.html', context)

@login_required
def add_to_favorite(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    item_already_in_favorite = Favorites.objects.filter(product=product_id, user=user)
    if item_already_in_favorite:
        messages.warning(request, "Product is already in favorites!")
    else:
        Favorites(user=user, product=product).save()

    return redirect('store:favorites')

@login_required
def checkout(request):
    user = request.user
    address_id = request.GET.get('address')
    address = get_object_or_404(DeliveryInformation, id=address_id)
    amount = decimal.Decimal(0)
    delivery_fee = decimal.Decimal(50)

    cp = [p for p in Cart.objects.all() if p.user==user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount

    order = Order.objects.create(
        user=user,
        address=address,
        total_price = amount+delivery_fee
    )
    order.save()
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderItem(invoice_no='INV-'+str(order.id),user=user,product=c.product,quantity=c.quantity,price=c.quantity*c.product.price).save()
        c.delete()
    return redirect('store:orders')
    
@login_required
def orders(request):
    order_item = OrderItem.objects.filter(user=request.user)
    order_list = Order.objects.filter(user=request.user)
    address_list = DeliveryInformation.objects.filter(user=request.user)

    template_path = 'store/orders.html'
    context = {'order_items':order_item,'order_lists':order_list,'address_lists':address_list}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reciept.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    OrderItem.objects.all().delete()
    return response

    