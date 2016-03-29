from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from papukaaniApp.models_LajiStore import *
from papukaaniApp.tests.page_models.page_models import NewsPage

class TestNewsFrontend(StaticLiveServerTestCase):
    def setUp(self):
        I2 = individual.create("test", "test")
        targets = []
        targets.append(I2.nickname)
        self.I = news.create("Title", "<p>content</p>", "sv", '2016-03-01T00:00:00+00:00', targets)
        self.page = NewsPage()
        self.page.navigate()

    def tearDown(self):
        self.I.delete()
        self.page.close()
        news.delete_all()

    def test_news_info_visible(self):
        self.assertEquals("Title", self.page.FIRST_NEWS_TITLE.text)
        self.assertEquals("Ruotsi", self.page.FIRST_NEWS_LANGUAGE.text)
        self.assertEquals("01.03.2016 00:00", self.page.FIRST_NEWS_PUBLISHDATE.text)
        self.assertEquals("test", self.page.FIRST_NEWS_TARGETS.text)

    def test_show_correct_message_after_create(self):
        self.page.delete_first_news()
        self.page.create_news("Title", "Content", "Ruotsi", "01.03.2016 00:00")
        self.assertEquals("Title", self.page.FIRST_NEWS_TITLE.text)
        self.assertEquals("Uutinen luotu onnistuneesti!", self.page.MESSAGE.text)

    def test_show_correct_message_after_delete(self):
        self.page.delete_first_news()
        self.assertEquals("Tiedot poistettu onnistuneesti!", self.page.MESSAGE.text)

    def test_show_correct_message_after_modify(self):
        self.page.modify_news("Title2", "Content2", "Suomi", "01.03.2015 00:00")
        self.assertEquals("Title2", self.page.FIRST_NEWS_TITLE.text)
        self.assertEquals("Tiedot tallennettu onnistuneesti!", self.page.MESSAGE.text)

    def test_show_correct_message_if_no_title_content_language(self):
        self.page.delete_first_news()
        self.page.create_news("", "", "", "")
        self.assertEquals("Otsikko puuttuu\nSisältö puuttuu\nKieli puuttuu", self.page.MODAL_MESSAGE.text)