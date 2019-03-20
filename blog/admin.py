from blog.models import (
    AboutPage, Config, Homepage, Post, PostTags, Project, ProjectTags, Tag,
)
from django.contrib import admin
from django.contrib.sites.models import Site
from django.db import models
from martor.widgets import AdminMartorWidget
from preferences.admin import PreferencesAdmin


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', )
    prepopulated_fields = {'slug': ('name', )}

    fields = ('name', 'slug', )


class PostTagsInline(admin.TabularInline):
    model = PostTags
    extra = 1
    fk_name = 'post'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'heading',
        'is_published',
        'publication_date',
        'updated_at',
    )
    list_filter = ('is_published', )
    search_fields = ('heading', 'content')
    prepopulated_fields = {'slug': ('heading', )}
    readonly_fields = ('updated_at', )
    inlines = (PostTagsInline, )

    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

    fieldsets = (
        (None, {
            'fields': (
                'heading', 'slug', 'is_published',
                'content', 'publication_date',
                'updated_at',
            )
        }),
        ('Метатеги', {
            'classes': ('collapse', ),
            'fields': ('title', 'keywords', 'description', ),
        }),
    )


class ProjectTagsInline(admin.TabularInline):
    model = ProjectTags
    extra = 1
    fk_name = 'project'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'heading',
        'sub_heading',
        'is_published',
        'publication_date',
        'updated_at',
    )
    list_filter = ('is_published', )
    search_fields = ('heading', 'content')
    prepopulated_fields = {'slug': ('heading', )}
    readonly_fields = ('updated_at', )
    inlines = (ProjectTagsInline, )

    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

    fieldsets = (
        (None, {
            'fields': (
                'heading', 'sub_heading', 'slug', 'is_published',
                'content', 'image_preview', 'publication_date',
                'updated_at',
            )
        }),
        ('Метатеги', {
            'classes': ('collapse', ),
            'fields': ('title', 'keywords', 'description', ),
        }),
    )


@admin.register(Config)
class PreferencesCustomAdmin(PreferencesAdmin):
    exclude = ('sites', )

    fieldsets = (
        (None, {
            'fields': (
                'robots_txt', 'head_injection', 'body_injection',
            )
        }),

        ('Метатеги главной страницы', {
            'classes': ('collapse', ),
            'fields': (
                'homepage_title_pattern',
                'homepage_keywords_pattern',
                'homepage_description_pattern',
            ),
        }),

        ('Шаблоны метатегов текстовых страниц (например, About)', {
            'classes': ('collapse', ),
            'fields': (
                'flatpage_title_pattern',
                'flatpage_keywords_pattern',
                'flatpage_description_pattern',
            ),
        }),

        ('Метатеги списка записей блога', {
            'classes': ('collapse', ),
            'fields': (
                'blog_title_pattern',
                'blog_keywords_pattern',
                'blog_description_pattern',
            ),
        }),

        ('Метатеги записи блога', {
            'classes': ('collapse', ),
            'fields': (
                'post_title_pattern',
                'post_keywords_pattern',
                'post_description_pattern',
            ),
        }),

        ('Метатеги списка проектов', {
            'classes': ('collapse', ),
            'fields': (
                'works_title_pattern',
                'works_keywords_pattern',
                'works_description_pattern',
            ),
        }),

        ('Метатеги страницы проекта', {
            'classes': ('collapse', ),
            'fields': (
                'project_title_pattern',
                'project_keywords_pattern',
                'project_description_pattern',
            ),
        }),
    )


@admin.register(AboutPage)
class AboutAdmin(PreferencesAdmin):
    exclude = ('sites', )
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

    fieldsets = (
        (None, {
            'fields': ('text', 'photo', )
        }),
        ('Метатеги', {
            'classes': ('collapse', ),
            'fields': ('title', 'keywords', 'description', ),
        }),
    )


@admin.register(Homepage)
class HomepageAdmin(PreferencesAdmin):
    exclude = ('sites', )
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

    fieldsets = (
        (None, {
            'fields': ('text', )
        }),
        ('Метатеги', {
            'classes': ('collapse', ),
            'fields': ('title', 'keywords', 'description', ),
        }),
    )


admin.site.unregister(Site)
