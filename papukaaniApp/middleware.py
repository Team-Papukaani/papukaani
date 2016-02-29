from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils import translation
import logging
from django.utils import timezone


class SessionBasedLocaleMiddleware(object):
    """
    This Middleware saves the desired content language in the user session.
    The SessionMiddleware has to be activated.
    """

    def process_request(self, request):
        if not (request.method == 'GET' and 'lang' in request.GET):
            return
        lang_code = request.GET['lang']
        if not translation.check_for_language(lang_code):
            return
        request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
        translation.activate(lang_code)

    def process_response(self, request, response):
        patch_vary_headers(response, ('Accept-Language', ))
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response


request_logger = logging.getLogger('papukaaniApp.requests')
request_logger.setLevel('DEBUG')


class RequestLoggingMiddleware(object):
    def process_request(self, request):
        request_logger.info('[%s] %s %s' %
                            (timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                             request.method, request.get_full_path()))

    def process_response(self, request, response):
        request_logger.info('[response to %s %s = %s]' %
                            (request.method, request.get_full_path(),
                             str(response.status_code)))
        return response
