"""bookstore URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin
from mainsite import views
from bookstore import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^index/', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^bookinfo/(\d+)/$', views.bookinfo, name='bookinfo'),
    url(r'^cart/$', views.cart, name='cart-url'),
    url(r'^additem/(\d+)/(\d+)/(.+)/$', views.add_to_cart, name='additem-url'),
    # url(r'^removeitem/(\d+)/$', views.remove_from_cart, name='removeitem-url'),

    url(r'^order/$', views.order, name='order')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)