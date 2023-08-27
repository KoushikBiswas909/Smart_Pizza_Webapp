from django.shortcuts import render
from home.models import Pizza
from home.models import *
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
import requests

# *************** Importing libraries for ML part *****************
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
# *****************************************************************

# For instamojo integration
from instamojo_wrapper import Instamojo
# Import API key, Token from settings
from django.conf import settings
# Initilize this class
api = Instamojo(api_key=settings.API_KEY,
                auth_token=settings.AUTH_TOKEN, endpoint="https://test.instamojo.com/api/1.1/")
# Create your views here.


# Render all pizzas with this function
def home(request):
    pizzas = Pizza.objects.all()
    data = requests.get('https://ipinfo.io/json')
    data = data.json()
    var1 = data["city"]
    var2 = data["region"]
    var3 = data["country"]
    context = {'pizzas': pizzas, 'city': var1, 'region': var2, 'country': var3}
    return render(request, 'home.html', context)

# Login function


def login_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_obj = User.objects.filter(username=username)
            if not user_obj.exists():
                messages.warning(request, 'User not found')
                return redirect('/login/')

            user_obj = authenticate(username=username, password=password)
            if user_obj:
                login(request, user_obj)
                return redirect('/')

            messages.error(request, 'Wrong Password')

            return redirect('/login/')
        except Exception as e:
            messages.error(request, 'Something went wrong')
            return redirect('/register/')
    return render(request, 'login.html')


# Register function
def register_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.error(request, 'Username is taken')
                return redirect('/register/')

            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request, 'Account Created')

            return redirect('/login/')
        except Exception as e:
            messages.error(request, 'Something went wrong')
            return redirect('/register/')
    return render(request, 'register.html')


# Add to cart function
@login_required(login_url='/login/')
def add_cart(request, pizza_uid):
    user = request.user
    pizza_obj = Pizza.objects.get(uid=pizza_uid)
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
    cart_items = CartItems.objects.create(
        cart=cart,
        pizza=pizza_obj
    )
    return redirect('/')


# Cart page rendering
@login_required(login_url='/login/')
def cart(request):
    cart = Cart.objects.get(is_paid=False, user=request.user)
    response = api.payment_request_create(
        amount=cart.get_cart_total(),
        purpose="Order",
        buyer_name=request.user.username,
        email="singhravi1093@gmail.com",
        redirect_url="http://127.0.0.1:8000/success/"
    )
    cart.instamojo_id = response['payment_request']['id']
    cart.save()
    context = {'carts': cart,
               'payment_url': response['payment_request']['longurl']}
    return render(request, 'cart.html', context)


# Cart item removing
@login_required(login_url='/login/')
def remove_cart_items(request, cart_item_uid):
    try:
        CartItems.objects.get(uid=cart_item_uid).delete()

        return redirect('/cart/')
    except Exception as e:
        print(e)


# Dashboard function
@login_required(login_url='/login/')
def orders(request):
    orders = Cart.objects.filter(is_paid=True, user=request.user)
    context = {'orders': orders}
    return render(request, 'orders.html', context)


# Success page rendering
@login_required(login_url='/login/')
def success(request):
    payment_request = request.GET.get('payment_request_id')
    cart = Cart.objects.get(instamojo_id=payment_request)
    cart.is_paid = True
    cart.save()
    return redirect('/orders/')


# Prediction model views
def predict(request):
    return render(request, 'predict.html')

# ML algorithm implemented


def result(request):
    data = pd.read_csv(
        r'C:\Users\Koushik Biswas\Downloads\pizza_new_dataset.csv')
    X = data.drop("Outcome", axis=1)
    Y = data['Outcome']
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
    model = LogisticRegression()
    model.fit(X_train, Y_train)
    val1 = int(request.GET['n1'])
    val2 = int(request.GET['n2'])
    val3 = int(request.GET['n3'])
    val4 = int(request.GET['n4'])
    pred = model.predict([[val1, val2, val3, val4]])
    result = ""
    pizza_names = {
        0: "Chicken Keema Pizza",
        1: "Papper Barbecue Chicken",
        2: "Chicken Dominator Pizza",
        3: "Spiced Double Chicken",
        4: "Panner Paratha Pizza",
        5: "Cheese n Corn",
        6: "Malai Chicken Pizza"
    }
    result = pizza_names.get(pred[0], "Classic Pizza")
    return render(request, 'predict.html', {"result1": result})


# Location tracker
def locate(request):
    return render(request, 'cart.html')
