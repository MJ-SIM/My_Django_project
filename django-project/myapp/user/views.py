from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate,login, logout
# from .models import User
from .forms import RegisterForm, LoginForm

# Create your views here.
# user 관련 기능
# 회원가입
# 로그인
# 로그아웃

### Registration
class Registration(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        #회원가입 페이지
        # 정보를 입력할 폼을 보여줘야 한다.
        form = RegisterForm()
        context = {
            'form':form,
            'title':'User'
        }
        return render(request, 'user/user_register.html', context)
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 회원가입한 다음 바로 로그인 기능 안넣음(Login() 넣어주면됨)
            return redirect('user:login')
        

### Login
class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        form = LoginForm()
        context = {
            'form': form,
            'title': 'User'
        }
        return render(request, 'user/user_login.html', context)
    
    def post(self, request):
        form = LoginForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password) # 유저가 입력한 값 참, 거짓으로 리턴됨(정보 맞는지 아닌지)
            # 참이라면 로그인
            if user:
                login(request, user)
                # 다음화면으로 넘어가도록
                return redirect('blog:list')
            # 거짓이라면
        form.add_error(None, '아이디가 없습니다.')
        #거짓이면 에러있는 폼으로 보내줌
        context = {
            'form': form
        }

        return render(request, 'user/user_login.html', context)
    

### Logout
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('blog:list')