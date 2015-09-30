from selenium.webdriver.support.wait import WebDriverWait


class Page:
    url = None

    def __init__(self, driver):
        self.driver = driver

    def navigate(self):
        self.driver.get(self.url)


class Element:
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
