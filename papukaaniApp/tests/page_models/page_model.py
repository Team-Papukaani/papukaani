from selenium.common.exceptions import TimeoutException, ElementNotVisibleException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from pyvirtualdisplay import Display
from selenium import webdriver

from django.conf import settings


class Page:
    """
    Basic Page Object to be used as super class.
    """
    display = None
    url = None

    def __init__(self):
        self.display = Display(visible=settings.XEPHYR_VISIBILITY, size=(1680, 720))
        self.display.start()
        fp = webdriver.FirefoxProfile()
        fp.set_preference('intl.accept_languages', 'fi')
        self.driver = webdriver.Firefox(firefox_profile=fp)

    def navigate(self):
        """
        Proceed the driver to the set url.
        """
        self.driver.get(self.url)

    def close(self):
        self.driver.quit()
        self.display.stop()


class Element:
    """
    Provides webdriver's find element functions.
    """

    def __init__(self, location_strategy, locator):
        self.location_strategy = location_strategy
        self.locator = locator


    def __get__(self, instance, owner):
        driver = instance.driver
        try:
            self._attempt_finding_element(driver)
        except(TimeoutException):
            raise NoSuchElementException(msg="Could not find the element")

        found_element = driver.find_element(
            self.location_strategy, self.locator
        )

        return found_element

    def _attempt_finding_element(self, driver):
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(
                self.location_strategy, self.locator
            )
        )
