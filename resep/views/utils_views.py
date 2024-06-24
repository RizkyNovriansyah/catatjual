# views.py
import json

from django.db.models.query import QuerySet
from django.views import View  
from ..models import ResepBahanJadi, MasterBahan, BarangJadi
from ..forms import BarangJadiForm, MasterBahanForm, ResepForm
# JsonResponse untuk merespons data dalam format JSON
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import TemplateView

class ErrorPageView(TemplateView):
    template_name = 'error_page.html'  # Ganti 'error_page.html' dengan nama template halaman error Anda