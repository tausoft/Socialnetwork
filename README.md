<h1>Django REST example project</h1>
Django Social Network app with REST framework &amp; Postman test collections

<h1>Pre-Requisites</h1>
Python 3.8
virtualenv
Postman - create free account and download Postman desktop aplication at https://www.postman.com/ 


<h1>Setup</h1>

Navigate to dir with terminal and clone the git


- `git clone https://github.com/tausoft/Socialnetwork.git`

Setup virtual environment with Python 3.8 and activate it

Install requirements from requirements.txt file

- `pip install -r requirements.txt or pip3 install -r requirements.txt for python 3.x (in case multiple versions are installed)`

Run Django server


- `cd Socialnetwork\django_rest`
- `python manage.py runserver`

<h1>Usage</h1>

Superuser/password is admin/admin.

<b>Webapp</b>

Open localhost url (http://127.0.0.1:8000/) in browser and you will be redirected to Signup/Login form - Crispy forms module with bootstrap that already has all functionalities built in. Signup to start browsing Social Network and create new posts. You can also create a number of new users and preview/like/unlike yours or other users posts.

<b>Django REST framework</b>

API endpoints are under `http://127.0.0.1:8000/api/users/` and `http://127.0.0.1:8000/api/messages/` urls. User API is protected with IsAuthenticated permission class, so you have to login for access. Messages API is under AllowAny permission class, so you can access it without logging in.

<b>Postman Functionality tests</b>

After you login to Postman go and import Collections provided in `Socialnetwork\postman API tests` dir. You can find more informations on https://learning.postman.com/docs/getting-started/importing-and-exporting-data/

Select `Messages Collection` and click on `Run` button and than clik on `Run Messages Collection` and wait for test results. Repeat steps with `User Collection`, but note that once the user is created, re-running the test will result with `Fail` on `POST Register`. To re-run the User tests you will have to edit Body params in `POST Register` request and enter different `username`, `email` and `password`.

Happy developing :)
