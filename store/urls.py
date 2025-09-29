from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
     path("", views.home, name="home"),  # Home shows product list
    path("product/<int:product_id>/", views.product_detail, name="product_detail"),
    
      # cart actions
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("cart/update/<int:product_id>/", views.cart_update, name="cart_update"),  # 👈 add this
    #checkout
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    
#authentication

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    
    
    path('profile/', views.profile, name='profile'),
    
    path('orders/', views.orders, name='orders'),  # ✅ THIS IS REQUIRED
    path('profile/data/', views.profile_data, name='profile_data'),
    path('search/', views.product_search, name='product_search'),



    
]






