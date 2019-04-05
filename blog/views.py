from blog.models import Post, Project, Tag
from blog.utils import to_int
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from preferences import preferences


def set_metatag_data(request, whois, instance=None, if_blank_then_field=''):
    default = None
    if if_blank_then_field:
        default = getattr(instance, if_blank_then_field)

    title = instance.title if instance else ''
    keywords = instance.keywords if instance else ''
    description = instance.description if instance else ''

    request.metatag_data = {
        'whois': whois,
        'title': title or default or '',
        'keywords': keywords or default or '',
        'description': description or default or '',
    }


def homepage(request):
    homepage = preferences.Homepage
    set_metatag_data(request, 'homepage', homepage)
    return TemplateResponse(request, 'homepage.html', {
        'latest_post': Post.objects.filter(is_published=True).last(),
        'page_type': 'homepage',
        'homepage': homepage,
    })


def about(request):
    about_page = preferences.AboutPage
    set_metatag_data(request, 'flatpage', about_page)
    return TemplateResponse(request, 'about.html', {
        'about_page': about_page,
        'page_type': 'about',
    })


def post(request, slug, page_type):
    model = page_type == 'blog' and Post or Project
    post = model.objects.filter(slug=slug, is_published=True).first()

    if not post:
        raise Http404

    seo_whois = 'post' if page_type == 'blog' else 'project'
    set_metatag_data(request, seo_whois, post, 'heading')

    return TemplateResponse(request, 'post.html', {
        'post': post,
        'page_type': page_type,
        'next_post': model.objects.filter(
            pk__gt=post.pk, is_published=True).first(),
        'prev_post': model.objects.filter(
            pk__lt=post.pk, is_published=True).last(),
    })


def post_list(request, page_type, tag_slug=None):
    model = page_type == 'blog' and Post or Project
    items = model.objects.filter(is_published=True)

    tag = None
    if tag_slug:
        tag = Tag.objects.filter(slug=tag_slug).first()
        if not tag:
            raise Http404

        items = items.filter(tags__tag=tag)

    if not items:
        raise Http404

    paginator = Paginator(items, settings.PAGINATION_PAGE_SIZE)
    page = to_int(request.GET.get('page'), 1)
    page = min(max(page, 1), paginator.count)

    items = paginator.get_page(page)

    template = '%s.html' % page_type
    set_metatag_data(request, page_type)

    return TemplateResponse(request, template, {
        'items': items,
        'page_type': page_type,
        'tag': tag,
        'paginator': paginator,
        'current_page': page,
    })


def robots_txt(request):
    return HttpResponse(
        '%s\n' % (preferences.Config.robots_txt or ''),
        content_type='text/plain'
    )


def sitemap_xml(request):
    entries = list(Post.objects.filter(is_published=True))
    entries += list(Project.objects.filter(is_published=True))

    content = render_to_string('sitemap.xml', {
        'entries': entries,
    })
    return HttpResponse(content, content_type='application/xml')
