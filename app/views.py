from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import json

# Create your views here.
def detail_page(request):
  quantity=0
  id=request.GET.get('id','')
  product = Product.objects.get(id=id)
  products = Product.objects.filter(id__lte=5)
  product_category = product.category.all()
  categories = Categorie.objects.filter(is_sub = False)
  if request.user.is_authenticated:
    customer = request.user
    order, created = Order.objects.get_or_create(customer = customer,complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
  else:
    items = []
    order = {'get_cart_total':0,'get_cart_items':0}
    cartItems = order['get_cart_items']
  for i in items:
    if i.product.id == product.id:
      quantity = i.quantity
  context= {'products':products,'product':product,'quantity': quantity,'order':order,'cartItems':cartItems,'categories': categories,'product_category': product_category}
  return render(request,'app/detail.html',context)

def category(request):
  categories = Categorie.objects.filter(is_sub = False)
  active_category = request.GET.get('category','')
  if active_category:
    products = Product.objects.filter(category__slug = active_category)
  if request.user.is_authenticated:
    customer = request.user
    order, created = Order.objects.get_or_create(customer = customer,complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
  else:
    items = []
    order = {'get_cart_total':0,'get_cart_items':0}
    cartItems = order['get_cart_items']
  context ={'categories':categories,'active_category':active_category,'products':products,'cartItems':cartItems}
  return render(request,'app/category.html',context)

def search(request):
  if request.method == "POST":
    searched = request.POST["searched"]
    keys = Product.objects.filter(name__contains = searched)
  if request.user.is_authenticated:
    customer = request.user
    order, created = Order.objects.get_or_create(customer = customer,complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
  else:
    items = []
    order = {'get_cart_total':0,'get_cart_items':0}
    cartItems = order['get_cart_items']
  products = Product.objects.all()
  categories = Categorie.objects.filter(is_sub = False)
  context= {'searched': searched,"keys": keys,'products': products,'cartItems':cartItems,'categories':categories}
  return render(request,'app/search.html',context)

def register(request):
  form = CreateUserForm()
  if request.method == "POST":
    form = CreateUserForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('login')
  context = {'form': form}
  return render(request,'app/register.html',context)

def loginPage(request):
  if request.user.is_authenticated:
    return redirect('home')
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request,username=username,password=password)
    if user is not None:
      login(request,user)
      return redirect('home')
    else: messages.info(request,'User or password not correct')
  context = {}
  return render(request,'app/login.html',context)
def logoutPage(request):
  logout(request)
  return redirect('login')

def home(request):
  if request.user.is_authenticated:
    customer = request.user
    order, created = Order.objects.get_or_create(customer = customer,complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
  else:
    items = []
    order = {'get_cart_total':0,'get_cart_items':0}
    cartItems = order['get_cart_items']
  banners = Banner.objects.all()[:3]
  products = Product.objects.all()
  categories = Categorie.objects.filter(is_sub = False)
  context= {'products': products,'cartItems': cartItems,'categories': categories,'banners': banners}
  return render(request,'app/home.html', context)

def cart(request):
  if request.user.is_authenticated:
    customer = request.user
    order, created = Order.objects.get_or_create(customer = customer,complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
  else:
    items = []
    order = {'get_cart_total':0,'get_cart_items':0}
    cartItems = order['get_cart_items']
  categories = Categorie.objects.filter(is_sub = False)
  context= {'items':items,'order':order,'cartItems':cartItems,'categories': categories}
  return render(request,'app/cart.html', context)

def checkout(request):
  if request.user.is_authenticated:
    customer = request.user
    order, created = Order.objects.get_or_create(customer = customer,complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
  else:
    items = []
    order = {'get_cart_total':0,'get_cart_items':0}
    cartItems = order['get_cart_items']
  categories = Categorie.objects.filter(is_sub = False)
  context= {'items':items,'order':order,'cartItems':cartItems,'categories': categories}
  # thanhtoan
  if request.method == "POST":
    name = request.POST.get("name", "").strip()
    address = request.POST.get("address", "").strip()
    mobile = int(request.POST.get("mobile", "").strip())
    identify = request.POST.get("identify", "").strip()

    # Kiểm tra nếu bất kỳ trường nào bị bỏ trống
    if not name or not address or not mobile or not identify:
      context['error'] = "Vui lòng điền đầy đủ thông tin trước khi thanh toán!"
      return render(request, 'app/checkout.html', context)
    if mobile<0 or mobile>=1000000000000:
      context['error'] = "Sai số điện thoại"
      return render(request, 'app/checkout.html', context)
    # Thực hiện lưu vào cơ sở dữ liệu hoặc xử lý thêm
    # ...
    order.name = name
    order.address = address
    order.numberphone = mobile
    order.transaction_id = identify
    order.complete =True
    order.save()
    return HttpResponse("Thông tin thanh toán đã được xử lý thành công!")
  return render(request,'app/checkout.html', context)

def updateItem(request):
  data = json.loads(request.body)
  productId = data['productId']
  action = data['action']
  customer = request.user
  product = Product.objects.get(id = productId)
  order, created = Order.objects.get_or_create(customer = customer,complete=False)
  orderItem, created = OrderItem.objects.get_or_create(order = order,product = product)
  if (action == 'add'):
    if(product.remaining_quantity>0):
      orderItem.quantity +=1
      product.purchased_quantity+=1
      product.save()
  elif action == 'remove':
    orderItem.quantity -=1
    product.purchased_quantity-=1
    product.save()
  orderItem.save()
  if orderItem.quantity<=0:
    orderItem.delete()
  return JsonResponse('added',safe=False)

def contact(request):
  return render(request, 'app/contact.html')

def introduce(request):
  return render(request, 'app/introduce.html')

def manage(request):
  return render(request,'app/admin')

