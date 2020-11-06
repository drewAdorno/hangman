from django.urls import path, include

urlpatterns = [
    path('', include('app1.urls')),
    path('user/', include('log_reg.urls')),
]