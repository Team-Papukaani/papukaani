from logging import Logger
from selenium import webdriver

from papukaani.config.common import PROJECT_DIR

__author__ = 'rapsutin'

def take_screenshot_of_test_case(test_case, web_driver):
    """
    Takes a screenshot from the browser and saves it to the default folder project_root/test_screenshots.
    Should only be used in the test teardown.
    :param test_case: A TestCase instance that is currently running.
    :param web_driver: A WebDriver instance that is currently running.
    """
    print("Screenshot saved into " + PROJECT_DIR + '/test_screenshots/'+test_case._testMethodName)
    web_driver.save_screenshot('test_screenshots/'+test_case._testMethodName)


def get_configured_firefox():
  profile = webdriver.FirefoxProfile()
  profile.set_preference('intl.accept_languages', '')
  driver = webdriver.Firefox(firefox_profile=profile)
  return driver

