from django.shortcuts import  render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db import connection
from .models import Messages, Like
import requests, json, datetime, time, threading


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            user_enrichment(user)
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="registration/register.html", context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="registration/login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("/")



def start_new_thread(function):
    def decorator(*args, **kwargs):
        t = threading.Thread(target = function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator

@start_new_thread
def user_enrichment(user):
    now = datetime.datetime.now()
    now_year = now.strftime("%Y")
    now_month = now.strftime("%m")
    now_day = now.strftime("%d")

    #now_month = '05'
    #now_day = '01'
    
    status_country = ''
    status_holidays = ''
    country = []
    holidays = []

    retry_trigger = True
    counter_429 = 0
    counter_5xx = 0

    while retry_trigger:
        response_geolocation = requests.get("https://ipgeolocation.abstractapi.com/v1/?api_key=b790759a6501487e9d49d4b8a1f39581")

        status_country = str(response_geolocation.status_code)
        #status_country = '204'
        print('geolocation_status_log: ' + str(status_country))

        if status_country[0] == '2':
            if status_country == '200':
                country = json.loads(response_geolocation.content)
                print(str(country['country_code']))
                user.geolocation_status = int(status_country)
                user.geolocation_data = str(country['country_code'])
                retry_trigger = False
            else:
                user.geolocation_status = int(status_country)
                user.geolocation_data = 'No location data for the IP address'
                retry_trigger = False
        elif status_country == '429':
            while counter_429 < 10:
                print('Error ' + status_country + ', waiting 1s for retry')
                time.sleep(1)
                counter_429 += 1
            if counter_429 == 10:
                print('Error ' + status_country + ', please try again later.')
                user.geolocation_status = int(status_country)
                user.geolocation_data = 'Connection error'
                retry_trigger = False
        elif status_country[0] == '5':
            if counter_5xx == 0:
                print('Error ' + status_country + ', waiting 5s for retry')
                time.sleep(5)
            elif counter_5xx == 1:
                print('Error ' + status_country + ', waiting 10s for retry')
                time.sleep(10)
            elif counter_5xx == 2:
                print('Error ' + status_country + ', waiting 15s for retry')
                time.sleep(15)
            else:
                print('Error ' + status_country + ', please try again later.')
                user.geolocation_status = int(status_country)
                user.geolocation_data = 'Connection error'
                retry_trigger = False
            counter_5xx += 1
        else:
            print('Abstract API - Geolocation Failed to load the data')
            print('Error ' + status_country + ', please try again later.')
            user.geolocation_status = int(status_country)
            user.geolocation_data = 'Connection error'
            retry_trigger = False

    if status_country == '200':
        retry_trigger = True
    else:
        user.holiday_data = 'Geolocation data Error'
    counter_429 = 0
    counter_5xx = 0

    while retry_trigger:
        response_holidays = requests.get('https://holidays.abstractapi.com/v1/?api_key=2dead08c354a4972aada5344fc5c2e7f&country=' + str(country['country_code']) + '&year=' + str(now_year) + '&month=' + str(now_month) + '&day=' + str(now_day))
        
        status_holidays = str(response_holidays.status_code)
        #status_holidays = '400'
        print('holidays_status_log: ' + str(status_holidays))

        if status_holidays[0] == '2':
            if status_holidays == '200':
                holidays = json.loads(response_holidays.content)
                if not holidays:
                    print('There are no holidays in ' + str(country['country_code']) + ' on signup date')
                    user.holiday_data = 'There are no holidays in ' + str(country['country_code']) + ' on signup date'
                else:
                    print('Writing holiday data')
                    user.holiday_data = holidays
                user.holiday_status = int(status_holidays)
                retry_trigger = False
            else:
                print('Abstract API - There is no holiday data for the submitted country code')
                user.holiday_status = int(status_holidays)
                user.holiday_data = 'No holiday data for the submitted country code'
                retry_trigger = False
        elif status_holidays == '429':
            while counter_429 < 10:
                print('Error ' + status_holidays + ', waiting 1s for retry')
                time.sleep(1)
                counter_429 += 1
            if counter_429 == 10:
                print('Error ' + status_holidays + ', please try again later.')
                user.holiday_status = int(status_holidays)
                user.holiday_data = 'Connection error'
                retry_trigger = False
        elif status_holidays[0] == '5':
            if counter_5xx == 0:
                print('Error ' + status_holidays + ', waiting 5s for retry')
                time.sleep(5)
            elif counter_5xx == 1:
                print('Error ' + status_holidays + ', waiting 10s for retry')
                time.sleep(10)
            elif counter_5xx == 2:
                print('Error ' + status_holidays + ', waiting 15s for retry')
                time.sleep(15)
            else:
                print('Error ' + status_holidays + ', please try again later.')
                user.holiday_status = int(status_holidays)
                user.holiday_data = 'Connection error'
                retry_trigger = False
            counter_5xx += 1
        else:
            print('Error ' + status_holidays + ', please try again later.')
            user.holiday_status = int(status_holidays)
            user.holiday_data = 'Connection error'
            retry_trigger = False

    user.save()
    connection.close()


@login_required
def index(request):
    messages_data = Messages.objects.all()
    user = request.user
    arg = {"messages_data": messages_data, "user": user}

    return render(request, "index.html", arg)

def submit_message(request):
    if request.method == "POST":
        current_user = request.user
        message = request.POST["message"]
        author = current_user
        email = current_user.email

        messages_table = Messages(message=message, email=email, author=author)
        messages_table.save()

        return HttpResponseRedirect('/')

def new_like(request):
    user = request.user
    if request.method == 'POST':
        message_id = request.POST['message_id']
        message_obj = Messages.objects.get(id=message_id)

        if user in message_obj.liked.all():
            message_obj.liked.remove(user)
        else:
            message_obj.liked.add(user)

        like, created = Like.objects.get_or_create(user=user, messages_id=message_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

        like.save()

    return redirect('/')
