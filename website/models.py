"""
Createable pages used in CodeRed CMS.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


import wagtail.images
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from modelcluster.fields import ParentalKey
from coderedcms.forms import CoderedFormField
from coderedcms.models import (
    CoderedArticlePage,
    CoderedArticleIndexPage,
    CoderedEmail,
    CoderedFormPage,
    CoderedWebPage
)


class ArticlePage(CoderedArticlePage):
    """
    Article, suitable for news or blog content.
    """
    class Meta:
        verbose_name = 'Article'
        ordering = ['-first_published_at', ]

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ['website.ArticleIndexPage']

    template = 'coderedcms/pages/article_page.html'
    amp_template = 'coderedcms/pages/article_page.amp.html'
    search_template = 'coderedcms/pages/article_page.search.html'


class ArticleIndexPage(CoderedArticleIndexPage):
    """
    Shows a list of article sub-pages.
    """
    class Meta:
        verbose_name = 'Article Landing Page'

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'website.ArticlePage'

    # Only allow ArticlePages beneath this page.
    subpage_types = ['website.ArticlePage']

    template = 'coderedcms/pages/article_index_page.html'


class FormPage(CoderedFormPage):
    """
    A page with an html <form>.
    """
    class Meta:
        verbose_name = 'Form'

    template = 'coderedcms/pages/form_page.html'


class FormPageField(CoderedFormField):
    """
    A field that links to a FormPage.
    """
    class Meta:
        ordering = ['sort_order']

    page = ParentalKey('FormPage', related_name='form_fields')


class FormConfirmEmail(CoderedEmail):
    """
    Sends a confirmation email after submitting a FormPage.
    """
    page = ParentalKey('FormPage', related_name='confirmation_emails')


class WebPage(CoderedWebPage):
    """
    General use page with featureful streamfield and SEO attributes.
    Template renders all Navbar and Footer snippets in existance.
    """

    # cover_image = models.ForeignKey(
    #     wagtail.images.get_image_model_string(),
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name='+',
    #     verbose_name=_('Cover image'),
    # )

    class Meta:
        verbose_name = 'Web Page'

    template = 'coderedcms/pages/web_page.html'


class ProvenancedImage(AbstractImage):
    """An extended Image class that tracks the provenance of the image
    """
    image_attribution = models.CharField(
        max_length=1024, blank=True,
        help_text="Who is the source of the image")
    image_attribution_url = models.URLField(
        max_length=1024, blank=True,
        help_text="URL to the origination of the image" )
    show_attribution = models.BooleanField(
        default=False,
        help_text="Source of the image requests the display of the attribution")
    license_notes = models.TextField(blank=True,
        help_text="Any extra info on image license (not to be displayed)")

    admin_form_fields = Image.admin_form_fields + (
        'image_attribution',
        'image_attribution_url',
        'show_attribution',
        'license_notes',
    )

class ProvenancedImageRendition(AbstractRendition):
    image = models.ForeignKey(ProvenancedImage,
                              on_delete=models.CASCADE,
                              related_name='renditions')

    class Meta:
        unique_together = ('image', 'filter_spec', 'focal_point_key')

