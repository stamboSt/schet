from django.urls import path
from . import views

app_name = 'schetovodstvo'

urlpatterns = [
path('', views.index, name='index'),
path('catalog.html', views.oborotna_vedomost, name='oborotna_vedomost'),
path('upload.html', views.upload_file_prodajbi, name='upload_file_prodajbi'),
path('upload_pok.html', views.upload_file_pokupki, name='upload_file_pokupki'),
path('display.html', views.function_display, name='function_display'),
path('upload_zaplati.html', views.upload_file_zaplati, name='upload_file_zaplati'),
path('upload_bank.html', views.upload_file_bank, name='upload_file_bank'),
]
