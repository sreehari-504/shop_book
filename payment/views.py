from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cart.cart import Cart
from payment.models import ShippingAddress, Order, OrderItem
from store.models import Product

# Create your views here.
def payment_success(request):
    return render(request,'payment_success.html')

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    # cart_item = cart.get_cart
    quantities = cart.get_quants
    totals = cart.cart_total()
    user = request.user
    print()
    try:
        shipping_info = get_object_or_404(ShippingAddress, user=user)
        return render(request, 'checkout.html',{'cart_products':cart_products,'quantities':quantities,'totals':totals,'shipping_info':shipping_info})
    except:
        pass
    return render(request, 'checkout.html',{'cart_products':cart_products,'quantities':quantities,'totals':totals})

def shipping_info(request):
    if request.method == 'POST':
        full_name = request.POST['full-name']
        email = request.POST['email']
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        zipcode = request.POST['zipcode']
        if full_name == '' or email == '' or address1 == '' or address2 == '' or city == '' or state == '' or country == '' or zipcode == '':
            messages.error(request,'Inputs cannot be empty')
            return render(request, 'shipping_info.html')
        user = request.user
        ShippingAddress.objects.create(user=user, full_name=full_name, email=email, address1=address1, address2=address2, city=city, state=state, country=country, zipcode=zipcode)
        messages.success(request, "Shipping Address saved successfully")
        return redirect('home')
    return render(request, 'shipping_info.html')

def process_order(request):
    if request.method == 'POST':
        user = request.user
        shipping_info = request.POST['shipping-detail']
        shipping_info = get_object_or_404(ShippingAddress, pk=shipping_info)
        cart = Cart(request)
        shipping_total = cart.cart_total()
        print(shipping_total)
        order = Order.objects.create(user=user, shipping_details=shipping_info, amount_paid=shipping_total)
        print(order)
        shipping_products = request.session.get('session_key')
        for key, value in shipping_products.items():
            id = int(key)
            product = Product.objects.get(id=id)
            print(product)
            
            OrderItem.objects.create(order_id=order.id, product=product, quantity=value)
        cart.cart_delete()
        messages.success(request, "Order has been created successfully")
        return render(request,'process_order.html',{'order':order})
    return render(request, 'process_order.html')

def view_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    return render(request, 'orders.html',{'orders':orders})