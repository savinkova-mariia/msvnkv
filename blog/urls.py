import blog.converters
import blog.views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, register_converter


register_converter(blog.converters.BlogOrWorksConverter, 'blog_or_works')


urlpatterns = [
    path('admin/', admin.site.urls),

    # ex: /blog/ or /works/
    path(
        '<blog_or_works:page_type>/',
        blog.views.post_list,
        name='post_list'
    ),
    path(
        '<blog_or_works:page_type>/tag/<tag_slug>/',
        blog.views.post_list,
        name='post_list_with_tag'
    ),

    # ex: /blog/<slug>/ or /works/<slug>/
    path(
        '<blog_or_works:page_type>/<slug>/',
        blog.views.post,
        name='post'
    ),

    path('martor/', include('martor.urls')),
    path('about/', blog.views.about, name='about'),
    path('robots.txt', blog.views.robots_txt, name='robots_txt'),
    path('sitemap.xml', blog.views.sitemap_xml, name='sitemap_xml'),
    path('', blog.views.homepage, name='homepage'),

]


if settings and settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
