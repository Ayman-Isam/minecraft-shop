from django.urls import path, reverse_lazy, include
from .views import *
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'redeem', RedeemViewSet, basename='redeem')

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('new/', ItemCreateView.as_view(), name='item-create'),
    path('<int:pk>/edit/', ItemUpdateView.as_view(), name='item-edit'),
    path('<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),
    path("login/", login_attempt, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_attempt, name="register"),
    path("success/", success, name="success"),
    path("verify/<auth_token>/", verify, name="verify"),
    path("error/", verify, name="error"),
    path('password-reset/', CustomPasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'), 
    path('password-reset-complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('cart/', cart, name='cart'),
    path('add-to-cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('increment/<int:id>/', increment_cart_item, name='increment_cart_item'),
    path('decrement/<int:id>/', decrement_cart_item, name='decrement_cart_item'),
    path('update_cart_item/<int:id>/', update_cart_item, name='update_cart_item'),
    path('remove-from-cart/<int:id>/', remove_from_cart, name='remove_from_cart'),
    path('', include(router.urls)),
    path('create_order/', create_order, name='create_order'),
    path('admin-orders/', orders, name='orders'),
    path('orders/', user_orders, name='orders'),
    path('refund/<int:order_id>/', refund_order, name='refund_order'),
    path('wishlist/', wishlist, name='wishlist'),
    path('add-to-wishlist/<int:item_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('increment-wishlist-item/<int:id>/', increment_wishlist_item, name='increment_wishlist_item'),
    path('decrement-wishlist-item/<int:id>/', decrement_wishlist_item, name='decrement_wishlist_item'),
    path('update-wishlist-item/<int:id>/', update_wishlist_item, name='update_wishlist_item'),
    path('remove-from-wishlist/<int:id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('item/<int:id>/', item_detail, name='item_detail'),
]