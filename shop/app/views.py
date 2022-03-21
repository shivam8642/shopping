from ast import Add
from django.shortcuts import render
from .models import Address, Cart, Product,Slider,Cart,Order
from .forms import Signup,MyUserChangeForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate,logout as django_logout, login as auth_login
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.http.response import HttpResponseNotFound
from django.contrib.auth.models import User
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import stripe
stripe.api_key = "sk_test_51JCHcMSCnbkK9gD73iWxvZrwtRXRY6qT8ohzlGjtcKtOAB2yQ2hZqsRyoqmRmxjulTIsfJ4UEsSowieVarDb23wC00KXMJ5cvc"

# Create your views here.

def index(request):
    productList=Product.objects.all().values() 
    slider=Slider.objects.all().values()
    return render(request,"index.html",{'product':productList,'slider':slider})

def signup(request):
    if request.method=="POST":
        signupform=Signup(request.POST)
        if signupform.is_valid():
            signupform.save()
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect("login")  
    else:
        signupform=Signup()
    return render(request,"signup.html",{'form':signupform})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = auth_login(request,user)
            return redirect("index")
        else:
            messages.info(request,'invalid username or password')     
            form = AuthenticationForm()
        
    if request.user.is_authenticated:
          return redirect("index")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form':form})


def logout(request):
   django_logout(request)
   return redirect("login")    


def account(request):
    if request.user.is_authenticated:
        current_user = request.user
        updateProfileform=MyUserChangeForm(instance=request.user)
        dataset= Address.objects.filter(user_id=current_user.id)
        return render(request, 'account.html',{'updateData': updateProfileform,'dataset':dataset})      
    else:
        return redirect("login")


def updateProfile(request):
    form = MyUserChangeForm(request.POST, instance=request.user)
    username = request.POST['username']
    current_user = request.user
    email=request.POST["email"]
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exclude(id= current_user.id).exists(),
        'is_email_taken':User.objects.filter(email=email).exclude(id= current_user.id).exists()
    } 
    if request.user.is_authenticated and request.method == 'POST' and form.is_valid() and data['is_taken'] == False and data['is_email_taken'] == False:

        form.save()
        response = {'status': 'success'}
        return JsonResponse(response)
    else:    

        response = {'status': 'failed','error_data': data}
        return JsonResponse(response)

def deleteAccount(request):
    current_user = request.user
    user = User.objects.filter(id=current_user.id)
    user.delete()
    user=Address.objects.filter(user_id=current_user.id).delete()
    user=Cart.objects.filter(user_id=current_user.id).delete()
    messages.info(request,'User has been deleted')
    return redirect("login")


def password_change(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
               form.save()
               update_session_auth_hash(request,form.user)
               messages.info(request,"Your Password has been changed Successfully")
               
        else:
           form=PasswordChangeForm(user=request.user)
        return render(request,"password_change.html",{'form':form})
    else:
        return redirect("login")


def detail(request):
    if request.user.is_authenticated:
     id_call= request.GET.get('id')
     list=Product.objects.filter(id=id_call).values() 
     return render(request,"detail.html",{'product':list[0]})
    else:
        return redirect("login")


def cartCreate(request):
    product_id=request.GET["product_id"]
    current_user=request.user
    cartItem=Cart.objects.filter(product_id =product_id,user_id=current_user.id).exists()
    print(cartItem)
    if cartItem != True:
     current_user=request.user
     product=Product.objects.filter(id=product_id).values()
     obj=Cart(product_id=product_id ,price=product[0]['price'] ,quantity=1,user_id=current_user.id,created_at= datetime.date.today())
     obj.save()
     response = {'status': 'success', 'message': 'Product added to cart'}
     return JsonResponse(response)
    else:
     response = {'status': 'failed', 'message': 'Product is already exist on cart'}
     return JsonResponse(response)

def cart(request):
    current_user = request.user
    list =Cart.objects.select_related('product').filter(user_id = current_user.id)
    if len(list) > 0:
     total = 0
     for obj in list:
       total = total + (obj.quantity * obj.price)
     return render(request,"cart.html",{'cartList':list,'totalPrice':total})
    else:
        return render(request,"emptycart.html")

def removecart(request):
    cart_id=request.GET["cart_id"]
    cart=Cart.objects.filter(id=cart_id)
    cart.delete()
    response = {'status': 'success', 'message': 'item has been deleted'}
    return JsonResponse(response)
    
def updateQuantity(request):
    if request.method == 'POST':
     cart_id=request.POST["cart_id"]
     quantity=request.POST["quantity"]
     cart=Cart.objects.filter(id=cart_id).update(quantity= int(quantity))
     print(cart)
     return JsonResponse({})

def checkout(request):
    current_user = request.user
    show=Address.objects.filter(user_id=current_user.id)
    list =Cart.objects.select_related('product').filter(user_id = current_user.id)
    total = 0
    for obj in list:
     total = total + (obj.quantity * obj.price)
    return render(request,"checkout.html",{'checkList':list,'grandtotal':total,'showAddress':show})

@csrf_exempt
def addAddress(request):
    if request.method=="POST":  
        current_user = request.user
        modifyId = request.POST['modifyId']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        pincode = request.POST['pincode']
        mobile_no = request.POST['mobile_no']
        state = request.POST['state']
        city = request.POST['city']
        if modifyId:
            Address.objects.filter(id=modifyId).update(first_name=first_name,last_name=last_name,
         address=address,pincode=pincode,state=state,city=city,mobile_no=mobile_no,user_id=current_user.id)
        else:
           obj=Address(first_name=first_name ,last_name=last_name,
           address=address,pincode=pincode,state=state,city=city,mobile_no=mobile_no,user_id=current_user.id)
           obj.save()
        msg = "Update Address successfully" if modifyId else "Add Address successfully"
        response = {'status': 'success', 'message': msg}
        return JsonResponse(response)

    else:
      return render(request,"addAddress.html")
 
def deleteAddress(request):
    id = request.GET.get('id')
    address=Address.objects.filter(id=id)
    address.delete()
    response = {'status': 'success', 'message': 'Address has been deleted'}
    return JsonResponse(response)

def updateAddress(request): 
    id=request.GET["id"]
    obj=Address.objects.filter(id=id)
    jsonData = serializers.serialize("json", obj)
    return render(request, "addAddress.html", { 'formData': jsonData })
    

def checkoutSession(request):
    current_user = request.user
    addressId=request.GET.get("addressId")
    list =Cart.objects.select_related('product').filter(user_id = current_user.id)
    obj = list[0]
    print(obj)
    YOUR_DOMAIN = "http://127.0.0.1:8000"
    checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': int(obj.price * 100),
                        'product_data': {
                            'name': obj.product.product_name
                        
                        },
                    },
                    'quantity': obj.quantity,
                },
            ],
            metadata={
                "product_id": obj.product_id
            },
            mode='payment',
            success_url=YOUR_DOMAIN +'/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=YOUR_DOMAIN + '/cancel',
    )
    order = Order()
    order.product_id = obj.product_id
    order.stripe_payment_intent = checkout_session['payment_intent']
    order.price = int(obj.price)
    order.quantity = obj.quantity
    order.user_id = current_user.id
    order.status = 'Cancel'
    order.created_at = datetime.date.today()
    order.address_id=addressId
    order.save()
    return JsonResponse({
            'id': checkout_session.id
        })

def success(request):
    session_id = request.GET.get('session_id')
    if session_id is None:
       return HttpResponseNotFound()
    else:
     session = stripe.checkout.Session.retrieve(session_id)
     Order.objects.filter(stripe_payment_intent=session.payment_intent).update(status= 'success', has_paid=True)
     current_user = request.user
     Cart.objects.filter(user_id=current_user.id).delete()
     return render(request, 'success.html')
    
def cancel(request):
    return render(request,'cancel.html')

def Orderdeatil(request):
    if request.user.is_authenticated:
        current_user = request.user
        dataset= Order.objects.filter(user_id=current_user.id).order_by('-created_at')
        return render(request, "order_history.html",{'dataset':dataset})
    else:
        return redirect("login")