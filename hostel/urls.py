from django.urls import path,NoReverseMatch
from . import views

app_name = 'hostel'

urlpatterns=[

    path('', views.homepage, name="home"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('facility/', views.facility, name="facility"),
    path('leave/', views.leave, name="leave"),
    path('complaint/', views.complaint, name="complaint"),
    path('approveleave/', views.ApproveLeave, name="approveleave"),
    path('leavedetails/', views.leavedetails, name="leavedetails"),
]
