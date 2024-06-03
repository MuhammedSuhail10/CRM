from django.urls import path
from.import views


urlpatterns = [
    path('',views.home,name='home'),
    path('home',views.home,name='home'),
    path('login',views.loginuser,name='user_login'),
    path('logout', views.logoutuser, name='userlogout'),
    path('lead', views.lead,name='lead'),
    path('status_<int:id>', views.status,name='status'),
    path('<int:id>', views.del_payment, name='del_payment'),
    path('follow-ups', views.followups, name='followups)'),
    path('total_follow', views.totalfollow, name='totalfollow)'),
    path('won', views.leads_won, name='leads_won)'),
    path('callbacks', views.callbacks, name='callbacks)'),
    path('syllabus', views.syllabus, name='syllabus)'),
]
