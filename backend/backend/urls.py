from django.contrib import admin
from django.urls import path, include
from tables import urls
from menu import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tables.urls')),
    path('', include('menu.urls'))

]
