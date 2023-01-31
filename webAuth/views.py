from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout




def signin(request):
    
    if request.method == "POST":
        
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(username=email, password=password)
        
        if user is not None:
            login(request, user)
            # messages.success(request, 'Login Success.')
            return redirect('home')
        
        messages.error(request, 'Invaild Creadentails.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            
    return render(request, 'webAuth/signin.html')



def signup(request):
    
    if request.method == "POST":
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            c_psd = request.POST['c_psd']
            
            if password != c_psd:
                messages.warning(request, 'Password is not Matching.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            if first_name == '':
                messages.warning(request, 'Firstname Required.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            if last_name == '':
                messages.warning(request, 'Lastname Required.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    
                
            if email == '':
                messages.warning(request, 'Email Required.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            if password == '':
                messages.warning(request, 'Password Required.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                
            if c_psd == '':
                messages.warning(request, 'Confirm Password Required.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    
            
            
            try:
                username = User.objects.get(email=email)
                if username:
                    messages.error(request, 'User is Already Exits. Please Sign In.')
                    return redirect('signin')
            
            except Exception as e:
                print(e)
            
            
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            messages.success(request, 'Your Account has been Succesfully Created. Please Login In')
            return redirect('signin')
        
    return render(request, 'webAuth/signup.html')



def signout(request):
    logout(request)
    messages.info(request, 'Logout Success.')
    return redirect('signin')