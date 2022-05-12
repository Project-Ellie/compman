from django.contrib import admin
from django.urls import path, include  # new
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

APPS = [
    'compman',
]


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("compman.urls")),  # new
]


path('admin/', admin.site.urls),
path("api/", include([
                         path('schema/', SpectacularAPIView.as_view(), name='schema'),
                         path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='Adtrac Brokerage API'),
                     ] + [
                         path('%s/' % app, include('%s.urls' % app)) for app in APPS
                     ]))
