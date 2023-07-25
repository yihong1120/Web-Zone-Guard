"""
URL configuration for WebZoneGuard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts import views as accounts_views
from VisionSnap import views as VisionSnap_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', VisionSnap_views.index, name='index'),
    path('signup/', accounts_views.signup_view, name='signup'),
    path('login/', accounts_views.login_view, name='login'),
    path('controls/', VisionSnap_views.controls, name='controls'),
    path('records/', VisionSnap_views.records, name='records'),
    path('logout/', VisionSnap_views.logout, name='logout'),
]