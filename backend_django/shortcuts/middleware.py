# shortcuts/middleware.py

from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class AppendSlashMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not settings.APPEND_SLASH:
            return

        if request.method == 'POST' and not request.path.endswith('/'):
            full_path = request.get_full_path(force_append_slash=True)
            return HttpResponsePermanentRedirect(full_path)
