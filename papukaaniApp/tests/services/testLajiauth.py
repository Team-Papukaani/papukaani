from django.test import TestCase
from django.http.request import HttpRequest
from django.conf import settings

from papukaaniApp.services.laji_auth_service.laji_auth import*
from papukaaniApp.views.choose_views import *

class testLajiStoreAPI(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.session = {}
        settings.MOCK_AUTHENTICATION = "Off"

    def tearDown(self):
        settings.MOCK_AUTHENTICATION = "Skip"

    def testlog_in_returns_true_if_user_not_logged_in(self):
        self.assertTrue(log_in(self.request, "user"))

    def testlog_in_returns_false_if_user_is_logged_in(self):
        log_in(self.request, "user")

        self.assertFalse(log_in(self.request, "user"))

    def test_log_out_returns_true_if_user_is_logged_in(self):
        log_in(self.request, "user")
        self.assertTrue(log_out(self.request))

    def test_log_out_return_false_if_user_is_not_logged_in(self):
        self.assertFalse(log_out(self.request))

    def testlog_in_sets_user_id_in_session(self):
        log_in(self.request, "user")

        self.assertTrue("user_id" in self.request.session)

    def test_log_out_removes_user_id_from_sessions(self):
        log_in(self.request, "user")
        log_out(self.request)

        self.assertTrue("user_id" not in self.request.session)

    def test_authenticated_returns_true_if_logged_in(self):
        log_in(self.request, "user")

        self.assertTrue(authenticated(self.request))
        log_out(self.request)
        log_in(self.request, "user")
        self.assertTrue(authenticated(self.request))

    def test_authenticated_returns_false_if_not_logged_in(self):

        self.assertFalse(authenticated(self.request))

        log_in(self.request, "user")
        log_out(self.request)

        self.assertFalse(authenticated(self.request))

    def test_require_auth_returns_original_funtion_if_authenticated(self):
        log_in(self.request, "user")
        self.a = False

        @require_auth
        def f(request):
            self.a = True

        f(self.request)

        self.assertTrue(self.a)

    def test_require_auth_does_not_return_original_funtion_if_not_authenticated(self):
        self.a = False

        @require_auth
        def f(request):
            self.a = True

        f(self.request)
        self.assertFalse(self.a)
