from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from wagtail.documents import urls as wagtaildocs_urls
from coderedcms import admin_urls as coderedadmin_urls
from coderedcms import search_urls as coderedsearch_urls
from coderedcms import urls as codered_urls
from choosefi_vault_ui import urls as vault_urls

urlpatterns = [
    # User management
    path("users/", include("community_choosefi_site.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),

     # Django Admin, use {% url 'admin:index' %}
     path(settings.ADMIN_URL, admin.site.urls),
     path(r'admin/', include(coderedadmin_urls)),

     path('docs/', include(wagtaildocs_urls)),
     path('search/', include(coderedsearch_urls)),

     # Your stuff: custom urls includes go here
     path('vault/', include(vault_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

urlpatterns += [
    path(r'', include(codered_urls)),
    re_path(r'', include(codered_urls)),
]
