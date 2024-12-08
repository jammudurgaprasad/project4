from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from . models import Biryani,CartItem,Addresses,Order
from django.contrib import messages
from decimal import Decimal
from django.db import transaction

# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']


        if User.objects.filter(username=username).exists():
            messages.error(request, 'User already exists. Please choose a different username.')
            return render(request, 'register.html')

        user = User.objects.create_user(username=username,email=email,password=password)
        user.save()
        return redirect('home')
    
    return render(request,'register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Incorrect username or password')
            return render(request,'login.html')
        
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')

def add_to_cart(request, item_id):
    biryani = Biryani.objects.get(id=item_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        biryani=biryani,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'{biryani.name} added to cart!')
    return redirect('home')


def remove_from_cart(request, item_id):
    # Ensure the user is authenticated
    if request.user.is_authenticated:
        # Get the cart item based on the user and the item ID
        cart_item = get_object_or_404(CartItem, user=request.user, biryani_id=item_id)
        cart_item.delete()  # Remove the item from the cart
        messages.success(request, f'{cart_item.biryani.name} has been removed from your cart!')
    else:
        messages.error(request, 'You need to be logged in to remove items from the cart.')

    return redirect('view_cart')  # Redirect back to the cart view



# def view_cart(request):
#     cart_items = request.user.cart_items.all()  # Assuming the user is authenticated

#     # Calculate total price of the items in the cart after discount
#     total_cart_price = sum(item.total_price for item in cart_items)

#     # Calculate total M.R.P. before discount
#     total_mrp = sum(item.biryani.price * item.quantity for item in cart_items)

#     for item in cart_items:
#         item.mrp_total = item.biryani.price * item.quantity

#     # Assuming fixed values for platform fee and delivery charges
#     platform_fee = Decimal('5.00')  # Convert to Decimal
#     delivery_charges = Decimal('20.00')  # Convert to Decimal

#     # Calculate total discount for all items in the cart
#     total_discount = sum(
#         item.biryani.price * (Decimal(item.biryani.discount) / Decimal(100)) * Decimal(item.quantity) 
#         for item in cart_items
#     )

#     # Calculate the final total amount to be paid
#     final_total = total_mrp - total_discount + platform_fee + delivery_charges

#     # Prepare the context to pass to the template
#     context = {
#         'cart_items': cart_items,
#         'total_cart_price': total_cart_price,
#         'total_discount': total_discount,
#         'platform_fee': platform_fee,
#         'delivery_charges': delivery_charges,
#         'final_total': final_total,
#         'total_mrp': total_mrp,  # Pass total M.R.P. to the template
#     }
    
#     # Render the view_cart template with the context
#     return render(request, 'view_cart.html', context)


from decimal import Decimal

def view_cart(request):
    cart_items = request.user.cart_items.all()  # Assuming the user is authenticated

    # Calculate total price of the items in the cart after discount
    total_cart_price = sum(item.total_price for item in cart_items)

    # Calculate total M.R.P. before discount
    total_mrp = sum(item.biryani.price * item.quantity for item in cart_items)

    for item in cart_items:
        item.mrp_total = item.biryani.price * item.quantity

    # Assuming fixed values for platform fee and delivery charges
    platform_fee = Decimal('5.00')  # Convert to Decimal
    delivery_charges = Decimal('20.00')  # Convert to Decimal

    # Calculate total discount for all items in the cart
    total_discount = sum(
        item.biryani.price * (Decimal(item.biryani.discount) / Decimal(100)) * Decimal(item.quantity) 
        for item in cart_items
    )

    # Check if the cart is empty
    is_cart_empty = len(cart_items) == 0

    # Calculate the final total amount to be paid (exclude fees if the cart is empty)
    if not is_cart_empty:
        final_total = total_mrp - total_discount + platform_fee + delivery_charges
    else:
        final_total = Decimal('0.00')

    # Prepare the context to pass to the template
    context = {
        'cart_items': cart_items,
        'total_cart_price': total_cart_price,
        'total_discount': total_discount,
        'platform_fee': platform_fee if not is_cart_empty else 0,  # Pass None if cart is empty
        'delivery_charges': delivery_charges if not is_cart_empty else 0,  # Pass None if cart is empty
        'final_total': final_total,
        'total_mrp': total_mrp,  # Pass total M.R.P. to the template
        'is_cart_empty': is_cart_empty,
    }
    
    # Render the view_cart template with the context
    return render(request, 'view_cart.html', context)



def home(request):
    # Fetch all biryani items
    biryanis = Biryani.objects.all()
    
    # Group biryanis by category
    categories = {}
    for biryani in biryanis:
        if biryani.category not in categories:
            categories[biryani.category] = []
        categories[biryani.category].append(biryani)

    return render(request, 'home.html', {'categories': categories})

def profile(request):
    return render(request, 'profile.html')




def add_address(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        phone = request.POST['phone']
        pincode = request.POST['pincode']
        state = request.POST['state']
        city = request.POST['city']
        doorno = request.POST['doorno']
        area = request.POST['area']

        Addresses.objects.create(
            user=request.user,
            fullname=fullname,
            phone=phone,
            pincode=pincode,
            state=state,
            city=city,
            doorno=doorno,
            area=area
        )
        messages.success(request, 'Address added successfully!')
        return redirect('addresses')  # Redirect to profile page after adding

    return render(request, 'add_address.html')


def delete_address(request, id):
    address = get_object_or_404(Addresses, id=id, user=request.user)  # Ensure the address belongs to the logged-in user
    if request.method == 'POST':
        address.delete()
        messages.success(request, 'Address deleted successfully!')
        return redirect('addresses')  # Redirect back to the addresses list after deletion

    return render(request, 'delete_address.html', {'address': address})

def addresses(request):
    addresses = request.user.addresses.all()
    return render(request, 'addresses.html', {'addresses': addresses})




def place_order(request):
    if request.method == "POST":
        cart_items = request.user.cart_items.all()
        selected_address = request.POST.get('address')

        if not selected_address:
            messages.error(request, "Please select an address to place the order.")
            return redirect('cart_page')

        # Ensure the selected address belongs to the user
        address = request.user.addresses.get(id=selected_address)

        if cart_items:
            with transaction.atomic():  # Ensure atomicity
                for cart_item in reversed(cart_items):  # Reverse order
                    Order.objects.create(
                        user=request.user,
                        biryani=cart_item.biryani,
                        quantity=cart_item.quantity,
                        total_price=cart_item.total_price,
                        status='Pending',  # Set initial order status to "Pending"
                        address=address  # Assign the selected address
                    )
                    cart_item.delete()  # Remove item from cart

            messages.success(request, "Your order has been placed successfully!")
        else:
            messages.error(request, "Your cart is empty.")
        
        return redirect('orders_page')    


def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'Pending':  # Only allow cancelling pending orders
        order.status = 'Cancelled'
        order.save()
        messages.success(request, f'Order {order.biryani.name} has been cancelled.')
    else:
        messages.error(request, "Order cannot be cancelled.")
    
    return redirect('orders_page')

def orders_page(request):

    orders = request.user.orders.all().order_by('-order_date')  # Latest orders first

    context = {
        'orders': orders
    }
    return render(request, 'orders.html', context)


def agentpage(request):
    orders = Order.objects.filter(status='Pending')
    user = request.user
    return render(request,'agent.html',{'orders':orders,'user':user})

def delivered(request,item_id):
    order = get_object_or_404(Order, id=item_id)
    if order.status == 'Pending':
        order.status = 'Delivered'
        order.save()
    return redirect('agent')


def aboutus(request):
    return render(request,'aboutus.html')

def menupage(request):
    return render(request,'menupage.html')

def offerspage(request):
    return render(request,'offerspage.html')

def contactus(request):
    return render(request,'contactus.html')