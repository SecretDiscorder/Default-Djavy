"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from . import views
from .views import StaticFilesView
urlpatterns = [    
	path('static/<path:filename>', StaticFilesView.as_view(), name='static-files'),
        path('', views.index, name="JAYA E-TOOLS"),
	path('kalkulator/', views.kalkulator, name='kalkulator'),
	path('morse/', views.morse, name="morse"),
	path('blang/', views.blang, name="blang"),
        path('aksara_converter/', views.aksara_converter, name='aksara_converter'),
        path('aksara_converter/aksara_converter_image/', views.convert_image, name='convert_image'),
]
