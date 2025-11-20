from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('bill.urls')),
    path('api/', include('cashRegister.urls')),
    # path('api/', include('inventory.urls')),
    path('api/', include('menu.urls')),
    path('api/', include('tables.urls')),
    path('api/', include('users.urls')),
    

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
