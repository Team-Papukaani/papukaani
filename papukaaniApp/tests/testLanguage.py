from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from papukaaniApp.tests.page_models.page_models import NavigationPage, UploadPage, PublicPage, BASE_URL
from papukaaniApp.tests.page_models.page_model import Page
from django.utils import translation
from django.conf import settings

class TestTranslation(TestCase):
    def test_translations_differ(self):
        s = 'Lataa tiedosto'
        with translation.override('en'):
            s_en = translation.ugettext(s)
        with translation.override('fi'):
            s_fi = translation.ugettext(s)
        with translation.override('sv'):
            s_sv = translation.ugettext(s)
        self.assertTrue(s_en != s_fi)
        self.assertTrue(s_en != s_sv)
        self.assertTrue(s_sv != s_fi)

class TestLanguage(StaticLiveServerTestCase):
    def setUp(self):
        self.default_lang = settings.LANGUAGE_CODE
        self.other_lang = self._get_other_lang(self.default_lang)

    def tearDown(self):
        pass

    def test_is_in_default_language(self):
        nav = NavigationPage()
        nav.navigate()

        self.assertTrue(self._page_with_nav_is_in_lang(nav, self.default_lang))

        nav.close()

    def test_language_changes(self):
        nav = NavigationPage()
        nav.navigate()

        self.assertTrue(self._page_with_nav_is_in_lang(nav, self.default_lang))
        self._change_language_via_picker(nav.driver, self.other_lang)
        self.assertTrue(self._page_with_nav_is_in_lang(nav, self.other_lang))

        nav.close()

    def test_selection_persists(self):
        page = Page()
        page.url = NavigationPage.url
        page.navigate()

        self._change_language_via_picker(page.driver, self.other_lang)
        page.url = UploadPage.url
        page.navigate()
        self.assertTrue(self._page_with_nav_is_in_lang(page, self.other_lang))

        page.close()

    def test_lang_parameter_sets_language(self):
        page = Page()
        page.url = '%s?lang=%s' % (NavigationPage.url, self.other_lang)
        page.navigate()

        self.assertTrue(self._page_with_nav_is_in_lang(page, self.other_lang))
        page.close()

    def test_lang_parameter_does_not_break_picker(self):
        page = Page()
        page.url = '%s?lang=%s' % (NavigationPage.url, self.other_lang)
        page.navigate()
        self.assertTrue(self._page_with_nav_is_in_lang(page, self.other_lang))
        self._change_language_via_picker(page.driver, self.default_lang)
        self.assertTrue(self._page_with_nav_is_in_lang(page, self.default_lang))

    def test_iframe_has_correct_language(self):
        public = PublicPage()
        public.url += '?lang=%s' % self.other_lang
        public.navigate()
        self.assertTrue(self._public_page_is_in_lang(public, self.other_lang))
        url = public.get_iframe_url()
        good_url = BASE_URL + url.split('127.0.0.1')[1]
        public.close()

        page = PublicPage()
        page.url = good_url
        page.navigate()
        self.assertTrue(self._public_page_is_in_lang(page, self.other_lang))
        page.close()

    def _change_language_via_picker(self, driver, target_lang):
        driver.find_element_by_id('language_%s' % target_lang).click()

    def _page_with_nav_is_in_lang(self, page, lang):
        ul_text = page.driver.find_element_by_id('upload_link').text
        with translation.override(lang):
            is_in_lang = self._similarStrings(ul_text, translation.ugettext('Lataa tiedosto'))
        with translation.override(self._get_other_lang(lang)):
            is_in_other_lang = self._similarStrings(ul_text, translation.ugettext('Lataa tiedosto'))
        return (is_in_lang and not is_in_other_lang)

    def _public_page_is_in_lang(self, page, lang):

        def refresh_in(lang):
            if lang == 'fi':
                return 'Lisää lintu'
            if lang == 'sv':
                return 'Uppdatera'
            if lang == 'en':
                return 'Refresh'

        with translation.override(lang):
            is_in_lang = self._similarStrings(page.REFRESH.text,
                    refresh_in(lang))
        with translation.override(self._get_other_lang(lang)):
            is_in_other_lang = self._similarStrings(page.REFRESH.text,
                    refresh_in(self._get_other_lang(lang)))
        return (is_in_lang and not is_in_other_lang)

    def _get_other_lang(self, lang):
        if lang == 'fi':
            return 'en'
        else:
            return 'fi'

    def _similarStrings(self, str1, str2):
        return (str1.strip().lower() == str2.strip().lower())
