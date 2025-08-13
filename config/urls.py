from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('cycle/', include('cycle.urls')),
    path('wellness/', include('wellness.urls')),
    path('meditations/', include('meditations.urls')),
    path('cercle/', include('cercle.urls')),
    path('horoscope/', include('horoscope.urls')),
    # URL personnalisée pour la connexion
    path('accounts/login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),  # Inclut les autres URLs d'auth
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)