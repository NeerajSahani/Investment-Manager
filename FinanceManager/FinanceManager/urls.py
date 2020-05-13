from django.contrib import admin
from django.views import generic
from django.urls import path, include
from django.conf.urls.static import settings, static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('analyzer.urls', namespace='analyzer')),
    path('', include('signup.urls', namespace='signup')),
    path('manager/', include('manager.urls', namespace='manager')),
    path('auth/', include('django.contrib.auth.urls')),
    path('test/', generic.TemplateView.as_view(template_name='analyzer/form.html')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
