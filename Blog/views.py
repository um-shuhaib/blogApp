from django.shortcuts import render,redirect
from django.views import View
from Blog.forms import UserRegForm,LoginForm,CreateForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from Blog.models import Blog

# Create your views here.
class UserRegView(View):
    def get(self,request):
        form=UserRegForm()
        return render(request,"userreg.html",{"form":form})
    def post(self,request):
        blog=UserRegForm(request.POST)
        if blog.is_valid():            
            User.objects.create_user(**blog.cleaned_data)
            messages.success(request,"Registration Succeful")
            return redirect("login")
        else:
            messages.error(request,"user already exist")
            return redirect("register")

        
class HomeView(View):
    def get(self,request):
        user=User.objects.all()
        return render(request,"index.html",{"user":user})
    

class LoginView(View):
    def get(self,request):
        form=LoginForm()
        return render(request,'login.html',{'form':form})
    
    def post(self,request):
        username=request.POST.get("username")
        password=request.POST.get("password")
        usertype=request.POST.get("usertype")
        res=authenticate(request,username=username,password=password)
        if res:
            login(request,res)
            messages.success(request,"login success")
            if usertype=="reader":
                return redirect("reader")
            else:
                return redirect("writer")

        else:
            messages.error(request,"invalid Credential")
            return redirect("login")
        
class Writerhome(View):
    def get(self,request):
        user=request.user
        blog=Blog.objects.filter(user_id=request.user)
        return render(request,"writer_home.html",{"blog":blog,"user":user})
class ReaderHome(View):
    def get(self,request):
        blog=Blog.objects.all()
        
        return render(request,"reader_home.html",{"blog":blog})
    

class CreateView(View):
    def get(self,request):
        form=CreateForm()
        return render(request,"create_blog.html",{"form":form})
    
    def post(self,request):
        blog=CreateForm(request.POST,request.FILES)
        if blog.is_valid():
            Blog.objects.create(**blog.cleaned_data,user_id=request.user)
            messages.success(request,"blog added")
            return redirect("writer")
        
class DeleteView(View):
    def get(self,request,**kwargs):
        blog=Blog.objects.get(id=kwargs.get("id"))
        blog.delete()
        messages.warning(request,"blog deleted")
        return redirect("writer")
            
