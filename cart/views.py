from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    # cart_item = cart.get_cart
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, 'cart_summary.html',{'cart_products':cart_products,'quantities':quantities,'totals':totals})

def cart_add(request):
    # Get the cart
    cart = Cart(request)

    # Test for post 
    if request.POST.get('action') == 'post':
        # Get product information from product.html through AJAX
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        # Lookup product in database
        product = get_object_or_404(Product, id=product_id)

        # Add the product to cart. Save to session
        cart.add(product=product, quantity = product_qty)

        # Get the quantity of the cart
        cart_quantity = cart.__len__()

        # Return a json response
        # response = JsonResponse({'Product Name': product.name})

        response = JsonResponse({'qty': cart_quantity})
        messages.success(request,"Product added to cart")
        return response

def cart_delete(request):
    cart = Cart(request)

    # Test for post 
    if request.POST.get('action') == 'post':
        # Get product information from product.html through AJAX
        product_id = int(request.POST.get('product_id'))
        
        cart.delete(product=product_id)

        response = JsonResponse({'product':product_id})
        messages.success(request,'Product deleted successfully')
        return response

def cart_update(request):
    cart = Cart(request)

    # Test for post 
    if request.POST.get('action') == 'post':
        # Get product information from product.html through AJAX
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty':product_qty})
        messages.success(request,'Product updated successfully')
        return response