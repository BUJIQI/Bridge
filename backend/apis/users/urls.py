from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('look1/', views.look1, name='look1'),
    path('lookhistory/', views.lookhistory, name='lookhistory'),
]
