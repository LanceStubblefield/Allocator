from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from . models import *
import bcrypt
import matplotlib.pyplot as plt

def index(request):
    return render (request, 'index.html')

def success(request):
    if 'user' not in request.session:
        return redirect('/')
    context = {
        'wall_messages': Wall_Message.objects.all()
    }
    return render (request, 'success.html', context)

def register(request):
    print(request.POST)
    errors = User.objects.basic_validator(request.POST)
    print(errors)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
        ########
    new_user = User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=request.POST['password'])
    #### SESSION REQUEST ####
    request.session['user'] = new_user.first_name
    request.session['id'] = new_user.id
    return redirect('/success')

def validate_login(request):
    user = User.objects.filter(email=request.POST['email'])  # hm...is it really a good idea to use the get method here?
    if bcrypt.checkpw(request.POST['password'].encode(), user.pw_hash.encode()):
        print("password match")
    else:
        print("failed password")

def login(request):
    print(request.POST)
    #### RETRIEVING user from database ####
    logged_user = User.objects.filter(email=request.POST['email'])
    if len(logged_user) >0:
        logged_user = logged_user[0]
        if logged_user.password == request.POST['password']:
            request.session['user'] = logged_user.first_name
            request.session['id'] = logged_user.id
            return redirect('/success')
    return redirect('/')

# def logoff(request):

def logoff(request):
    print(request.session)
    request.session.flush()
    print(request.session)
    return redirect('/')

def post_mess(request):
    Wall_Message.objects.create(message=request.POST['mess'], poster= User.objects.get(id=request.session['id']))
    return redirect ('/success')

def post_comment(request, id):
    poster = User.objects.get(id=request.session['id'])
    message = Wall_Message.objects.get(id=id)
    Comment.objects.create(comment=request.POST['comment'], poster= poster, wall_message=message)
    return redirect('/success')


def profile(request, id):
    context= {
        'user': User.objects.get(id=id)
    }
    

    # # Data to plot
    # labels = 'Stocks', 'Bonds', 'Real Estate', 'Business', 'Gold', 'Silver', 
    # sizes = [215, 25, 150, 100, 0, 75]
    # colors = ['blue', 'lightskyblue', 'lightcoral', 'red', 'gold', 'silver' ]
    # explode = (0.1, 0, 0, 0, 0, 0)  # explode 1st slice

    # # Plot
    # plt.pie(sizes, explode=explode, labels=labels, colors=colors,
    # autopct='%1.1f%%', shadow=True, startangle=140)
    # plt.axis('equal')
    # plt.show()
    # client_age = Risk.objects.get(age=request.session['age'])
    # client_risk = Risk.objects.get(age=request.session['risk_t'])
    # Risk.objects.create(medium=request.POST['risk'], poster= User.objects.get(id=request.session['id']))
    return render (request, 'profile.html', context)


def is_old(self):

    return self.age_range_client in (self.tier3, self.tier4)

def is_risky(self):
    return self.risk_range_client in (self.medium, self.aggressive)

def add_like(request, id):
    liked_message = Wall_Message.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['id'])
    liked_message.user_likes.add(user_liking)
    return redirect('/success')

def edit(request, id):
    edit_user = User.objects.get(id=id)
    edit_user.first_name = request.POST['first_name']
    edit_user.last_name = request.POST['last_name']
    edit_user.email = request.POST['email']
    edit_user.save()
    return redirect('/success')

def delete_comment(request, id):
    destroyed = Comment.objects.get(id=id)
    destroyed.delete()
    return redirect('/success')
