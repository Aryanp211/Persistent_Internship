from django.urls import path
from . import views


app_name="app1"
urlpatterns=[
    path('home',views.home,name='home'),
    path('result',views.result,name='result'),
]