# views.py
import json

from django.views import View  
from ..models import Resep, MasterBahan, BarangJadi
from ..forms import BarangJadiForm, MasterBahanForm, ResepForm
# JsonResponse untuk merespons data dalam format JSON
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

