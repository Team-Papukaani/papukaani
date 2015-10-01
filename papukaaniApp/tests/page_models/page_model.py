from selenium.webdriver.support.wait import WebDriverWait
from pyvirtualdisplay import Display
from selenium import webdriver


class Page:
    """
    Basic Page Object to be used as super class.
    """
    display = None
    url = None

    def __init__(self):
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        self.driver = webdriver.Firefox()

    def navigate(self):
        """
        Proceed the driver to the set url.
        """
        self.driver.get(self.url)

    def close(self):
        self.driver.close()
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
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(
                self.location_strategy, self.locator
            )
        )
        return driver.find_element(
            self.location_strategy, self.locator
        )
