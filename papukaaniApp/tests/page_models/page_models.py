from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.wait import WebDriverWait
from papukaaniApp.tests.page_models.page_model import Page, Element
import logging
from papukaaniApp.tests.test_utils import retry_if_stale, decorate_all_methods

logger = logging.getLogger(__name__)

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
    MESSAGE = Element(By.ID, 'messages')
    POLYLINE = Element(By.TAG_NAME, 'g')
    FORMAT_SELECTOR = Element(By.ID, 'fileFormat')

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

    def push_upload_button(self):
        upload = self.UPLOAD_FIELD
        upload.submit()

    def change_format_selection(self, key):
        sel = Select(self.FORMAT_SELECTOR)
        sel.select_by_value(key)


class PublicPage(Page):
    """
    Page Object for the public page.
    """
    url = BASE_URL + '/papukaani/public/'

    POLYLINE = Element(By.TAG_NAME, 'g')
    PLAY = Element(By.ID, 'play')
    PLAY_SLIDER  = Element(By.ID, 'playSlider')
    SINGLE_MARKER = Element(By.XPATH, './/img[contains(@class, "leaflet-marker-icon")]')
    SKIP = Element(By.ID, 'skip')
    SPEED_SLIDER = Element(By.ID, 'speedSlider')
    SPEED_SLIDER_LABEL = Element(By.ID, 'speedLabel')
    IFRAME_SRC = Element(By.ID, 'iframeSrc')
    IFRAME_BUTTON_OPEN = Element(By.ID, 'iframeOpen')
    IFRAME_BUTTON_CLOSE = Element(By.ID, 'iframeClose')
    TIME_START = Element(By.ID, 'start_time')
    TIME_END = Element(By.ID, 'end_time')
    INDIVIDUAL_SELECTOR = Element(By.ID, "selectIndividual")

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

    def play_animation_for_individual(self, key):
        self.change_individual_selection(key)
        self.play()

    def play(self):
        self.PLAY.click()
        time.sleep(0.5)

    def get_marker(self):
        return self.driver.find_element_by_class_name("leaflet-marker-icon")

    def get_popup(self):
        return self.driver.find_element_by_class_name("leaflet-popup-content-wrapper")

    def get_navigation(self):
        return self.driver.find_element_by_id("navbar")

    def change_individual_selection(self, key):
        sel = Select(self.INDIVIDUAL_SELECTOR)
        sel.select_by_value(key)
        while self.INDIVIDUAL_SELECTOR.get_attribute('disabled'):
            time.sleep(2)
        time.sleep(2)

    def remove_selected_individual(self, id):
        self.driver.find_element_by_css_selector("#individual" + str(id) + " button.remove").click()
        time.sleep(0.5)

    def get_speed_set_as_param(self, speed):
        self.driver.get(BASE_URL + '/papukaani/public/?speed=' + str(speed))
        return self.driver.execute_script('return $("#speedSlider").slider("option", "value")')


    def set_slider_value_to_min(self):
        minval = self.driver.execute_script('return $("#playSlider").slider("option", "min")')
        self.driver.execute_script('$("#playSlider").slider("option", "value", ' + str(minval) + ')')


    def get_iframe_url(self):
        time.sleep(1)
        self.IFRAME_BUTTON_OPEN.click()
        time.sleep(2)
        url = self.IFRAME_SRC.get_attribute('value')
        self.IFRAME_BUTTON_CLOSE.click()
        time.sleep(1)
        return url

    def get_linelayercanvas_as_base64(self):
        return self.driver.execute_script('return document.getElementById("lines-layer").toDataURL("image/png");')


class ChoosePage(Page):
    """
    Page Object for the choose page.
    """
    url = BASE_URL + '/papukaani/choose/?nofit=1'

    SAVE_BUTTON = Element(By.ID, 'save')
    MESSAGE_BOX = Element(By.ID, 'loading')
    MARKER = Element(By.CLASS_NAME, 'marker-cluster')
    ZOOM_IN = Element(By.CLASS_NAME, 'leaflet-control-zoom-in')
    ZOOM_OUT = Element(By.CLASS_NAME, 'leaflet-control-zoom-out')
    RESET_BUTTON = Element(By.ID, 'reset')
    START_TIME = Element(By.ID, 'start_time')
    END_TIME = Element(By.ID, 'end_time')
    SUBMIT_TIME = Element(By.ID, 'show_time_range')
    INDIVIDUAL_SELECTOR = Element(By.ID, 'selectIndividual')
    ALERT = Element(By.ID, 'popup')
    ALERT_YES = Element(By.ID, 'save_button')
    ALERT_NO = Element(By.ID, 'no_save_button')
    ALERT_CANCEL = Element(By.ID, 'cancel_button')

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

    def _double_click_by_class(self, cls):
        actionChains = ActionChains(self.driver)
        elem = self.driver.find_element_by_class_name(cls)
        actionChains.double_click(elem).perform()

    def click_public_cluster(self):
        self._double_click_by_class('marker-cluster-small')

    def click_private_cluster(self):
        self._double_click_by_class('marker-cluster-large')

    def click_partially_public_cluster(self):
        self._double_click_by_class('marker-cluster-medium')

    def save_and_change(self, id):
        self.save()
        self.change_individual_selection(id)

    def save(self):
        self.click_save_button()
        while self.INDIVIDUAL_SELECTOR.get_attribute('disabled'):
            time.sleep(0.2)

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
        while self.INDIVIDUAL_SELECTOR.get_attribute('disabled'):
            time.sleep(0.1)

    def set_start_time(self, string):
        self.START_TIME.send_keys(string)

    def set_end_time(self, string):
        self.END_TIME.send_keys(string)

    def set_end_time_forced_submit(self, string):
        self.END_TIME.send_keys(string + Keys.RETURN)

    def get_start_time(self):
        return self.START_TIME.get_attribute('value')

    def get_end_time(self):
        return self.END_TIME.get_attribute('value')

    def show_time_range(self):
        """
        Show the points that match the selected time range.
        """
        self.SUBMIT_TIME.click()

    def format_error(self):
        return self.driver.find_element_by_id("formatError").get_attribute("innerHTML")

    def popup_displayed(self):
        return self.ALERT.is_displayed()

    def popup_click_yes(self):
        self.ALERT_YES.click()
        while self.INDIVIDUAL_SELECTOR.get_attribute('disabled'):
            time.sleep(0.1)

    def popup_click_no(self):
        self.ALERT_NO.click()

    def popup_click_cancel(self):
        self.ALERT_CANCEL.click()

    def change_individual_selection(self, key):
        sel = Select(self.INDIVIDUAL_SELECTOR)
        sel.select_by_value(key)
        while self.INDIVIDUAL_SELECTOR.get_attribute('disabled'):
            time.sleep(0.1)

    def get_individual_selection(self):
        return self.INDIVIDUAL_SELECTOR.get_attribute('value')


@decorate_all_methods(retry_if_stale)
class DevicePage(Page):
    """
    Page Object for the device page.
    """

    url = BASE_URL + '/papukaani/devices/'

    def __init__(self):
        super().__init__()

    def clickNew(self):
        self._css('.new-button:not(.disabled)').click()

    def clickCancel(self):
        self._css('.cancel-button').click()

    def clickSave(self):
        self._css('.save-button').click()

    def _getRowBy(self, row=None, attID=None):

        if (row is not None) and (attID is not None):
            raise ValueError('Must specify only one of row and attID')

        # by row index
        if row is not None:
            rows = self.driver.find_elements_by_css_selector('.atts-list tbody tr')
            return rows[row]

        # by attachment id 
        if attID is not None:
            return self._css('.atts-list tbody tr#att-%s' % attID)

        raise ValueError('Must specify one of row and attID')

    def clickDelete(self, row=None, attID=None):
        row = self._getRowBy(row=row, attID=attID)
        delete = row.find_element_by_css_selector('.delete-button')
        delete.click()

    def clickEdit(self, row=None, attID=None):
        row = self._getRowBy(row=row, attID=attID)
        edit = row.find_element_by_css_selector('.edit-button')
        edit.click()

    def getDisplayedAttachTime(self, row=None, attID=None):
        row = self._getRowBy(row=row, attID=attID)
        return row.find_element_by_css_selector('.attach-time').text.strip()

    def getDisplayedRemoveTime(self, row=None, attID=None):
        row = self._getRowBy(row=row, attID=attID)
        el = row.find_element_by_css_selector('.remove-time')
        if el.find_elements_by_css_selector('.not-removed-note'):
            return None
        else:
            return el.text.strip()

    def getDisplayedIndividualName(self, row=None, attID=None):
        row = self._getRowBy(row=row, attID=attID)
        return row.find_element_by_css_selector('.attached-individual').text.strip()

    def numTableRows(self):
        return len(self.driver.find_elements_by_css_selector('.atts-list tbody tr'))

    def numAttachments(self):
        return len(self.driver.find_elements_by_css_selector('.att'))

    def getCurrentDeviceID(self):
        return self._css('#selectDevice').get_attribute('value')

    def _getIndividualInput(self):
        return self._css('.select-individual')

    def _getAttachedInput(self):
        return self._css('[name=attach-time]')

    def _getRemovedInput(self):
        return self._css('[name=remove-time]')

    def isEditing(self):
        return self._hasOne('.att.editing')

    def getEditingIndividualChoice(self):
        selected = self._getIndividualInput().get_attribute('value')
        if selected == 'None':
            return None
        return selected

    def getEditingAttachedChoice(self):
        return self._getAttachedInput().get_attribute('value')

    def getEditingRemovedChoice(self):
        return self._getRemovedInput().get_attribute('value')

    def inputAttachedChoice(self, s):
        self._getAttachedInput().clear()
        self._getAttachedInput().send_keys(s)

    def inputRemovedChoice(self, s):
        self._getRemovedInput().clear()
        self._getRemovedInput().send_keys(s)

    def inputIndividualChoice(self, indID):
        sel = Select(self._getIndividualInput())
        sel.select_by_value(indID)

    def changeDevice(self, devID):
        sel = Select(self._css('#selectDevice'))
        sel.select_by_value(devID)

    def hasNoneNote(self):
        return self._hasOne('.none-note')

    def hasTableHeadings(self):
        return self._hasOne('.atts-list thead')

    def hasMessage(self):
        return len(self._css('#message_area').text.strip()) > 0
        
    def hasErrorMessage(self):
        return self.hasMessage() and \
                'error-message' in self._css('#message_area').get_attribute('class')

    def hasInfoMessage(self):
        return self.hasMessage() and \
                'info-message' in self._css('#message_area').get_attribute('class')

    def hasNewButton(self):
        return self._hasOne('.new-button')

    def newButtonEnabled(self):
        return not ('disabled' in self._css('.new-button').get_attribute('class'))

    def deviceSelectorEnabled(self):
        return self._hasOne('#selectDevice') and \
            self._hasNone('#selectDevice[disabled=disabled]')

    def editDeleteButtonsPresentAndEnabled(self):
        return \
            self._hasNone('.edit-button.disabled') and \
            self._hasNone('.delete-button.disabled') and \
            self._hasSome('.edit-button:not(.disabled)') and \
            self._hasSome('.delete-button:not(.disabled)')

    def editDeleteButtonsPresentAndDisabled(self):
        return \
            self._hasSome('.edit-button.disabled') and \
            self._hasSome('.delete-button.disabled') and \
            self._hasNone('.edit-button:not(.disabled)') and \
            self._hasNone('.delete-button:not(.disabled)')

    def _css(self, selector):
        return self.driver.find_element_by_css_selector(selector)

    def _hasOne(self, selector):
        return len(self.driver.find_elements_by_css_selector(selector)) == 1

    def _hasSome(self, selector):
        return len(self.driver.find_elements_by_css_selector(selector)) > 0

    def _hasNone(self, selector):
        return len(self.driver.find_elements_by_css_selector(selector)) == 0


class IndividualPage(Page):
    """
    Page Object for the individual page.
    """
    url = BASE_URL + '/papukaani/individuals/'

    NEW_FORM = Element(By.ID, 'new_individual_form')
    NEW_NAME_FIELD = Element(By.ID, 'new_individual_nickname')
    NEW_TAXON_FIELD = Element(By.XPATH, '//input[@name="taxon"][1]')
    FIRST_TAXON_FIELD = Element(By.XPATH, '//form[@name="modify_individuals"][1]//input[@name="taxon"]')
    FIRST_NICKNAME_FIELD = Element(By.XPATH, '//form[@name="modify_individuals"][1]/input[@name="nickname"]')
    FIRST_RING_ID_FIELD = Element(By.XPATH, '//form[@name="modify_individuals"][1]/input[@name="ring_id"]')
    MODIFY_BUTTON = Element(By.XPATH, '//form[@name="modify_individuals"][1]/button[@name="modify"]')
    CONFIRM_MODIFY_BUTTON = Element(By.ID, 'confirm_modify')
    FIRST_DESCRIPTION_EN_FIELD = Element(By.XPATH, '//form[@name="modify_individuals"][1]//textarea[@name="descriptionEN"]')
    FIRST_DESCRIPTION_FI_FIELD = Element(By.XPATH, '//form[@name="modify_individuals"][1]//textarea[@name="descriptionFI"]')
    FIRST_DESCRIPTION_SV_FIELD = Element(By.XPATH, '//form[@name="modify_individuals"][1]//textarea[@name="descriptionSV"]')
    FIRST_DESCRIPTION_ENURL_FIELD = Element(By.XPATH, '//form[@name="modify_individuals"][1]//input[@name="descriptionUrlEN"]')
    FIRST_DESCRIPTION_FIURL_FIELD = Element(By.XPATH, '//form[@name="modify_individuals"][1]//input[@name="descriptionUrlFI"]')
    FIRST_DESCRIPTION_SVURL_FIELD = Element(By.XPATH, '//form[@name="modify_individuals"][1]//input[@name="descriptionUrlSV"]')
    MODIFY_DESCRIPTION_BUTTON = Element(By.XPATH, '//form[@name="modify_individuals"][1]//button[@name="modifyDescription"]')
    CLOSE_MODAL_BUTTON = Element(By.XPATH, '//form[@name="modify_individuals"][1]//button[@name="close"]')
    DELETE_BUTTON = Element(By.XPATH, '//form[@name="modify_individuals"][1]/button[@name="delete"]')
    DELETE_CONFIRM_BUTTON = Element(By.ID, 'yes_button')
    MESSAGE = Element(By.ID, 'messages')
    MODAL_TAB_LINK_FI = Element(By.XPATH, '//form[@name="modify_individuals"][1]//li[2]//a')
    MODAL_TAB_LINK_SV = Element(By.XPATH, '//form[@name="modify_individuals"][1]//li[3]//a')

    def get_message(self):
        """
        :return: The message after user action.
        """
        return self.MESSAGE.get_attribute('innerHTML')

    def create_new_individual(self, taxon, name):
        """
        Inputs the name of the new individual and submits the form.
        """
        self.driver.execute_script('return $(".combobox").removeAttr("required");')
        self.set_taxon_field_visible_for_input()
        namefield2 = self.NEW_TAXON_FIELD
        namefield2.send_keys(taxon)

        namefield = self.NEW_NAME_FIELD
        namefield.send_keys(name)
        namefield.submit()
        time.sleep(5)

    def set_taxon_field_visible_for_input(self):
        for attempt in range(10):
            try:
                self.driver.execute_script(
                    'return $("[name=\'taxon\']").attr("type", "text");')  # set taxon field visible for input
                break
            except:
                time.sleep(1)

    def get_first_individual_en(self):
        return self.FIRST_DESCRIPTION_EN_FIELD.get_attribute("value")

    def get_first_individual_fi(self):
        return self.FIRST_DESCRIPTION_FI_FIELD.get_attribute("value")

    def get_first_individual_sv(self):
        return self.FIRST_DESCRIPTION_SV_FIELD.get_attribute("value")

    def get_first_individual_enurl(self):
        return self.FIRST_DESCRIPTION_ENURL_FIELD.get_attribute("value")

    def get_first_individual_fiurl(self):
        return self.FIRST_DESCRIPTION_FIURL_FIELD.get_attribute("value")

    def get_first_individual_svurl(self):
        return self.FIRST_DESCRIPTION_SVURL_FIELD.get_attribute("value")

    def get_first_individual_taxon(self):
        self.driver.execute_script('return $(".combobox").show;')  # set taxon select visible
        return self.FIRST_TAXON_FIELD.get_attribute("value")

    def get_first_individual_nickname(self):
        return self.FIRST_NICKNAME_FIELD.get_attribute("value")

    def get_first_individual_ring_id(self):
        return self.FIRST_RING_ID_FIELD.get_attribute("value")

    def modify_descriptionurl(self, en, fi, sv):
        """
        Inputs the name and ring_id of an existing individual and submits the form.
        """
        self.MODIFY_DESCRIPTION_BUTTON.click()
        time.sleep(1)
        f1 = self.FIRST_DESCRIPTION_ENURL_FIELD
        f1.send_keys(en)
        time.sleep(1)
        self.driver.execute_script("tinyMCE.get('{0}').focus()".format("descriptionEN"))
        self.driver.execute_script("tinyMCE.activeEditor.setContent('{0}')".format("engtext"))
        self.MODAL_TAB_LINK_FI.click()
        time.sleep(1)
        f2 = self.FIRST_DESCRIPTION_FIURL_FIELD
        f2.send_keys(fi)
        time.sleep(1)
        self.driver.execute_script("tinyMCE.get('{0}').focus()".format("descriptionFI"))
        self.driver.execute_script("tinyMCE.activeEditor.setContent('{0}')".format("fitext"))
        self.MODAL_TAB_LINK_SV.click()
        time.sleep(1)
        f3 = self.FIRST_DESCRIPTION_SVURL_FIELD
        f3.send_keys(sv)
        time.sleep(1)
        self.driver.execute_script("tinyMCE.get('{0}').focus()".format("descriptionSV"))
        self.driver.execute_script("tinyMCE.activeEditor.setContent('{0}')".format("svtext"))
        time.sleep(1)
        self.CLOSE_MODAL_BUTTON.click()
        time.sleep(1)
        self.MODIFY_BUTTON.click()


    def modify_individual(self, nickname, ring_id):
        """
        Inputs the name and ring_id of an existing individual and submits the form.
        """
        modify_button = self.MODIFY_BUTTON
        nickname_field = self.FIRST_NICKNAME_FIELD
        nickname_field.clear()
        nickname_field.send_keys(nickname)
        ring_id_field = self.FIRST_RING_ID_FIELD
        ring_id_field.clear()
        ring_id_field.send_keys(ring_id)
        modify_button.click()

    def delete_individual(self):
        """
        Clicks the delete button.
        """
        delete_button = self.DELETE_BUTTON
        delete_button.click()
        confirm_button = self.DELETE_CONFIRM_BUTTON
        confirm_button.click()


class FormatPage(Page):
    url = BASE_URL + '/papukaani/formats/create/0'

    SUBMIT = Element(By.ID, "submit")
    HELP_BUTTON = Element(By.ID, "formatName_helpbutton")
    HELP_BOX = Element(By.ID, "help_formatName")
    FORMAT_NAME = Element(By.ID, "formatName")
    TIMESTAMP = Element(By.ID, "timestamp")
    DATE = Element(By.ID, "date")
    TIME = Element(By.ID, "time")
    LONGITUDE = Element(By.ID, "longitude")
    LATITUDE = Element(By.ID, "latitude")
    GPS_NUMBER = Element(By.ID, "manufacturerID")
    TEMPERATURE = Element(By.ID, "temperature")
    ALTITUDE = Element(By.ID, "altitude")

    def input_values_and_submit(self, format_name, timestamp, date, time, longitude, latitude, gps_number, temperature,
                                altitude):
        format_name_field = self.FORMAT_NAME
        format_name_field.send_keys(format_name)
        timestamp_field = self.TIMESTAMP
        timestamp_field.send_keys(timestamp)
        date_field = self.DATE
        date_field.send_keys(date)
        time_field = self.TIME
        time_field.send_keys(time)
        longitude_field = self.LONGITUDE
        longitude_field.send_keys(longitude)
        latitude_field = self.LATITUDE
        latitude_field.send_keys(latitude)
        gps_number_field = self.GPS_NUMBER
        gps_number_field.send_keys(gps_number)
        temperature_field = self.TEMPERATURE
        temperature_field.send_keys(temperature)
        altitude_field = self.ALTITUDE
        altitude_field.send_keys(altitude)

        altitude_field.submit()


class FormatListPage(Page):
    url = BASE_URL + '/papukaani/formats'

    FIRST_MODIFY_BUTTON = Element(By.XPATH, '//a[contains(@class, "glyphicon-pencil")][1]')
    FIRST_DELETE_BUTTON = Element(By.XPATH, '//a[contains(@class, "glyphicon-trash")][1]')
    DELETE_CONFIRM_BUTTON = Element(By.ID, 'yes_button')

    def does_page_contain(self, search):
        return search in self.driver.page_source

    def delete_first_format(self):
        self.FIRST_DELETE_BUTTON.click()
        self.DELETE_CONFIRM_BUTTON.click()

    def modify_first_format(self):
        self.FIRST_MODIFY_BUTTON.click()

class NewsPage(Page):
    """
    Page Object for the news page.
    """
    url = BASE_URL + '/papukaani/news/'
    CREATE_NEWS_BUTTON = Element(By.ID, 'create_news')
    FIRST_NEWS_TITLE = Element(By.ID, 'title')
    FIRST_NEWS_PUBLISHDATE = Element(By.ID, 'publishdate')
    FIRST_NEWS_LANGUAGE = Element(By.ID, 'language')
    FIRST_NEWS_TARGETS = Element(By.ID, 'targets')
    NEWS_TITLE = Element(By.ID, 'news_title')
    NEWS_CONTENT = Element(By.ID, 'news_content')
    NEWS_LANGUAGE = Element(By.ID, 'news_language')
    NEWS_PUBLISHDATE = Element(By.ID, 'news_publishDate')
    INDIVIDUAL_SELECTOR = Element(By.ID, 'selectIndividual')
    MESSAGE = Element(By.ID, 'messages')
    MODAL_MESSAGE = Element(By.ID, 'modalmessages')
    NEWS_SAVE_BUTTON = Element(By.XPATH, '//a[@id="news_tallenna"][1]')
    NEWS_CLOSE_BUTTON = Element(By.ID, 'news_close_button')
    NEWS_DELETE_BUTTON = Element(By.CLASS_NAME, 'remove')
    NEWS_MODIFY_BUTTON = Element(By.CLASS_NAME, 'update')
    NEWS_MODAL = Element(By.ID, 'news_modal')
    CONFRIM_TEXT = True


    def set_inputs(self, title, content, language, publishdate, targets="none"):
        time.sleep(1)
        self.CREATE_NEWS_BUTTON.click()
        time.sleep(1)
        self.NEWS_TITLE.send_keys(title)
        self.NEWS_LANGUAGE.send_keys(language)
        self.NEWS_PUBLISHDATE.send_keys(publishdate)
        time.sleep(1)
        self.driver.execute_script("tinyMCE.get('{0}').focus()".format("news_content"))
        self.driver.execute_script("tinyMCE.activeEditor.setContent('{0}')".format(content))
        self.NEWS_TITLE.click()
        time.sleep(1)

    def create_news(self, title, content, language, publishdate, targets="none"):
        self.set_inputs(title, content, language, publishdate, targets)
        self.NEWS_SAVE_BUTTON.click()

    def create_news_and_close_without_saving_accept(self, title, content, language, publishdate, targets="none"):
        self.set_inputs(title, content, language, publishdate, targets)
        self.NEWS_CLOSE_BUTTON.click()
        time.sleep(1)
        self.driver.switch_to.alert.accept()
        time.sleep(2)

    def create_news_with_inputs(self, title, content, language, publishdate, targets="none"):
        self.set_inputs(title, content, language, publishdate, targets)
        self.NEWS_CLOSE_BUTTON.click()
        time.sleep(1)

    def create_news_without_inputs(self, title, content, language, publishdate, targets="none"):
        self.set_inputs("", "", "", "", targets)
        self.NEWS_CLOSE_BUTTON.click()
        time.sleep(1)

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert().accept()
        except:
            self.CONFRIM_TEXT = False

    def create_news_and_close_without_saving_dismiss(self, title, content, language, publishdate, targets="none"):
        self.set_inputs(title, content, language, publishdate, targets)
        self.NEWS_CLOSE_BUTTON.click()
        time.sleep(1)
        self.driver.switch_to.alert.dismiss()
        time.sleep(2)

    def delete_first_news(self):
        self.NEWS_DELETE_BUTTON.click()
        self.driver.switch_to.alert.accept()
        time.sleep(1)

    def modify_news(self, title, content, language, publishdate):
        time.sleep(1)
        self.NEWS_MODIFY_BUTTON.click()
        time.sleep(1)
        self.NEWS_TITLE.clear()
        self.NEWS_TITLE.send_keys(title)
        self.NEWS_LANGUAGE.send_keys(language)
        self.NEWS_PUBLISHDATE.send_keys(publishdate)
        time.sleep(1)
        self.driver.execute_script("tinyMCE.get('{0}').focus()".format("news_content"))
        self.driver.execute_script("tinyMCE.activeEditor.setContent('{0}')".format(content))
        self.NEWS_TITLE.click()
        time.sleep(1)
        self.NEWS_SAVE_BUTTON.click()
        time.sleep(1)

    def add_targets(self, key):
        time.sleep(1)
        self.NEWS_MODIFY_BUTTON.click()
        time.sleep(1)
        self.driver.find_element_by_css_selector("button.remove").click()
        time.sleep(0.5)
        sel = Select(self.INDIVIDUAL_SELECTOR)
        sel.select_by_value(key)
        while self.INDIVIDUAL_SELECTOR.get_attribute('disabled'):
            time.sleep(2)
        time.sleep(2)
        self.NEWS_SAVE_BUTTON.click()
        time.sleep(1)


