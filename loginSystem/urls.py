from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import os
from loginSystem.settings import BASE_DIR

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(BASE_DIR, 'static'))