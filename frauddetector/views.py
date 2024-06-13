from django.shortcuts import render, redirect
import pandas as pd
from django.contrib import messages
from contact.models import contactform
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from keras.models import load_model
import pickle
import numpy as np



@login_required(login_url="/login")
def home(request):

    if request.method=="POST":

        if request.FILES == '':
            msg = "choose a file to upload"

            return render(request,'index.html',{'message':msg})

        else:

         uploaded_file = request.FILES['file']
        
         df = pd.read_csv(uploaded_file)
         df1= np.array(df)


         nnmodel =load_model('prediction_model.h5')

         nnpred = nnmodel.predict(df)
         output1 = nnpred.round()
         if output1 == 1:
           transaction = 'Fraud'
           statem = 'This transaction is more likely to be fraud' 
    
         else:
           transaction = 'Valid'
           statem = 'This transaction is more likely to be valid'
   

         return render(request,'index.html',{'prediction_text5':transaction, 'statement':statem })    


    return render(request,'index.html')
 
def signup(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('signup')
            else:   
                user = User.objects.create_user(username=username, password=password1, email=email,first_name=first_name,last_name=last_name)
                user.save()
                print('user created')
                return redirect('login')
        else:
            messages.info(request,'password not matching..')    
            return redirect('signup')     

    else:    
        return render(request,'signup.html')

def login(request):
    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')

    else:
        return render(request,'login.html')   


def logout(request):
    auth.logout(request)
    return redirect('login') 


def models(request):

    return render(request,'models.html')

def about(request):

    return render(request,'documentation.html')

def contact(request):
    if request.method == "POST":
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        text = request.POST.get('message')
        en = contactform(name=name,email=email,message=text)
        en.save()

    return render(request,'contact.html')             


