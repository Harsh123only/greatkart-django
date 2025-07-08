from django.shortcuts import render

# Create your views here.


def crats(request):
    context = {
        'title': 'Cart',
        'message': 'This is your cart page.'
    }
    return render(request, 'store/cart.html')