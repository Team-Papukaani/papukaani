from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from papukaaniApp.tests.page_models.page_model import Page, Element

BASE_URL = "http://127.0.0.1:8081"


class NavigationPage(Page):
    """
    Page Object for the index page.
    """
    url = BASE_URL + '/papukaani/'

    UPLOAD_LINK = Element(By.ID, 'upload_link')

    def open_upload_page(self):
        """
        Click the link-element and proceed to the page it directs to.
        """
        self.UPLOAD_LINK.click()


class UploadPage(Page):
    """
    Page Object for the upload page.
    """
    url = BASE_URL + '/papukaani/upload/'

    UPLOAD_FIELD = Element(By.NAME, 'file')
    MESSAGE = Element(By.ID, 'message')
    POLYLINE = Element(By.TAG_NAME, 'g')

    def upload_file(self, filepath):
        """
        Inputs the path of the file-to-be-uploaded and submits the form.
        """
        upload = self.UPLOAD_FIELD
        upload.send_keys(filepath)
        upload.submit()

    def get_message(self):
        """
        :return: The error message after an attempted upload, if applicable.
        """
        return self.MESSAGE.get_attribute('innerHTML')

    def get_map_polyline_elements(self):
        """
        :return: The element containing a polyline formed of the points.
        """
        return self.POLYLINE


class PublicPage(Page):
    """
    Page Object for the public page.
    """
    url = BASE_URL + '/papukaani/public/'

    POINTS_JSON = Element(By.ID, 'mapScript')
    POLYLINE = Element(By.TAG_NAME, 'g')

    def __init__(self, driver, creature_id):
        super().__init__(driver)
        self.url += str(creature_id)

    def get_points_json(self):
        """
        :return: The json of the list of points in text form.
        """
        return str(self.POINTS_JSON.get_attribute("innerHTML"))

    def get_map_polyline_elements(self):
        """
        :return: The element containing a polyline formed of the points.
        """
        return self.POLYLINE


class ChoosePage(Page):
    """
    Page Object for the choose page.
    """
    url = BASE_URL + '/papukaani/choose'

    SAVE_BUTTON = Element(By.ID, 'save')
    MESSAGE_BOX = Element(By.ID, 'loading')
    MARKER = Element(By.CLASS_NAME, "leaflet-marker-icon")

    def click_save_button(self):
        """
        Clicks the save button on the page.
        """
        self.SAVE_BUTTON.click()

    def save_button_is_enabled(self):
        """
        :return: The boolean status of whether the save button is enabled or not.
        """
        return self.SAVE_BUTTON.is_enabled()

    def get_marker_src(self):
        """
        :return: The source of the icon used by the marker.
        """
        return self.MARKER.get_attribute('src')

    def double_click_marker(self):
        """
        Performs a double click action on the marker.
        """
        actionChains = ActionChains(self.driver)
        actionChains.double_click(self.MARKER).perform()
