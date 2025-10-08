from django.shortcuts import render,redirect
from django.views import View
from Blog.forms import UserRegForm,LoginForm,CreateForm,UpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from Blog.models import Blog,Comment

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
            
class UpdateBlogView(View):
    def get(self,request,**kwargs):
        blog=Blog.objects.get(id=kwargs.get("id"))
        form=CreateForm(instance=blog)
        return render(request,"update_blog.html",{"form":form})
    def post(self,request,**kwargs):
        blog=Blog.objects.get(id=kwargs.get("id"))
        form_instance=CreateForm(request.POST,instance=blog)
        if form_instance.is_valid():
            form_instance.save()
            messages.success(request,"Blog Updated successfully")
            return redirect("writer")
        else:
            messages.error(request,"Somthing Wrong")
            return redirect("writer")


class UpdateProfileView(View):
    def get(self,request,**kwargs):
        user=User.objects.get(id=kwargs.get("id"))
        form=UpdateForm(instance=user)
        return render(request,"update_profile.html",{"form":form})
    def post(self,request,**kwargs):
        user=User.objects.get(id=kwargs.get("id"))
        form=UpdateForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            # User.objects.create_user(**form.cleaned_data)
            messages.success(request,"profile updated succesfully")
            return redirect("writer")
        else:
            messages.error(request,"somthing went wrong")
            return redirect("update_profile")
            

        

class ViewMoreView(View):
    def get(self,request,**kwargs):
        blog=Blog.objects.get(id=kwargs.get("id"))
        comment=Comment.objects.filter(blog=kwargs.get("id"))
        
        return render(request,"blog-details.html",{"blog":blog,"comment":comment})
    def post(self,request,**kwargs):
        user=request.user
        blog=Blog.objects.get(id=kwargs.get("id"))
        comment=request.POST.get("comment")
        Comment.objects.create(comment=comment,user=user,blog=blog)
        messages.success(request,"comment added")
        return redirect("viewblog",id=blog.id)



class LogoutView(View):
    def get(self,request):
        logout(request)
        messages.warning(request,"Logout")
        return redirect("login")