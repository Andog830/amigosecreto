"""
URL configuration for amigosecreto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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

from participantes.views import cerrar_sesion, generar_clave, login_participante, pagina_principal

urlpatterns = [
    path('', login_participante, name='login'),
    path('generar-clave/', generar_clave, name='generar_clave'),
    path('pagina-principal/', pagina_principal, name='pagina_principal'),
    path('salir/', cerrar_sesion, name='cerrar_sesion'),
    path('admin/', admin.site.urls),
]
