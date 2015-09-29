from selenium.webdriver.support.wait import WebDriverWait



class Page:

    def __init__(self, selenium):
        self.selenium = selenium


class Element:

    def __init__(self, location_strategy, locator):
        self.location_strategy = location_strategy
        self.locator = locator

    def __get__(self, instance, owner):
        selenium = instance.selenium
        WebDriverWait(selenium, 100).until(
            lambda selenium: selenium.find_element(
                self.location_strategy, self.locator
            )
        )
        return selenium.find_element(
                self.location_strategy, self.locator
            )