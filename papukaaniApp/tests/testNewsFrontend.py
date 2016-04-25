from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from papukaaniApp.models_LajiStore import *
from papukaaniApp.tests.page_models.page_models import NewsPage

class TestNewsFrontend(StaticLiveServerTestCase):
    def setUp(self):
        self.I2 = individual.create("test", "ERIEUR")
        self.I3 = individual.create("test2", "ERIEUR")
        self.targets = []
        self.targets.append(self.I2.id)
        self.I = news.create("Title", "<p>content</p>", "sv", '2016-03-01T00:00:00+00:00', '2016-03-01T00:00:00+00:00', self.targets)
        self.page = NewsPage()
        self.page.navigate()

    def tearDown(self):
        self.I.delete()
        self.I2.delete()
        self.I3.delete()
        self.page.close()
        news.delete_all()

    def test_news_info_visible(self):
        self.assertEquals("Title", self.page.FIRST_NEWS_TITLE.text)
        self.assertEquals("Ruotsi", self.page.FIRST_NEWS_LANGUAGE.text)
        self.assertEquals("01.03.2016 00:00", self.page.FIRST_NEWS_PUBLISHDATE.text)
        self.assertEquals("test (Siili)", self.page.FIRST_NEWS_TARGETS.text)

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

    def test_add_targets(self):
        self.page.add_targets(str(self.I3.id))
        self.assertEquals("test2 (Siili)", self.page.FIRST_NEWS_TARGETS.text)

    def test_close_without_saving_confirmed(self):
        self.page.create_news_and_close_without_saving_accept("Title", "Content", "Ruotsi", "01.03.2016 00:00")
        self.assertEquals("display: none;", self.page.NEWS_MODAL.get_attribute("style"))

    def test_close_without_saving_not_confirmed(self):
        self.page.create_news_and_close_without_saving_dismiss("Title", "Content", "Ruotsi", "01.03.2016 00:00")
        self.assertEquals("display: block;", self.page.NEWS_MODAL.get_attribute("style"))

    def test_show_confirm_dialog_with_change(self):
        self.page.create_news_with_inputs("Title", "Content", "Ruotsi", "01.03.2016 00:00")
        self.page.is_alert_present()
        self.assertTrue(self.page.CONFRIM_TEXT)

    def test_show_confirm_dialog_without_change(self):
        self.page.create_news_without_inputs("Title", "Content", "Ruotsi", "01.03.2016 00:00")
        self.page.is_alert_present()
        self.assertFalse(self.page.CONFRIM_TEXT)