"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import blog.views

urlpatterns = [
                  path('',
                       blog.views.home,
                       name='home'),
                  path('blog/',
                       include('blog.urls')),
                  path('accounts/',
                       include('allauth.urls')),
                  path('admin/',
                       admin.site.urls),
                  path('api/',
                       blog.views.post_api_view,
                       name='blog_api_view'),
                  path('api/<int:pk>',
                       blog.views.post_api_detail_view,
                       name='blog_api_detail_view'),
                  path('api/auth/',
                       include('rest_auth.urls')),
                  path('api/auth/registration/',
                       include('rest_auth.registration.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Problem with rest_auth. Don't support django 4.0+
# *For django.conf.urls use
# from django.urls import re_path as url

# *For ugettext use
# from django.utils.translation import gettext_lazy as _

# *for force_text use
# from django.utils.encoding import force_str as force_text
