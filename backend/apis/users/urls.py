from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('look1/', views.look1, name='look1'),
    path('lookhistory/', views.lookhistory, name='lookhistory'),
    path('commit_decision/', views.commit_decision, name='commit_decision'),
    path('historical_decision/', views.historical_decision, name='historical_decision'),
    path('compete_outcome/', views.compete_outcome_fun, name='compete_outcome'),
    path('enterreporting/', views.enterreporting, name='enterreporting'),
    path('summart_evaluation/', views.get_summart_evaluation, name='summart_evaluation'),
    path('new_rounds/', views.new_rounds, name='new_rounds'),
]
