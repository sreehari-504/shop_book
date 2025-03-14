"""
URL configuration for ecom_codemy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.urls import path
from . import views

urlpatterns = [
    path('payment_success/',views.payment_success, name='payment_success'),
    path('shipping_info/', views.shipping_info, name='shipping_info'),
    path('checkout/', views.checkout, name='checkout'),
    path('process_order/', views.process_order, name='process_order'),
    path('view_orders/', views.view_orders, name='view_orders')
]
