from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.conf import settings
import stripe
from django.core.mail import send_mail


stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
def registration(request):
    if (request.method == "POST"):
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        propic = request.FILES.get('propic')
        gender = request.POST.get("gender")
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if (password == cpassword):
            data = ecomregister(fullname=fullname, email=email, phone=phone, propic=propic, gender=gender,
                                password=password)
            data.save()
            return redirect(userlogin)
        else:
            return HttpResponse('registration failed')

    return render(request, 'registration.html')


def userlogin(request):
    if (request.method == "POST"):
        email = request.POST.get('email')
        password = request.POST.get('password')
        data = ecomregister.objects.all()
        for i in data:
            if (i.email == email and i.password == password):
                request.session['userid'] = i.id
                return redirect(userprofile)
        else:
            return HttpResponse('login failed')
    return render(request, 'userlogin.html')


def userprofile(request):
    try:
      id1 = request.session['userid']
      data = ecomregister.objects.get(id=id1)
      category = request.GET.get('category',
                               'all')  # get selected category,if there is no category selected, all option will work
      if category == 'all':
        db = sellerproduct.objects.all()
      else:
        db = sellerproduct.objects.filter(category=category)
      for item in db:
        item.size = item.size.split(',')

      return render(request, 'userprofile.html', {'data': data, 'db': db})
    except KeyError:
        return redirect(userlogin)



def updateprofile(request, id):
    data = ecomregister.objects.get(id=id)
    if (request.method == "POST"):
        if (request.FILES.get('propic') == None):
            data.save()
        else:
            data.propic = request.FILES.get('propic')
        data.fullname = request.POST.get('fullname')
        data.email = request.POST.get('email')
        data.phone = request.POST.get('phone')
        data.gender = request.POST.get('gender')
        data.save()
        return redirect(userprofile)

    return render(request, 'updateprofile.html', {'data': data})


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


def addtocart(request, itemid):
    item = sellerproduct.objects.get(id=itemid)
    cart = cartitem.objects.all()
    size = ''  # empty memory space assign
    if (request.method == 'GET'):
        size = request.GET.get('size')  # xl
    for i in cart:

        if i.item.id == itemid and i.selectedsize == size and i.userid == request.session['userid']:
            i.quantity += 1

            i.save()
            return redirect(cartdisplay)
    else:
        db = cartitem(userid=request.session['userid'], item=item, selectedsize=size)

        db.save()
        return redirect(cartdisplay)


def inc_dec(request, cartid):
    db = cartitem.objects.get(id=cartid)
    action = request.GET.get('action')
    if action == 'increment':
        db.quantity += 1
        db.save()
    elif action == 'decrement' and db.quantity > 1:
        db.quantity -= 1
        db.save()

    return redirect(cartdisplay)


# delete item from cart


# 123
def cartdisplay(request):
    userid = request.session['userid']
    db = cartitem.objects.filter(userid=userid)
    # preprocess the data
    total = 0
    count = 0
    for i in db:  # total , prod , price increment
        i.item.price *= i.quantity
        total += i.item.price
        count += 1
    db_reversed = reversed(list(db))
    return render(request, 'cartdisplay.html', {'db': db_reversed, 'total': total, 'count': count})


def addaddress(request):
    userid = request.session['userid']
    userdetails = ecomregister.objects.get(id=userid)
    if (request.method == 'POST'):
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        pincode = request.POST.get('pincode')
        city = request.POST.get('city')
        state = request.POST.get('state')
        cname = request.POST.get('cname')
        cnumber = request.POST.get('cnumber')
        db = Addressdetails(userdetails=userdetails, address_line1=address1, address_line2=address2, pincode=pincode,
                            city=city, state=state, contact_name=cname, contact_number=cnumber)
        db.save()
        return redirect(delivery_details)
    else:
        return render(request, 'add address.html')


def delivery_details(request):
    userid = request.session['userid']  # 5 #login
    data = Addressdetails.objects.filter(userdetails__id=userid)
    return render(request, 'delivery adress.html', {'data': data})


# model.objects.filter(item__prodname=prodname)

def final_summary(request):
    userid = request.session['userid']
    address_id = request.GET.get('address')
    address = Addressdetails.objects.get(id=address_id)
    cartitems = cartitem.objects.filter(userid=userid)
    key = settings.STRIPE_PUBLISHABLE_KEY  # settings
    total = 0
    striptotal = 0
    for i in cartitems:
        i.item.price *= i.quantity
        total += i.item.price
        striptotal = total * 100

    return render(request, 'summary.html',
                  {'address': address, 'cartitems': cartitems, 'total': total, 'striptotal': striptotal, 'key': key})

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.conf import settings
from datetime import datetime, timedelta

def create_order(request):  # after payment
    if request.method == 'POST':
        order_items = []
        total_price = 0
        userid = request.session['userid']  # userid session calling

        user = ecomregister.objects.get(id=userid)  # registered details

        address_id = request.POST.get('address_id')  # hidden field address id

        address = Addressdetails.objects.get(id=address_id)  # fetch address using the address id

        cart = cartitem.objects.filter(userid=userid)  # cart filter

        # Create the order object
        order = Order.objects.create(userdetails=user, address=address)  # automatically save

        # Process each item in the cart
        for i in cart:  # cart itreation
            # Create order item for each cart item
            OrderItem.objects.create(  #model
                order=order,
                order_pic=i.item.productimage,
                pro_name=i.item.product,
                quantity=i.quantity,
                price=i.item.price
            )

            total_price += i.item.price * i.quantity
            order_items.append({  #mail
                'product': i.item.product,
                'quantity': i.quantity,
                'price': i.item.price * i.quantity,

            })
        expected_delivery_date = datetime.now() + timedelta(days=7)
        # Construct email content
        subject = 'Order Confirmation'
        context = {
            'order_items': order_items,  #list of items
            'total_price': total_price, #total price
            'expected_delivery_date': expected_delivery_date.strftime('%Y-%m-%d')
        }

        html_message = render_to_string('order_confirmation_email.html', context) #string
        plain_message = strip_tags(html_message)
        from_email = 'anshyaclement123@gmail.com'
        to_email = [user.email]
        send_mail(subject,plain_message,from_email,to_email,html_message= html_message)

        cart.delete()

        return HttpResponse('Order created successfully!')


# mail sending
# order canceling
# order cancellation mai\
# reverse


import stripe





def order_view(request):
    userid = request.session['userid'] #login user id
    order = OrderItem.objects.filter(order__userdetails__id=userid).order_by('-order__ordered_date')

    return render(request, 'order.html', {'order': order})


def order_cancel(request,id):
    db=OrderItem.objects.get(id=id)  #1  #item
    db.order_status=False
    db.save()
    #email sending
    return HttpResponse('order cancelled')





#in order display page  create a order cancel button
#user the orderitem default id update the orderitem model to Flase
#send a mail to corresponding email id
#order cancel
#item details





def logout(request):
    request.session.flush()
    return redirect(index)








def index(request):
    return render(request, 'index.html')
