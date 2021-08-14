from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('admin/', include('api.admin_api.urls')),
    path('employee/', include('api.employee_api.urls')),

]
