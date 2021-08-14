from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse
from api.internal.app import ninja_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('metrics', lambda request: HttpResponse('')),
    path('app/', ninja_api.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler500 = 'api.utils.errors.handler500'
handler400 = 'api.utils.errors.handler400'
handler404 = 'api.utils.errors.handler404'
handler403 = 'api.utils.errors.handler403'
