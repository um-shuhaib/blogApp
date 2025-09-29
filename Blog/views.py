from django.shortcuts import render,redirect
from django.views import View
from Blog.forms import UserRegForm
from django.contrib import messages

# Create your views here.
class UserRegView(View):
    def get(self,request):
        form=UserRegForm()
        return render(request,"userreg.html",{"form":form})
    def post(self,request):
        blog=UserRegForm(request.POST)
        if blog.is_valid():
            blog.save()
            messages.success(request,"Registration Succeful")
            return redirect("home")
        
class HomeView(View):
    def get(self,request):
        return render(request,"home.html")
