from django.core.management.base import BaseCommand

from django.conf import settings
from django.urls import URLPattern, URLResolver

urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])


def list_urls(lis, acc=None):
    if acc is None:
        acc = []
    if not lis:
        return
    l = lis[0]
    if isinstance(l, URLPattern):
        yield acc + [str(l.pattern)]
    elif isinstance(l, URLResolver):
        yield from list_urls(l.url_patterns, acc + [str(l.pattern)])
    yield from list_urls(lis[1:], acc)


class Command(BaseCommand):
    """
    solution source:
    https://stackoverflow.com/a/54531546/2975936
    """
    help = 'show all urls'

    def handle(self, *args, **options):
        for p in list_urls(urlconf.urlpatterns):
            url = ''.join(p)
            if url.startswith('admin'):
                continue
            elif url.startswith('__debug__'):
                continue

            self.stdout.write(url)
