from django.contrib import admin
from django.urls import path, include
from tables import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tables.urls'))

]
