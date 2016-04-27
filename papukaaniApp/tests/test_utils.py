from logging import Logger
from selenium import webdriver
import inspect
from selenium.common.exceptions import StaleElementReferenceException
import logging

logger = logging.getLogger(__name__)

from papukaani.config.common import PROJECT_DIR

__author__ = 'rapsutin&co'

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

# decorator for dealing with StaleElementReferenceExceptions caused by
# javascript changing the page
def retry_if_stale(function):

    tries = 3

    def wrapped(*args, **kwargs):
        tried = 0

        while 1:
            try:
                ret = function(*args, **kwargs)
                return ret
            except StaleElementReferenceException as e:
                tried += 1
                logger.info('got stale from %s, try %d' % (function.__name__, tried))
                if tried >= tries:
                    raise StaleAfterRetries(e)

    return wrapped

# a class decorator to apply a normal decorator to all methods
def decorate_all_methods(decorator):
    def dectheclass(cls):
        for name, m in inspect.getmembers(cls, inspect.isfunction):
            setattr(cls, name, decorator(m))
        return cls
    return dectheclass
