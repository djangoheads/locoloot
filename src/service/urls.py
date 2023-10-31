from django.contrib import admin
from django.urls import path, include

from repo.views import i18next_http_interface


urlpatterns = [
    path("admin/", admin.site.urls),
    path("locales/<space>/<lang_code>/<namespace>.json", i18next_http_interface),
    path("__debug__/", include("debug_toolbar.urls")),
]
