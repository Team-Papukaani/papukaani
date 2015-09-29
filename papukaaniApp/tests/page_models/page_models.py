from selenium.webdriver.common.by import By

from papukaaniApp.tests.page_models.page_model import Page, Element


class MainNavigation(Page):

    UPLOAD_LINK = Element(By.ID, 'upload_link')

    def open_upload_page(self):
        self.UPLOAD_LINK.click()
