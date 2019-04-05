import blog.utils
from django.db import models
from django.utils import timezone
from django.urls import reverse
from markdown import markdown
from preferences.models import Preferences
import random


class SlugMixin(models.Model):
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='Ключ ЧПУ'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.slug

    def set_slug(self, source):
        if not self.slug:
            slug = blog.utils.transliterate(source)
            is_unique = False

            while not is_unique:
                is_unique = self.__class__.objects.filter(
                    slug=slug).count() == 0

                if is_unique:
                    self.slug = slug
                else:
                    slug = blog.utils.transliterate(
                        '%s-%s' % (source, random.randint(1000, 9999))
                    )


class MetatagsMixin(models.Model):
    title = models.CharField(
        max_length=255,
        default='',
        blank=True,
        verbose_name='Title',
        help_text='''
            Подставляется в качестве переменной __V__ в общий шаблон
            метатега title для сайта. Если значение не задано, то
            в шаблон подставляется заголовок сущности (название, имя, и т.д.).
        '''
    )
    keywords = models.CharField(
        max_length=255,
        default='',
        blank=True,
        verbose_name='Keywords',
        help_text='''
            Подставляется в качестве переменной __V__ в общий шаблон
            метатега keywords для сайта. Если значение не задано, то
            в шаблон подставляется заголовок сущности (название, имя, и т.д.).
        '''
    )
    description = models.CharField(
        max_length=255,
        default='',
        blank=True,
        verbose_name='Description',
        help_text='''
            Подставляется в качестве переменной __V__ в общий шаблон
            метатега description для сайта. Если значение не задано, то
            в шаблон подставляется заголовок сущности (название, имя, и т.д.).
        '''
    )

    class Meta:
        abstract = True


class PostMixin(models.Model):
    is_published = models.BooleanField(
        blank=True,
        default=True,
        db_index=True,
        verbose_name='Опубликован',
        help_text='''
            Если флажок снят, то материал не будет присутствовать на сайте.
        '''
    )
    publication_date = models.DateField(
        blank=True,
        null=True,
        db_index=True,
        verbose_name='Дата публикации'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлено'
    )
    heading = models.CharField(max_length=512, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Основное содержимое')

    class Meta:
        abstract = True

    def __str__(self):
        return self.heading

    @property
    def html_content(self):
        return markdown(self.content or '')

    @property
    def last_modified(self):
        if not self.publication_date:
            return None

        return max(self.publication_date, self.updated_at.date())

    def save(self, *args, **kwargs):
        self.set_slug(source=self.heading)

        if self.is_published and not self.publication_date:
            self.publication_date = timezone.now().date()

        super(PostMixin, self).save(*args, **kwargs)


class Post(SlugMixin, MetatagsMixin, PostMixin):
    class Meta:
        verbose_name = 'Запись блога'
        verbose_name_plural = 'Записи блога'

    def get_absolute_url(self):
        return reverse('post', args=['blog', self.slug, ])


class Project(SlugMixin, MetatagsMixin, PostMixin):
    sub_heading = models.CharField(
        max_length=512,
        verbose_name='Подзаголовок'
    )
    image_preview = models.ImageField(
        upload_to=blog.utils.unique_upload_path,
        verbose_name='Изображение для списка',
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def get_absolute_url(self):
        return reverse('post', args=['works', self.slug, ])


class Tag(SlugMixin):
    name = models.CharField(
        max_length=512,
        verbose_name='Метка',
        help_text='Название тега'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name', ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/t/%s/' % self.slug

    def save(self, *args, **kwargs):
        self.set_slug(source=self.name)
        super(Tag, self).save(*args, **kwargs)


class PostTags(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='tags',
        verbose_name='Запись',
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Тег')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        unique_together = ('post', 'tag')

    def __str__(self):
        return '%s + %s' % (self.post.heading, self.tag.name)

    def get_absolute_url(self):
        return reverse('post_list_with_tag', args=['blog', self.tag.slug, ])


class ProjectTags(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tags',
        verbose_name='Проект',
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Тег')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        unique_together = ('project', 'tag')

    def __str__(self):
        return '%s + %s' % (self.project.heading, self.tag.name)

    def get_absolute_url(self):
        return reverse('post_list_with_tag', args=['works', self.tag.slug, ])


class Config(Preferences):
    homepage_title_pattern = models.CharField(
        max_length=512,
        blank=True,
        default='',
        verbose_name='Шаблон Title',
        help_text='''
            Определяет шаблон метатега title.
            Если в шаблоне присутствует переменная __V__, то
            в метатеге страницы сайта эта переменная будет
            замена значением соответствующего поля для текущей сущности.
        '''
    )
    homepage_keywords_pattern = models.CharField(
        max_length=512,
        blank=True,
        default='',
        verbose_name='Шаблон Keywords',
        help_text='''
            Определяет шаблон метатега keywords.
            Если в шаблоне присутствует переменная __V__, то
            в метатеге страницы сайта эта переменная будет
            замена значением соответствующего поля для текущей сущности.
        '''
    )
    homepage_description_pattern = models.CharField(
        max_length=512,
        blank=True,
        default='',
        verbose_name='Шаблон Description',
        help_text='''
            Определяет шаблон метатега description.
            Если в шаблоне присутствует переменная __V__, то
            в метатеге страницы сайта эта переменная будет
            замена значением соответствующего поля для текущей сущности.
        '''
    )

    flatpage_title_pattern = models.CharField(
        max_length=512,
        blank=True,
        default='',
        verbose_name='Шаблон Title',
        help_text='''
            Определяет шаблон метатега title.
            Если в шаблоне присутствует переменная __V__, то
            в метатеге страницы сайта эта переменная будет
            замена значением соответствующего поля для текущей сущности.
        '''
    )
    flatpage_keywords_pattern = models.CharField(
        max_length=512,
        blank=True,
        default='',
        verbose_name='Шаблон Keywords',
        help_text='''
            Определяет шаблон метатега keywords.
            Если в шаблоне присутствует переменная __V__, то
            в метатеге страницы сайта эта переменная будет
            замена значением соответствующего поля для текущей сущности.
        '''
    )
    flatpage_description_pattern = models.CharField(
        max_length=512,
        blank=True,
        default='',
        verbose_name='Шаблон Description',
        help_text='''
            Определяет шаблон метатега description.
            Если в шаблоне присутствует переменная __V__, то
            в метатеге страницы сайта эта переменная будет
            замена значением соответствующего поля для текущей сущности.
        '''
    )

    blog_title_pattern = models.CharField(
        max_length=512,
        blank=True,
        default='',
        verbose_name='Шаблон Title',
        help_text='''
            Определяет шаблон метатега title.
            Если в шаблоне присутствует переменная __V__, то
            в метатеге страницы сайта эта переменная будет
            замена значением соответствующего поля для текущей сущности.
        '''
    )
    blog_keywords_pattern = models.CharField(
        max_length=512,
        blank=True,
        default='',
        verbose_name='Шаблон Keywords',
        help_text='''
            Определяет шаблон метатега keywords.
            Если в шаблоне присутствует переменная __V__, то
            в метатеге страницы сайта эта переменная будет
            замена значением соответствующего поля для текущей сущности.
        '''
    )
    blog_description_pattern = models.CharField(
        max_length=512,
        blank=True,
        default='',
        verbose_name='Шаблон Description',
        help_text='''
            Определяет шаблон метатега description.
            Если в шаблоне присутствует переменная __V__, то
            в метатеге страницы сайта эта переменная будет
            замена значением соответствующего поля для текущей сущности.
        '''
    )

    works_title_pattern = models.CharField(
        max_length=512,
        blank=True,
        default='',
        verbose_name='Шаблон Title',
        help_text='''
            Определяет шаблон метатега title.
            Если в шаблоне присутствует переменная __V__, то
            в метатеге страницы сайта эта переменная будет
            замена значением соответствующего поля для текущей сущности.
        '''
    )
    works_keywords_pattern = models.CharField(
        max_length=512,
        blank=True,
        default='',
        verbose_name='Шаблон Keywords',
        help_text='''
            Определяет шаблон метатега keywords.
            Если в шаблоне присутствует переменная __V__, то
            в метатеге страницы сайта эта переменная будет
            замена значением соответствующего поля для текущей сущности.
        '''
    )
    works_description_pattern = models.CharField(
        max_length=512,
        blank=True,
        default='',
        verbose_name='Шаблон Description',
        help_text='''
            Определяет шаблон метатега description.
            Если в шаблоне присутствует переменная __V__, то
            в метатеге страницы сайта эта переменная будет
            замена значением соответствующего поля для текущей сущности.
        '''
    )

    post_title_pattern = models.CharField(
        max_length=512,
        blank=True,
        default='',
        verbose_name='Шаблон Title',
        help_text='''
            Определяет шаблон метатега title.
            Если в шаблоне присутствует переменная __V__, то
            в метатеге страницы сайта эта переменная будет
            замена значением соответствующего поля для текущей сущности.
        '''
    )
    post_keywords_pattern = models.CharField(
        max_length=512,
        blank=True,
        default='',
        verbose_name='Шаблон Keywords',
        help_text='''
            Определяет шаблон метатега keywords.
            Если в шаблоне присутствует переменная __V__, то
            в метатеге страницы сайта эта переменная будет
            замена значением соответствующего поля для текущей сущности.
        '''
    )
    post_description_pattern = models.CharField(
        max_length=512,
        blank=True,
        default='',
        verbose_name='Шаблон Description',
        help_text='''
            Определяет шаблон метатега description.
            Если в шаблоне присутствует переменная __V__, то
            в метатеге страницы сайта эта переменная будет
            замена значением соответствующего поля для текущей сущности.
        '''
    )

    project_title_pattern = models.CharField(
        max_length=512,
        blank=True,
        default='',
        verbose_name='Шаблон Title',
        help_text='''
            Определяет шаблон метатега title.
            Если в шаблоне присутствует переменная __V__, то
            в метатеге страницы сайта эта переменная будет
            замена значением соответствующего поля для текущей сущности.
        '''
    )
    project_keywords_pattern = models.CharField(
        max_length=512,
        blank=True,
        default='',
        verbose_name='Шаблон Keywords',
        help_text='''
            Определяет шаблон метатега keywords.
            Если в шаблоне присутствует переменная __V__, то
            в метатеге страницы сайта эта переменная будет
            замена значением соответствующего поля для текущей сущности.
        '''
    )
    project_description_pattern = models.CharField(
        max_length=512,
        blank=True,
        default='',
        verbose_name='Шаблон Description',
        help_text='''
            Определяет шаблон метатега description.
            Если в шаблоне присутствует переменная __V__, то
            в метатеге страницы сайта эта переменная будет
            замена значением соответствующего поля для текущей сущности.
        '''
    )

    robots_txt = models.TextField(
        blank=True,
        null=True,
        verbose_name='Содержимое файла robots.txt',
    )

    head_injection = models.TextField(
        blank=True,
        null=True,
        verbose_name='Вставка в конец секции HEAD',
        help_text='''
            Содержимое поля будет "как есть" добавлено в конец
            секции HEAD для любой html-страницы сайта.
        '''
    )

    body_injection = models.TextField(
        blank=True,
        null=True,
        verbose_name='Вставка в конец секции BODY',
        help_text='''
            Содержимое поля будет "как есть" добавлено в конец
            секции HEAD для любой html-страницы сайта.
        '''
    )

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'


class AboutPage(Preferences, MetatagsMixin):
    photo = models.ImageField(
        blank=True,
        null=True,
        upload_to=blog.utils.unique_upload_path,
        verbose_name='Фото в левой части страницы',
    )
    text = models.TextField(
        blank=True,
        null=True,
        verbose_name='Текстовое содержимое',
    )

    class Meta:
        verbose_name = 'Страница "About"'
        verbose_name_plural = 'Страница "About"'

    @property
    def html_content(self):
        return markdown(self.text or '')


class Homepage(Preferences, MetatagsMixin):
    text = models.TextField(
        blank=True,
        null=True,
        verbose_name='Текстовое содержимое',
    )

    class Meta:
        verbose_name = 'Главная страница'
        verbose_name_plural = 'Главная страница'

    @property
    def html_content(self):
        return markdown(self.text or '')
