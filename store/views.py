from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem, UserProfile, Review
from .cart import Cart
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import login ,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

from .forms import UserForm, UserProfileForm  # import forms
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Order
from django.db.models import Q






# ---------------- Home & Product Detail -----------------
def home(request):
    products = Product.objects.all()
    return render(request, "product_list.html", {"products": products})




def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.all().order_by("-created_at")  # ✅ show ALL reviews

    if request.method == "POST" and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={
                    "rating": form.cleaned_data["rating"],
                    "comment": form.cleaned_data["comment"],
                },
            )
            return redirect("product_detail", product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, "product_detail.html", {
        "product": product,
        "reviews": reviews,
        "form": form,
    })



@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart_detail.html', {'cart': cart})

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1

    cart.add(product=product, quantity=quantity, update_quantity=True)
    return redirect('cart_detail')

# ---------------- Checkout -----------------


@login_required
# store/views.py
def checkout(request):
    cart = Cart(request)

    if cart.__len__() == 0:
        messages.warning(request, "Your cart is empty!")
        return redirect('home')

    full_name = phone = address = ''

    if request.user.is_authenticated:
        full_name = request.user.get_full_name() or request.user.username
        profile = getattr(request.user, 'userprofile', None)
        if profile:
            phone = profile.phone
            address = profile.address

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()

        if not all([full_name, phone, address]):
            messages.error(request, "Please fill all fields.")
            return render(request, 'checkout.html', {
                'cart': cart,
                'full_name': full_name,
                'phone': phone,
                'address': address
            })

        # Create order
        order = Order.objects.create(
            user=request.user,
            total_price=cart.get_total_price(),
            full_name=full_name,
            phone=phone,
            address=address
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price']
            )

        cart.clear()
        return redirect('order_success', order_id=order.id)

    return render(request, 'checkout.html', {
        'cart': cart,
        'full_name': full_name,
        'phone': phone,
        'address': address
    })


# ---------------- Order Success -----------------
def order_success(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, 'order_success.html', {'order': order})


#authetication

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken")
            return render(request, 'signup.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, "Account created and logged in!")
        return redirect('home')

    return render(request, 'signup.html')




@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user).prefetch_related("items__product")
    return render(request, "orders.html", {"orders": user_orders})



@login_required
def profile_data(request):
    user = request.user
    profile = user.userprofile

    # user info
    user_info = {
        "username": user.username,
        "email": user.email,
        "phone": profile.phone,
        "address": profile.address,
    }

    # orders info
    orders = []
    for order in Order.objects.filter(user=user).order_by("-created_at"):
        orders.append({
            "id": order.id,
            "total_price": float(order.total_price),
            "status": order.status,
            "created_at": order.created_at.strftime("%Y-%m-%d %H:%M"),
        })

    return JsonResponse({"user_info": user_info, "orders": orders})


@login_required
def profile(request):
    user = request.user
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "✅ Profile updated successfully!")
            return redirect("profile")
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, "profile.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })



def product_search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
    return render(request, 'product_list.html', {'products': products, 'query': query})