from django.conf import settings


def ga_gtm_processor(request):
    return {"IEE_GA_GTM": settings.IEE_GA_GTM}
