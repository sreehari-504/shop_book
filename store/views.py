from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
import json
from cart.cart import Cart

# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html',{'products':products})

def about(request):
    return render(request, 'about.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == '' or password == '':
            messages.error(request, "Fields cannot be empty")
            return redirect('login')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Include shopping cart
            current_user = Profile.objects.get(user__id=request.user.id)
            # current_user = get_object_or_404(Profile, user=request.user)

            # Get saved cart from database
            saved_cart = current_user.old_cart

            # Convert database string to python dictionary
            if saved_cart:
                # Convert string to dictionary using JSON
                # import json
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)

                # Loop though the cart and add the items from the database
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, "You have been logged in")
            return redirect('home')
        else:
            messages.error(request, "Username or password incorrect")
            return redirect('login')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request,"Logged out successfully")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        emailid = request.POST['email-id']
        firstname = request.POST['first-name']
        lastname = request.POST['last-name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if username == '' or emailid == '' or firstname == '' or lastname == '' or password1 == '' or password2 == '':
            messages.error(request, "Some details missing. You must enter all the details")
            return redirect('register_user')
        if password1 != password2:
            messages.error(request, "Passwords didn't match")
            return redirect('register_user')
        User.objects.create_user(username = username, email=emailid, first_name = firstname, last_name = lastname, password = password1)
        user = authenticate(request, username=username, password=password1)
        Profile.objects.create(user=user)
        if user is not None:
            login(request, user)
            messages.success(request, "Succesfully registerd and logged in")
            return redirect('home')
    return render(request, 'register.html')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        
    return render(request, 'update.html')

def product(request,pk):
    product = get_object_or_404(Product,pk=pk)
    return render(request,'product.html',{'product':product})

def category(request, foo):
    foo = foo.replace('-',' ')
    
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request,'category.html',{'products':products,'category':category})
    except:
        messages.error(request,"Category doesn't exist")
        return redirect('home')

def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

        if not searched:
            messages.error(request,"Product you searched for doesn't exist")
            return render(request,'search.html')
        else:
            return render(request,'search.html',{'searched':searched})
    return render(request,'search.html')