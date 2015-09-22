from selenium import webdriver


class MainNavigation:
    def __init__(self, selenium):
        self.selenium = selenium

    def openPage(self, page):
        self.selenium.find_element_by_id('upload_link').click()

