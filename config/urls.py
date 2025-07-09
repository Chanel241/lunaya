from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Inclure core.urls pour gérer home, login, signup, etc.
    path('cycle/', include('cycle.urls')),
    path('wellness/', include('wellness.urls')),
    path('meditations/', include('meditations.urls')),
    path('cercle/', include('cercle.urls')),
    path('horoscope/', include('horoscope.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)