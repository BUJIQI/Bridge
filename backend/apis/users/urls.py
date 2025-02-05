from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('look1/', views.look_marketsituation, name='look1'),
    path('lookhistory/', views.lookhistory, name='lookhistory'),
    path('commit_decision/', views.commit_decision, name='commit_decision'),
    path('historical_decision/', views.historical_decision, name='historical_decision'),
    path('compete_outcome/', views.compete_outcome_fun, name='compete_outcome'),
    path('enterreporting/', views.enterreporting, name='enterreporting'),
    path('summart_evaluation/', views.get_summart_evaluation, name='summart_evaluation'),
    path('new_rounds/', views.new_rounds, name='new_rounds'),
    path('user_data/', views.user_data, name='user_data'),
    path('loginout/', views.user_logout, name='user_logout'),
    path('import_imformation/', views.import_imformation, name='import_imformation'),
    path('decision_terms_introduction/', views.decision_terms_introduction, name='decision_terms_introduction'),
    path('round_hisdistail/',views.round_hisdistail,name='round_hisdistail'),
    path('AIaided_decision_making/',views.AIaided_decision_making,name='AIaided_decision_making'),
]
