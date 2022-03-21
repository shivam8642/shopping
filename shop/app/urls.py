from unicodedata import name
from django.urls import path
from app import views 
urlpatterns = [
    path("",views.index, name="index"),
    path("signup",views.signup,name="signup"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("account",views.account,name="account"),
    path("updateProfile",views.updateProfile,name="updateProfile"), 
    path("deleteAccount",views.deleteAccount,name="deleteAccount"),
    path("password_change",views.password_change,name="password_change"),
    path("detail",views.detail,name="detail"),
    path("cartCreate",views.cartCreate,name="cartCreate"),
    path("cart",views.cart,name="cart"),
    path("removecart",views.removecart,name="removecart"),
    path("updateQuantity",views.updateQuantity,name="updateQuantity"),
    path("checkout",views.checkout,name="checkout"),
    path("addAddress",views.addAddress,name="addAddress"),
    path("deleteAddress",views.deleteAddress,name="deleteAddress"),
    path("updateAddress",views.updateAddress,name="updateAddress"),
    path("checkoutSession",views.checkoutSession,name="checkoutSession"),
    path("success",views.success,name="success"),
    path("Orderdeatil",views.Orderdeatil,name="Orderdeatil"),
    path("cancel",views.cancel,name="cancel")
]