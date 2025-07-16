from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Cart, CartItem
from store.models import Product
from store.models import Variation
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request,product_id):
    
    current_user=request.user
    product = Product.objects.get(id=product_id)  # Get the product by ID

    if current_user.is_authenticated:
        product_variation = []  # Initialize here

        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(
                        product=product,
                        variation_category__iexact=key,
                        variation_value__iexact=value
                    )
                    product_variation.append(variation)
                    product_variation = list(set(product_variation))  # Remove duplicates        
                except:
                    pass


        is_cart_item_exists = CartItem.objects.filter(product=product,user=current_user).exists()  # Check if the item is already in the cart
        if is_cart_item_exists:
            cart_items = CartItem.objects.filter(product=product,user=current_user)  # Use filter, not get
            ex_var_list = []
            id_list = []
            for item in cart_items:
                existing_variation = item.variation.all()
                ex_var_list.append(list(existing_variation))
                id_list.append(item.id)
        

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id_list[index]
                cart_item = CartItem.objects.get(product=product, id=item_id)
                cart_item.quantity += 1
                cart_item.save()


            else:
                cart_item = CartItem.objects.create(product=product,user=current_user, quantity=1)
                if len(product_variation) > 0:
                    item.variation.clear()  # Clear existing variations
                    item.variation.add(*product_variation)  # Add new variations
                item.save()
        
        else:
            cart_item = CartItem.objects.create(product=product,user=current_user, quantity=1)  # Create a new cart item if it doesn't exist
            if len(product_variation) > 0:
                cart_item.variation.clear()  # Clear existing variations
                cart_item.variation.add(*product_variation)  # Add new variations
            cart_item.save()  # Save the new cart item


        return redirect('cart')  # Render the cart page with the updated cart

    # if user is not authentiacted
    else:    
        
        product_variation = []  # Initialize here

        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(
                        product=product,
                        variation_category__iexact=key,
                        variation_value__iexact=value
                    )
                    product_variation.append(variation)
                    product_variation = list(set(product_variation))  # Remove duplicates        
                except:
                    pass
            
            
        product= Product.objects.get(id=product_id)  # Get the product by ID
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the cart using the session key
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()  # Save the cart instance


        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()  # Check if the item is already in the cart
        if is_cart_item_exists:
            cart_items = CartItem.objects.filter(product=product, cart=cart)  # Use filter, not get
            ex_var_list = []
            id_list = []
            for item in cart_items:
                existing_variation = item.variation.all()
                ex_var_list.append(list(existing_variation))
                id_list.append(item.id)
            


            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id_list[index]
                cart_item = CartItem.objects.get(product=product, id=item_id)
                cart_item.quantity += 1
                cart_item.save()


            else:
                cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
                if len(product_variation) > 0:
                    item.variation.clear()  # Clear existing variations
                    item.variation.add(*product_variation)  # Add new variations
                item.save()
        
        else:
            cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)  # Create a new cart item if it doesn't exist
            if len(product_variation) > 0:
                cart_item.variation.clear()  # Clear existing variations
                cart_item.variation.add(*product_variation)  # Add new variations
            cart_item.save()  # Save the new cart item


        return redirect('cart')  # Render the cart page with the updated cart


def remove_cart(request, product_id,cart_item_id):

    product=get_object_or_404(Product,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item=CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_item=CartItem.objects.get(product=product,cart=cart,id=cart_item_id)  # Get the cart item
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()  # Decrease the quantity if more than 1
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')  # Redirect to the cart page

def remove_cart_item(request, product_id,cart_item_id):
    
    product = get_object_or_404(Product, id=product_id)  # Get the product by ID
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product,user=request.user,id=cart_item_id)  # Get the cart item
    else:    
        cart = Cart.objects.get(cart_id=_cart_id(request)) 
        cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)  # Get the cart item
    cart_item.delete()  # Delete the cart item
    return redirect('cart')  # Redirect to the cart page


        

def cart(request,total=0, quantity=0, cart_items=None):
    tax=0
    grand_total=0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the cart using the session key
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)  # Get all active items in the cart
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)  # Calculate total price
            quantity += cart_item.quantity  # Calculate total quantity
        tax1=total * 0.05  # Calculate tax (5% of total)
        tax= round(total * 0.05, 2)  # Round tax to 2 decimal places
        grand_total = total + tax  # Calculate grand total
    except Cart.DoesNotExist:
        pass  # If no cart exists, we simply pass

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity, 
        'tax': tax,
        'grand_total': grand_total, 
    }


    return render(request, 'store/cart.html',context)


@login_required(login_url='login')
def checkout(request,cart_items=None, total=0, quantity=0):
    tax=0
    grand_total=0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the cart using the session key
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)  # Calculate total price
            quantity += cart_item.quantity  # Calculate total quantity
        tax1=total * 0.05  # Calculate tax (5% of total)
        tax= round(total * 0.05, 2)  # Round tax to 2 decimal places
        grand_total = total + tax  # Calculate grand total
    except Cart.DoesNotExist:
        pass  # If no cart exists, we simply pass

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity, 
        'tax': tax,
        'grand_total': grand_total, 
    }

    return render(request, 'store/checkout.html',context)  
