from django.contrib import admin
from django.urls import path, include
from home import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('extensions/', views.extensions_list, name='extensions_list'),
    
    # Extension pages
    path('extension/<slug:slug>/', views.extension_detail, name='extension_detail'),
    path('extension/<slug:slug>/privacy-policy/', views.extension_privacy_policy, name='extension_privacy_policy'),
    path('extension/<slug:slug>/terms-of-service/', views.extension_terms_of_service, name='extension_terms_of_service'),
    
    # Static pages
    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('support/', views.support, name='support'),
]
