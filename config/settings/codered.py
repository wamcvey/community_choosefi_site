"""Routines to update the config of a cookiecutter-django site for codered
"""

def update_installed_apps(apps):
    needed_apps = [
       # This project
        'website',
        # CodeRed CMS
        'coderedcms',
        'bootstrap4',
        'modelcluster',
        'taggit',
        'wagtailfontawesome',
        'wagtailcache',
        'wagtailimportexport',
        # Wagtail
        'wagtail.contrib.forms',
        'wagtail.contrib.redirects',
        'wagtail.embeds',
        'wagtail.sites',
        'wagtail.users',
        'wagtail.snippets',
        'wagtail.documents',
        'wagtail.images',
        'wagtail.search',
        'wagtail.core',
        'wagtail.contrib.settings',
        'wagtail.contrib.modeladmin',
        'wagtail.contrib.table_block',
        'wagtail.admin',
        # Django
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sitemaps',
    ]
    new_list = []
    for pkg in needed_apps:
        if pkg not in apps:
            new_list.append(pkg)
    new_list.extend(apps)
    return new_list



def update_templates(TEMPLATES, DEBUG):
    TEMPLATES[0]["OPTIONS"]['context_processors'].append("wagtail.contrib.settings.context_processors.settings")
    return TEMPLATES


def update_middleware(middleware):
    middleware_setting = middleware[:]
    update_cache = 'wagtailcache.cache.UpdateCacheMiddleware'
    if update_cache not in middleware:
        middleware_setting.insert(0, update_cache)
    middleware_setting.extend([
        'wagtail.core.middleware.SiteMiddleware',
        'wagtail.contrib.redirects.middleware.RedirectMiddleware',
        # Fetch from cache. Must be LAST.
        'wagtailcache.cache.FetchFromCacheMiddleware',
    ])
    return middleware_setting

