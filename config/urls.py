from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dchat.views import home

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('auth/social/', include('googleauth.urls'), name='googleauth'),
    path('google-drive/', include('drive.urls')),
    path("dchat/", include("dchat.urls") ,name="dchat"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
