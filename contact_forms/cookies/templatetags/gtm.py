from . import register
from django.utils.safestring import mark_safe
from django.conf import settings
from django.template import loader


@register.inclusion_tag("banner.html")
def cookie_banner():
    return {}


def render_gtm_template(template_filename, gtm_container_id):
    t = loader.get_template(template_filename)

    return t.render({"GTM_CONTAINER_ID": gtm_container_id})


@register.simple_tag()
def google_tag_manager():
    if not settings.IEE_GA_GTM:
        return mark_safe("<!-- missing GTM container id -->")

    return render_gtm_template("gtm.html", settings.IEE_GA_GTM)


@register.simple_tag()
def google_tag_manager_noscript():
    if not settings.IEE_GA_GTM:
        return mark_safe("<!-- missing GTM container id -->")

    return render_gtm_template("gtm_noscript.html", settings.IEE_GA_GTM)
