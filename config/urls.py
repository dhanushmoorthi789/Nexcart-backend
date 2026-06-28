from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as static_serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
]

# static() only registers routes when DEBUG=True, so on Render (DEBUG=False)
# the /media/ and /static/ URLs were never being added -> 404 on every image.
# We add explicit fallback routes so media/static files are served even in
# production. WhiteNoise already serves /static/, but /media/ needs this.
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', static_serve, {'document_root': settings.MEDIA_ROOT}),
]
