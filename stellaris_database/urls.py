from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('', views.home, name="home"),
    path('accounts/', include('allauth.urls')),
]

# To display images
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

