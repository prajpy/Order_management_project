from django.shortcuts import render, redirect
from .models import Product,Customer,Order
from .forms import OrderForm,CreateUserForm,CustomerForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,adminonly
from django.contrib.auth.models import Group

@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or pwd incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutuser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles='customer')
def userpage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders':orders,'total_orders': total_orders,'delivered': delivered,
               'pending': pending,}
    return render(request,'accounts/user.html',context)

@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(form.save())
            group = Group.objects.get(name = 'customer')
            user.groups.add(group)
            Customer.objects.create(user=user)

            messages.success(request, 'User registered ')

            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)



@login_required(login_url='login')
@adminonly
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders':orders,'total_orders': total_orders,'delivered': delivered,
               'pending': pending,'customers':customers}
    return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles='customer')
def accountsettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid:
            form.save()
    context = {'form':form}
    return render(request,'accounts/account_settings.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def products(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request,'accounts/products.html',context)

@login_required(login_url='login')
def customer(request,pk_test):
    customer = Customer.objects.get(id=pk_test)
    order = customer.order_set.all()
    orders_count = order.count()

    myfilter = OrderFilter(request.GET,queryset=order)
    order = myfilter.qs


    context = {'customer':customer,'order':order,'orders_count':orders_count,'myfilter':myfilter}
    return render(request,'accounts/customer.html',context)

@login_required(login_url='login')
def CreateOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra = 5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
def UpdateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
def DeleteOrder(request,pk):
    item = Order.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('/')

    context = {'item':item}
    return render(request, 'accounts/delete_order.html', context)