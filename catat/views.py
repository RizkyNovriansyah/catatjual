from django.shortcuts import render
from django.contrib import messages
import json
from django.contrib.auth import (
	REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
	logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.views import LoginView as BaseLoginView
from django.shortcuts import redirect
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.views import View  
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from resep.models import BarangJadi, MasterBahan, Resep
from pesan.models import ListPesanan, Pesanan
from django.urls import reverse_lazy
from django.views import generic
from .forms import UserCreationForm
from catat.models import LoginSessionsTrack, User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission, User
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from datetime import timedelta

class LoginView(BaseLoginView):
	template_name = 'registration/login.html'
	form_class = AuthenticationForm

	def dispatch(self, request, *args, **kwargs):
		if request.method == 'GET':
			if request.user.is_authenticated:
				print('user is authenticated')
				return redirect('dashboard')
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		user = form.get_user()
		auth_login(self.request, user)
		self.update_login_time(user)
		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self, form):
		messages.error(self.request, 'Username atau password salah.')
		return self.render_to_response(self.get_context_data(form=form))

	def update_login_time(self, user):
		login_track, created = LoginSessionsTrack.objects.get_or_create(user=user)
		login_track.daily_login = timezone.now()
		login_track.save()

	def get_login_info(self, user):
		login_track = LoginSessionsTrack.objects.filter(user=user).first()
		if login_track:
			login_time = timezone.now() - login_track.daily_login
			return int(login_time.total_seconds() / 60)  # Menghitung menit
		return 0

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context[REDIRECT_FIELD_NAME] = self.request.GET.get(REDIRECT_FIELD_NAME, '')
		if self.request.user.is_authenticated:
			login_info = self.get_login_info(self.request.user)
			context['login_info'] = login_info
		return context

class SignUpView(generic.CreateView):
	form_class = UserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'registration/signup.html'
	
	def dispatch(self, request, *args, **kwargs):
		if self.request.method == 'GET':
			if self.request.user.is_authenticated:
				return redirect('dashboard')
		return super().dispatch(request, *args, **kwargs)
	
	def form_valid(self, form):
		password1 = form.cleaned_data.get('password1')
		password2 = form.cleaned_data.get('password2')
		
		# Check if passwords match
		if password1 != password2:
			form.add_error('password2', 'Password konfirmasi tidak sesuai.')
			return self.form_invalid(form)

		# Check if password length is 6 digits
		if len(password1) != 6:
			form.add_error('password1', 'Pin harus terdiri dari 6 digit.')
			return self.form_invalid(form)
		
		return super().form_valid(form)

# @login_required(login_url='login')
def dashboard(request):
	barang_jadi_count = BarangJadi.objects.filter(is_deleted=False).count()
	resep_count = Resep.objects.filter(is_deleted=False).count()
	bahan_count = MasterBahan.objects.filter(is_deleted=False).count()
	list_pesanan_count = ListPesanan.objects.filter(is_deleted=False).count()
	
	username = 'Anonymous'
	login_info = 0  

	if request.user.is_authenticated:
		username = request.user.username
		login_track = LoginSessionsTrack.objects.filter(user=request.user).first()
		if login_track:
			login_time = timezone.now() - login_track.daily_login
			login_info = int(login_time.total_seconds() / 60)  # Menghitung menit
			print('login_info: ', login_info)
	
	context = { 'bahan_count': bahan_count,
				'resep_count': resep_count,
				'username': username,
				'login_info': login_info,  # Menambahkan login_info ke dalam konteks
				'list_pesanan_count': list_pesanan_count,
				'barang_jadi_count': barang_jadi_count}
	return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def profile(request):
	user = User.objects.get(username=request.user)
	
	
	context = {'user': user,
				'username' : user.username, 
				'is_staff' : user.is_staff, 
				'is_active' : user.is_active, 
				'date_joined' : user.date_joined, 
				'groups' : user.groups,
				'user_permissions': user.user_permissions,
				}
	return render(request, 'profile.html', context)