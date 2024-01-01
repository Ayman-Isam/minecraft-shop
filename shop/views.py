from datetime import datetime, timedelta
import uuid
from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetCompleteView
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger    
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import RedeemForm
from .models import Item, Cart, Redeem, Profile, Order, OrderItem, Wishlist
from .serializers import RedeemSerializer
from rest_framework import viewsets
from .decorators import unauthenticated_user


class HomePageView(ListView):
    model = Item
    template_name = 'home.html'
    context_object_name = 'items'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        categories = self.request.GET.getlist('category')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        stocks = self.request.GET.getlist('stock')

        if categories:
            queryset = queryset.filter(category__in=categories)
        if min_price and max_price:
            queryset = queryset.filter(price__range=(min_price, max_price))
        elif min_price:
            queryset = queryset.filter(price__gte=min_price)
        elif max_price:
            queryset = queryset.filter(price__lte=max_price)
        if stocks:
            queryset = queryset.filter(stock__in=stocks)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.request.GET.getlist('category')
        context['min_price'] = self.request.GET.get('min_price', '0')
        context['max_price'] = self.request.GET.get('max_price', '100')
        context['stocks'] = self.request.GET.getlist('stock')
        context['messages'] = messages.get_messages(self.request)
        return context


class ItemCreateView(UserPassesTestMixin, CreateView):
    model = Item
    template_name = 'item_new.html'
    fields = ('name', 'image', 'price', 'description', 'quantity', 'unit', 'stock', 'category')
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.is_superuser

class ItemUpdateView(UserPassesTestMixin, UpdateView):
    model = Item
    template_name = 'item_edit.html'
    fields = ('name', 'image', 'price', 'description', 'quantity', 'unit', 'stock', 'category')
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.is_superuser    

class ItemDeleteView(UserPassesTestMixin, DeleteView):
    model = Item
    template_name = 'item_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.is_superuser

class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('password_reset')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            response = super().form_valid(form)
            messages.success(self.request, 'Password reset link has been sent.')
        else:
            messages.error(self.request, 'This email is not valid.')
        return HttpResponseRedirect(self.get_success_url())

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    def get(self, request, *args, **kwargs):
        messages.success(request, 'Your password has been reset', extra_tags='toast-success')
        return redirect('login') 

#Decorator to prevent logged in user from viewing login page 
@unauthenticated_user
def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.error(request, 'User not found', extra_tags='toast-error')
            return redirect('/login/')

        profile_obj = Profile.objects.filter(user = user_obj).first()

        if not profile_obj.is_verified:
            messages.error(request, 'Profile is not verified, check your email', extra_tags='toast-error')
            return redirect('/login/')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Wrong Password', extra_tags='toast-error')
            return redirect('/login/')

        login(request, user)
        return redirect('/')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

#Decorator to prevent logged in user from viewing register page  
@unauthenticated_user
def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            if User.objects.filter(username=username).first():
                messages.error(request, 'Username is taken.', extra_tags='toast-error')
                return redirect('/register/')
            if User.objects.filter(email=email).first():
                messages.error(request, 'Email is taken.', extra_tags='toast-error')
                return redirect('/register/')
            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()
            send_mail_after_register(email, auth_token)
            messages.success(request, 'An email has been sent for account verification', extra_tags='toast-success')
            return redirect('/login/')
        except Exception as e:
            print(e)
    return render(request, 'register.html')

def success(request):
    return render(request,'success.html')  


def verify (request, auth_token):
    try: 
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified')
                return redirect('/')

            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified')
            return redirect('/login/')
        else:
            return redirect('/error/')
    except Exception as e:
        print(e)


def error_page(request):
    return render(request, 'error.html')

def send_mail_after_register(email, token):
    subject = "Your account needs to be verified"
    message = f"Hi, paste the link to verify your account http://cantankerousally.pythonanwhere.com/verify/{token}/"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)  

class RedeemViewSet(viewsets.ModelViewSet):
    queryset = Redeem.objects.all()
    serializer_class = RedeemSerializer

@login_required
def cart(request):
    carts = Cart.objects.filter(user=request.user)
    cart_subtotal = sum(cart.get_total_item_price() for cart in carts)
    active_selection = Item.objects.filter(cart__in=carts)
    redeem_form = RedeemForm()
    if request.method == 'POST':
        redeem_form = RedeemForm(request.POST)
        if redeem_form.is_valid():
            code = redeem_form.cleaned_data['code']
            try:
                redeem_obj = Redeem.objects.get(code__iexact=code, redeemed=False)
                diamonds = redeem_obj.diamonds
                request.user.profile.balance += diamonds  # add diamonds to user's balance
                request.user.profile.save()
                redeem_obj.redeemed = True  # mark code as redeemed
                redeem_obj.save()
                messages.success(request, f'{diamonds} diamonds added to your account.')
            except Redeem.DoesNotExist:
                messages.error(request, 'Invalid code.')
    return render(request, 'cart.html', {'carts': carts, 'cart_subtotal': cart_subtotal, 'active_selection': active_selection, 'redeem_form': redeem_form})

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user, item=item)
    try:
        wishlist = Wishlist.objects.get(user=request.user, item=item)
        if created:
            cart.quantity = wishlist.quantity
        else:
            if request.path == reverse('home'):
                cart.quantity += 1
            else:
                cart.quantity += wishlist.quantity
        wishlist.delete()  # delete the Wishlist object
    except Wishlist.DoesNotExist:
        if request.path == reverse('home') and not created:
            cart.quantity += 1
    cart.save()
    messages.success(request, f'{item.name} has been added to your cart. Click <a href="/cart/">here</a> to view your cart.')
    return redirect('home')

@login_required
def increment_cart_item(request, id):
    cart_item = get_object_or_404(Cart, id=id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required
def decrement_cart_item(request, id):
    cart_item = get_object_or_404(Cart, id=id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

@login_required
def update_cart_item(request, id):
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, id=id)
        new_quantity = request.POST.get('quantity')
        if new_quantity:
            cart_item.quantity = int(new_quantity)
            cart_item.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, id):
    cart_item = get_object_or_404(Cart, id=id)
    cart_item.delete()
    return redirect('cart')

@login_required
def create_order(request):
    if request.method == "POST":
        user = request.user
        profile = Profile.objects.get(user=user)
        x_coordinate = request.POST.get("x-coordinate")
        z_coordinate = request.POST.get("z-coordinate")
        new_total_cost_str = request.POST.get("new_total_cost", "0")
        shipping_option = request.POST.get("shipping-option")

        try:
            new_total_cost = Decimal(new_total_cost_str)
        except InvalidOperation:
            messages.error(request, "Invalid total cost.")
            return render(request, "error.html", {"message": "Invalid total cost."})

        if shipping_option == "standard-shipping":
            date_delivery = datetime.now() + timedelta(days=3)
        elif shipping_option == "express-shipping":
            date_delivery = datetime.now() + timedelta(days=1)
        else:
            date_delivery = None

        if new_total_cost <= profile.balance:
            profile.balance -= new_total_cost
            profile.save()

            order = Order(user=user, x_coordinate=x_coordinate, z_coordinate=z_coordinate, cart_total=new_total_cost, date_delivery=date_delivery)
            order.save()

            cart_items = Cart.objects.filter(user=user)
            for cart_item in cart_items:
                order_item = OrderItem(order=order, item=cart_item.item, quantity=cart_item.quantity, price=cart_item.item.price)
                order_item.save()

            cart_items.delete()

            return redirect("orders")
        else:
            messages.error(request, "Insufficient balance.")
            return redirect("cart")

    return render(request, "cart.html")

@user_passes_test(lambda u: u.is_superuser)
def orders(request):
    orders = Order.objects.all().order_by("-id")
    for order in orders:
        order_items = order.orderitem_set.all().order_by("-id")
        order.order_items = order_items
    return render(request, "orders.html", {"orders": orders})

@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-id")
    for order in orders:
        order_items = order.orderitem_set.all().order_by("-id")
        order.order_items = order_items
    return render(request, "orders.html", {"orders": orders})

@user_passes_test(lambda u: u.is_superuser)
def refund_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status == 'cancelled':
        messages.warning(request, 'This order has already been cancelled.')
    elif order.status == 'delivered':
        messages.warning(request, 'This order has already been delivered.')
    else:
        user = order.user
        profile = Profile.objects.get(user=user)
        refund_amount = order.cart_total
        profile.balance += refund_amount
        profile.save()
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Your order has been cancelled and your money has been refunded. Sorry for the inconvenience.')
    return redirect('orders')

@login_required
def wishlist(request):
    wishlists = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlists': wishlists})

@login_required
def add_to_wishlist(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, item=item)
    if not created:
        wishlist.quantity += 1
        wishlist.save()
        messages.success(request, f'{item.name} has been added to your wishlist. Click <a href="/wishlist/">here</a> to view your wishlist.')
    else:
        messages.success(request, f'{item.name} has been added to your wishlist. Click <a href="/wishlist/">here</a> here to view your wishlist.')
    return redirect('home')

@login_required
def increment_wishlist_item(request, id):
    wishlist_item = get_object_or_404(Wishlist, id=id)
    wishlist_item.quantity += 1
    wishlist_item.save()
    return redirect('wishlist')

@login_required
def decrement_wishlist_item(request, id):
    wishlist_item = get_object_or_404(Wishlist, id=id)
    if wishlist_item.quantity > 1:
        wishlist_item.quantity -= 1
        wishlist_item.save()
    else:
        wishlist_item.delete()
    return redirect('wishlist')

@login_required
def update_wishlist_item(request, id):
    if request.method == 'POST':
        wishlist_item = get_object_or_404(Wishlist, id=id)
        new_quantity = request.POST.get('quantity')
        if new_quantity:
            wishlist_item.quantity = int(new_quantity)
            wishlist_item.save()
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, id):
    wishlist_item = get_object_or_404(Wishlist, id=id)
    wishlist_item.delete()
    return redirect('wishlist')

def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    context = {'item': item}
    return render(request, 'item_detail.html', context)

