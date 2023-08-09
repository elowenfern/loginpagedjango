from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control, never_cache
from django.contrib import messages

# Create your views here.
def custom(view_function):
    def wrapper(request, *args, **kwargs):
        print("Hey, hello!")
        return view_function(request, *args, **kwargs)
    return wrapper
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
@custom
def homepage(request):
    return render(request,'home.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def signup(request):
    if 'username' in request.session:
        return redirect('homepage')
    elif request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if not (uname and email and pass1 and pass2):
            messages.info(request,"please fill required field")
            return redirect('signup')
        elif pass1 != pass2:
           messages.info(request,"Password Mismatch")
           return redirect('signup')
        else: 
            if User.objects.filter(username = uname).exists():
                messages.info(request,"Username already taken")
                return redirect('signup')
            elif User.objects.filter(email = email).exists():
                messages.info(request,"Email already taken")
                return redirect ('signup')
            else:
                my_user=User.objects.create_user(uname,email,pass1)
                my_user.save()
        return redirect('login')    
    
    return render(request,'signup.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def loginpage(request):
    if 'username' in request.session:
        return redirect('homepage')   
    elif request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            request.session['username'] = username
            login(request,user)
            return redirect('homepage')
        else:
            return HttpResponse("<h1>User name or password is not correct!!!!<h1>")
       
    return render(request,'login.html')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def logoutpage(request):
    if 'username'in request.session:
        del request.session['username']
        logout(request)
    return redirect('login')
    
