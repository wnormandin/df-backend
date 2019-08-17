"""df_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include, path

from .api import views
from .api.urls import urlpatterns as api_urls
from .ui.urls import urlpatterns as ui_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', views.UserLogin.as_view()),
    path('api/', include(api_urls)),
    path('ui/', include(ui_urls))
]
