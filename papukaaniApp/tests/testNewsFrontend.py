from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from papukaaniApp.models_LajiStore import *
from papukaaniApp.tests.page_models.page_models import NewsPage

class TestIndividualFrontend(StaticLiveServerTestCase):
    def setUp(self):
        self.I = news.create("Title", "<p>content</p>", "sv")
        self.page = NewsPage()
        self.page.navigate()

    def tearDown(self):
        self.I.delete()
        self.page.close()
        news.delete_all()

    def test_news_info_visible(self):
        self.assertEquals("Title", self.page.FIRST_NEWS_TITLE)