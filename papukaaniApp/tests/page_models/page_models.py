from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select

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


class PageWithDeviceSelector(Page):
    DEVICE_SELECTOR = Element(By.ID, 'selectDevice')

    def get_device_selection(self):
        return self.DEVICE_SELECTOR.get_attribute('value')

    def change_device_selection(self, key):
        sel = Select(self.DEVICE_SELECTOR)
        sel.select_by_value(key)


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


class PublicPage(PageWithDeviceSelector):
    """
    Page Object for the public page.
    """
    url = BASE_URL + '/papukaani/public/'

    def __init__(self):
        super().__init__()

    def get_map_polyline_elements(self):
        """
        :return: List of polyline elements
        """
        return self.driver.find_elements_by_tag_name("g")

    def get_number_of_points(self):
        plines = self.get_map_polyline_elements()
        no_of_pts = 0
        for line in plines:
            d = line.find_element_by_tag_name("path").get_attribute("d")
            no_of_pts += (len(d.split()) - 2)

        return no_of_pts


class ChoosePage(PageWithDeviceSelector):
    """
    Page Object for the choose page.
    """
    url = BASE_URL + '/papukaani/choose'

    SAVE_BUTTON = Element(By.ID, 'save')
    MESSAGE_BOX = Element(By.ID, 'loading')
    MARKER = Element(By.CLASS_NAME, 'marker-cluster-large')
    ZOOM_IN = Element(By.CLASS_NAME, 'leaflet-control-zoom-in')
    ZOOM_OUT = Element(By.CLASS_NAME, 'leaflet-control-zoom-out')
    RESET_BUTTON = Element(By.ID, 'reset')
    START_TIME = Element(By.ID, 'start_time')
    END_TIME = Element(By.ID, 'end_time')
    SUBMIT_TIME = Element(By.ID, 'show_time_range')
    DEVICE_SELECTOR = Element(By.ID, 'selectDevice')

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

    def number_of_visible_markers_on_map(self):
        """
        Calculates how many markers are currently shown to the user on the map.
        :return: The number of markers.
        """
        return len(self.driver.find_elements_by_class_name("leaflet-marker-icon"))

    def number_of_completely_public_clusters_on_map(self):
        """
        Counts the number of clusters that contain only public points.
        :return: The number of public (green) clusters.
        """
        return len(self.driver.find_elements_by_class_name("marker-cluster-small"))

    def number_of_partially_public_clusters_on_map(self):
        """
        Counts the number of clusters that contain at least 1 public point.
        :return: The number of partially public (yellow) clusters.
        """
        return len(self.driver.find_elements_by_class_name("marker-cluster-medium"))

    def number_of_private_clusters_on_map(self):
        """
        Counts the number of clusters that contain only private points.
        :return: The number of private (grey) clusters.
        """
        return len(self.driver.find_elements_by_class_name("marker-cluster-large"))

    def get_cluster_size(self):
        cluster = self.driver.find_element_by_class_name("marker-cluster")
        size = cluster.find_element_by_tag_name("div").find_element_by_tag_name("span").get_attribute("innerHTML")
        return size

    def map_zoom_in(self):
        self.ZOOM_IN.click()

    def map_zoom_out(self):
        self.ZOOM_OUT.click()

    def double_click_marker(self):
        """
        Performs a double click action on the marker.
        """
        actionChains = ActionChains(self.driver)
        actionChains.double_click(self.MARKER).perform()

    def reset(self):
        """
        Resets the page by clicking the reset button.
        """
        self.RESET_BUTTON.click()

    def set_start_time(self, string):
        self.START_TIME.send_keys(string)

    def set_end_time(self, string):
        self.END_TIME.send_keys(string)

    def set_end_time_forced_invalid(self):
        self.driver.executeScript("document.getElementById('end_time').setAttribute('value', 'notadate')")

    def get_start_time(self):
        return self.START_TIME.get_attribute('value')

    def get_end_time(self):
        return self.END_TIME.get_attribute('value')

    def change_device_selection(self, key):
        sel = Select(self.DEVICE_SELECTOR)
        sel.select_by_value(key)

    def show_time_range(self):
        """
        Show the points that match the selected time range.
        """
        self.SUBMIT_TIME.click()

    def format_error(self):
        return self.driver.find_element_by_id("formatError").get_attribute("innerHTML")
