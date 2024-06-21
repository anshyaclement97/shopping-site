from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SellerRegistrationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from ecommerceapp.models import *




from django.http import HttpResponse
def register_sellers(request):
    return render(request,'seller_register.html',{'form':SellerRegistrationForm()})


def register_seller(request): #request='register.html'
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        #request.POST which is the method used to pass your POST data into your SellerRegistrationForm
        if form.is_valid():
            #
            password = form.cleaned_data.get('password')
            cpassword = form.cleaned_data.get('cpassword')
            if password != cpassword:
                messages.error(request, "Passwords don't match")
            else:
                user = form.save(commit=False)
                user.set_password(password)
                user.save() #coomit =True
                messages.success(request, 'Registration successful. You can now log in.')
                return HttpResponse("registration success")
        else:
            messages.error(request,"it is not a valid data")

    else:
        form = SellerRegistrationForm() #storing our form

    return render(request, 'register.html', {'form': form})  #form visible

def sellerproductupload(request):
    if (request.method == 'POST'):
        category = request.POST.get('category')
        productimage = request.FILES.get('productimage')
        product = request.POST.get('product')
        price = request.POST.get('price')
        size = request.POST.get('size')
        desc = request.POST.get('desc')
        data = sellerproduct(category=category, productimage=productimage, product=product, price=price, size=size,
                             desc=desc)
        data.save()
        return HttpResponse("upload successfully")
    return render(request, "sellerproductupload.html")
# IF IS the method is not POST
#is the form is not valid
#if password is incorrect
#success







def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        #In Django, AuthenticationForm is a built-in form class provided by the django.contrib.auth.forms module.
        # It's designed to handle user authentication, particularly for logging users into a web application.
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')


            user = authenticate(username=username, password=password)

            #When authenticate() is called, it checks the provided username and password against the User
            # records stored in the Django authentication system.IF it is found it returns the object
            #else it returns None

            if user is not None:
                login(request, user)
                #login() : function used to login authenticated Users
                request.session['sellerid']=user.id
                messages.success(request, f'You are now logged in as {username}.')
                return HttpResponse('login success')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'form is not valid')
    else:
        form=AuthenticationForm()
    return render(request, 'login.html', {'form':form})


def home(request):
    return render(request, 'sellerindex.html')


def order_list(request):
    a=OrderItem.objects.all()
    return render(request,'view.html',{'a':a})