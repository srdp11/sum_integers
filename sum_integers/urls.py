"""sum_integers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from sum_ints_app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.render_main),
    url(r'^save_data/', views.save_data),
    url(r'^run_calculation/', views.run_calculation),
    url(r'^last_status/', views.last_status),
    url(r'^last_result/', views.last_results),
]
