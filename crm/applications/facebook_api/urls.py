from django.contrib import admin
from django.urls import path

from applications.facebook_api.views import *

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('base', BaseView.as_view(), name='base'),

    # NOTE: Sessions
    path('login', auth_views.LoginView.as_view(
                    template_name='facebook_api/login.html', 
                    redirect_authenticated_user=True, 
                    redirect_field_name='index'
                    ), name='login'),

    path('logout', auth_views.LogoutView.as_view(
                    next_page='/facebook/',  
                    redirect_field_name='index'), name='logout'),
         
    path('signup', register, name = 'register'),

    # NOTE: Site pages
    path('', IndexView.as_view(), name='index'),  # Index view
    
    path('dashboard', login_required(DashboardView.as_view()), name='index'),  # Index view

    
]