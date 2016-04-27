from selenium.webdriver.support.select import Select
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from papukaaniApp.models_LajiStore import *
from papukaaniApp.tests.page_models.page_models import DevicePage
from papukaaniApp.tests.test_utils import retry_if_stale
from papukaaniApp.services.deviceindividual_service import DeviceIndividual
from papukaaniApp.utils import model_utils 
import datetime
import time

_filePath = "papukaaniApp/tests/test_files/"

_times = {}
for i in range(1,31):
    _times[i] = datetime.datetime(2015, 1, i, 12, i, 0)

_future = datetime.datetime.now() + datetime.timedelta(days=7)

class DeviceTest(StaticLiveServerTestCase):

    def _waitUntil(self, test, maxtime=20):
        interval = 0.1
        waited = 0
        while 1:
            if waited > maxtime:
                raise WaitTimeout("Timed out when waiting for %s" % test.__name__)
            if test():
                return
            time.sleep(interval)
            waited += interval

    def _waitUntilNot(self, test, maxtime=20):
        def negTest():
            return not test()
        self._waitUntil(negTest, maxtime=maxtime)

    def _datetime_to_inputformat(self, dt):
        return dt.strftime('%d.%m.%Y %H:%M')

    def _datetime_to_pageformat(self, dt):
        return dt.strftime('%d.%m.%Y %H:%M')

    def _pageformat_to_datetime(self, s):
        return datetime.datetime.strptime(s, '%d.%m.%Y %H:%M')

    def _inputformat_to_datetime(self, s):
        return datetime.datetime.strptime(s, '%d.%m.%Y %H:%M')

    def _is_pageformat_time(self, s):
        try:
            self._pageformat_to_datetime(s)
            return True
        except ValueError:
            return False

    def assertEventually(self, test, maxtime=20):
        try:
            self._waitUntil(test, maxtime=maxtime)
        except WaitTimeout:
            raise AssertionError("assertEventually of %s timed out" % test.__name__)

    def assertEventuallyNot(self, test, maxtime=20):
        def negTest():
            return not test()
        self.assertEventually(negTest, maxtime=maxtime)

    @retry_if_stale
    def sortedCorrectly(self):
        attRows = self.page.driver.find_elements_by_css_selector('.att display')
        attachTimes = [
                self._pageformat_to_datetime(
                    row.find_element_by_css_selector('.attach-time').text)
                for row in attRows ]
        if sorted(attachTimes) == attachTimes:
            return True
        else:
            return False

    def clickNewExpectSuccess(self):
        self.page.clickNew()
        self.assertEventually(self.properNewEditingView)

    def clickDeleteExpectSuccess(self, row=None, attID=None):
        self.page.clickDelete(row=row, attID=attID)
        self.assertEventually(self.properDisplayView)        

    def clickEditExpectSuccess(self, row=None, attID=None):
        self.page.clickEdit(row=row, attID=attID)
        self.assertEventually(self.properExistingEditingView)

    def clickCancelExpectSuccess(self):
        self.page.clickCancel()
        self.assertEventually(self.properDisplayView)

    def clickSaveExpectSuccess(self):
        self.page.clickSave()
        self.assertEventually(self.properDisplayView)

    def changeDeviceExpectSuccess(self, devID):
        self.page.changeDevice(devID)
        self.assertEventually(self.properDisplayView)

    def makeNew(self, individualID, attach, remove=None):
        self.clickNewExpectSuccess()
        self.assertTrue(self.properNewEditingView())
        self.page.inputIndividualChoice(individualID)
        self.page.inputAttachedChoice(self._datetime_to_inputformat(attach))
        if remove is not None:
            self.page.inputRemovedChoice(self._datetime_to_inputformat(remove))
        self.clickSaveExpectSuccess()

    @retry_if_stale
    def dropdownMatchesPage(self):
        select_id = self.page.driver.find_element_by_css_selector('#selectDevice').get_attribute('value')
        page_id = self.page.driver.find_element_by_css_selector('.atts-list').get_attribute('data-id')
        return select_id == page_id

    def properDisplayView(self):
        return \
                self.page.hasTableHeadings() and \
                self.page.hasNewButton() and \
                self.dropdownMatchesPage() and \
                self.page.newButtonEnabled() and \
                not self.page.isEditing() and \
                self.page.deviceSelectorEnabled()

    def properEmptyDisplayView(self):
        return \
                self.properDisplayView() and \
                self.page.hasNoneNote() and \
                self.page.numTableRows() == 1

    def properNonEmptyDisplayView(self):
        return \
                self.properDisplayView() and \
                not self.page.hasNoneNote() and \
                self.page.numTableRows() >= 1

    def properEditingView(self):
        if self.page.numTableRows() > 1:
            if not self.page.editDeleteButtonsPresentAndDisabled():
                return False
        return \
                self.page.isEditing() and \
                not self.page.hasNoneNote() and \
                not self.page.newButtonEnabled() and \
                not self.page.deviceSelectorEnabled()

    def properNewEditingView(self):
        return \
                self.properEditingView() and \
                self.page.getEditingIndividualChoice() is None and \
                self.page.getEditingAttachedChoice() == "" and \
                self.page.getEditingRemovedChoice() == ""

    def properExistingEditingView(self):
        return \
                self.properEditingView() and \
                self.page.getEditingIndividualChoice() is not None and \
                self._is_pageformat_time(self.page.getEditingAttachedChoice())



class TestDeviceFrontend(DeviceTest):

    @classmethod
    def setUpClass(cls):
        super(TestDeviceFrontend, cls).setUpClass()
        cls.page = DevicePage()

        cls.I1 = individual.create("DummyBird1", "DummyTaxon")
        cls.I2 = individual.create("DummyBird2", "DummyTaxon")

        dev1 = {
            "deviceManufacturerID": "DummyDev1",
            "deviceType": "DummyType",
            "deviceManufacturer": "DummyManufacturer",
            "dateCreated": "2015-09-29T14:00:00+03:00",
            "dateEdited": "2015-09-29T14:00:00+03:00"
        }
        cls.D1 = device.create(**dev1)
        dev2 = {
            "deviceManufacturerID": "DummyDev2",
            "deviceType": "DummyType",
            "deviceManufacturer": "DummyManufacturer",
            "dateCreated": "2015-09-29T14:00:00+03:00",
            "dateEdited": "2015-09-29T14:00:00+03:00"
        }
        cls.D2 = device.create(**dev2)

    @classmethod
    def tearDownClass(cls):
        device.delete_all()
        individual.delete_all()
        cls.page.close()
        super(TestDeviceFrontend, cls).tearDownClass()

    def setUp(self):
        self.page.navigate()
        self.changeDeviceExpectSuccess(self.D1.id)

    def tearDown(self):
        DeviceIndividual.delete_all()

    def makeThree(self):
        # sorted by attach time, so:
        self.makeNew(self.I1.id, _times[6], _times[8])  # middle row (row=1)
        self.makeNew(self.I2.id, _times[2], _times[4])  # top row (row=0)
        self.makeNew(self.I2.id, _times[10], None)  # bottom row (row=2) 

    def assertThreeCorrectlyDisplayed(self):
        self.assertTrue(self.properNonEmptyDisplayView())
        self.assertTrue(self.page.numAttachments() == 3)

        self.assertTrue(self.page.getDisplayedAttachTime(row=0) 
                == self._datetime_to_pageformat(_times[2]))
        self.assertTrue(self.page.getDisplayedRemoveTime(row=0) 
                == self._datetime_to_pageformat(_times[4]))
        self.assertTrue(self.page.getDisplayedIndividualName(row=0) 
                == self.I2.nickname)

        self.assertTrue(self.page.getDisplayedAttachTime(row=1) 
                == self._datetime_to_pageformat(_times[6]))
        self.assertTrue(self.page.getDisplayedRemoveTime(row=1) 
                == self._datetime_to_pageformat(_times[8]))
        self.assertTrue(self.page.getDisplayedIndividualName(row=1) 
                == self.I1.nickname)

        self.assertTrue(self.page.getDisplayedAttachTime(row=2) 
                == self._datetime_to_pageformat(_times[10]))
        self.assertTrue(self.page.getDisplayedRemoveTime(row=2) is None)
        self.assertTrue(self.page.getDisplayedIndividualName(row=2) 
                == self.I2.nickname)

    def assertNewNotAcceptedWith(self, individualID, attach, remove):
        self.page.clickNew()
        if individualID is not None:
            self.page.inputIndividualChoice(individualID)
        if attach is not None:
            self.page.inputAttachedChoice(self._datetime_to_inputformat(attach))
        if remove is not None:
            self.page.inputRemovedChoice(self._datetime_to_inputformat(remove))
        self.page.clickSave()
        self.assertEventually(self.page.hasErrorMessage)
        self.clickCancelExpectSuccess()
        self.assertEventuallyNot(self.page.hasErrorMessage)

    def test_010_empty_ok(self):
        self.assertTrue(self.properEmptyDisplayView())
        self.assertTrue(not self.page.hasMessage())

    def test_020_new_then_cancel(self):
        self.clickNewExpectSuccess()
        self.assertEventually(lambda: self.page.numTableRows() == 1)
        self.assertTrue(not self.page.hasMessage())
        self.clickCancelExpectSuccess()
        self.assertTrue(not self.page.hasMessage())

    def test_030_long_use_case_with_subtests(self):

        def subtest_same_data_after_reload():
            self.changeDeviceExpectSuccess(self.D2.id)
            self.changeDeviceExpectSuccess(self.D1.id)

            self.assertThreeCorrectlyDisplayed()

        def subtest_edit_then_cancel():
            self.clickEditExpectSuccess(row=1) 
            self.clickCancelExpectSuccess()

        def subtest_editing_starts_with_correct_data():
            self.clickEditExpectSuccess(row=1)
            self.assertTrue(self.page.getEditingIndividualChoice() == self.I1.id)
            self.assertTrue(self.page.getEditingAttachedChoice() == 
                    self._datetime_to_inputformat(_times[6]))
            self.assertTrue(self.page.getEditingRemovedChoice() == 
                    self._datetime_to_inputformat(_times[8]))
            self.clickCancelExpectSuccess()

            self.clickEditExpectSuccess(row=2)
            self.assertTrue(self.page.getEditingIndividualChoice() == self.I2.id)
            self.assertTrue(self.page.getEditingAttachedChoice() == 
                    self._datetime_to_inputformat(_times[10]))
            self.assertTrue(self.page.getEditingRemovedChoice().strip() == "")
            self.clickCancelExpectSuccess()

        def _edited_content_correct():
            self.assertTrue(self.properNonEmptyDisplayView())
            self.assertTrue(self.page.numAttachments() == 3)

            self.assertTrue(self.page.getDisplayedAttachTime(row=1) 
                    == self._datetime_to_pageformat(_times[5]))
            self.assertTrue(self.page.getDisplayedRemoveTime(row=1) 
                    == self._datetime_to_pageformat(_times[9]))
            self.assertTrue(self.page.getDisplayedIndividualName(row=1) 
                    == self.I2.nickname)

            self.assertTrue(self.page.getDisplayedAttachTime(row=2) 
                    == self._datetime_to_pageformat(_times[10]))
            self.assertTrue(self.page.getDisplayedRemoveTime(row=2) 
                    == self._datetime_to_pageformat(_times[12]))
            self.assertTrue(self.page.getDisplayedIndividualName(row=2) 
                    == self.I2.nickname)

        def subtest_edit_save_works():
            self.clickEditExpectSuccess(row=1)
            self.page.inputAttachedChoice(self._datetime_to_inputformat(_times[5]))
            self.page.inputRemovedChoice(self._datetime_to_inputformat(_times[9]))
            self.page.inputIndividualChoice(self.I2.id)
            self.clickSaveExpectSuccess()

            self.clickEditExpectSuccess(row=2)
            self.page.inputRemovedChoice(self._datetime_to_inputformat(_times[12]))
            self.clickSaveExpectSuccess()

            _edited_content_correct()

            self.changeDeviceExpectSuccess(self.D2.id)
            self.changeDeviceExpectSuccess(self.D1.id)

            _edited_content_correct()

        def subtest_delete_works():
            self.clickDeleteExpectSuccess(row=1)
            self.assertTrue(self.properNonEmptyDisplayView())
            self.assertTrue(self.page.numAttachments() == 2)

            self.clickDeleteExpectSuccess(row=1)
            self.assertTrue(self.properNonEmptyDisplayView())
            self.assertTrue(self.page.numAttachments() == 1)

            self.changeDeviceExpectSuccess(self.D2.id)
            self.changeDeviceExpectSuccess(self.D1.id)

            self.assertTrue(self.properNonEmptyDisplayView())
            self.assertTrue(self.page.numAttachments() == 1)


        self.makeThree()
        self.assertThreeCorrectlyDisplayed()

        subtest_same_data_after_reload()

        subtest_edit_then_cancel()

        self.assertThreeCorrectlyDisplayed()

        subtest_editing_starts_with_correct_data()

        self.assertThreeCorrectlyDisplayed()

        subtest_edit_save_works()
        
        subtest_delete_works()

    def test_040_validation_subtests(self):

        def subtest_must_specify_individual():
            self.assertNewNotAcceptedWith(None, _times[20], _times[22])

        def subtest_must_specify_attach_time():
            self.assertNewNotAcceptedWith(self.I1.id, None, _times[20])

        def subtest_attach_time_cannot_be_in_future():
            self.assertNewNotAcceptedWith(self.I1.id, _future, None)

        def subtest_remove_time_cannot_be_in_future():
            self.assertNewNotAcceptedWith(self.I1.id, _times[20], _future)

        def subtest_cannot_specify_nothing():
            self.assertNewNotAcceptedWith(None, None, None)

        def subtest_attach_must_be_before_remove():
            self.assertNewNotAcceptedWith(self.I1.id, _times[22], _times[20])

        def subtest_cannot_add_overlapping_new():
            # would overlap with one of the "three"
            self.assertNewNotAcceptedWith(self.I1.id, _times[5], _times[7])

        def subtest_cannot_edit_to_overlap():
            # would overlap with one of the "three"
            self.clickEditExpectSuccess(row=0)
            self.page.inputRemovedChoice(self._datetime_to_pageformat(_times[7]))
            self.page.clickSave()
            self.assertEventually(self.page.hasErrorMessage)
            self.clickCancelExpectSuccess()
            self.assertTrue(not self.page.hasMessage())

        def subtest_can_clear_removed():
            self.clickDeleteExpectSuccess(row=2)
            self.clickEditExpectSuccess(row=1)
            self.page.inputRemovedChoice("")
            self.clickSaveExpectSuccess()
            self.assertTrue(not self.page.hasErrorMessage())

        self.makeThree()

        subtest_must_specify_individual()

        subtest_must_specify_attach_time()

        subtest_attach_time_cannot_be_in_future()

        subtest_remove_time_cannot_be_in_future()
        
        subtest_cannot_specify_nothing()

        subtest_attach_must_be_before_remove()

        subtest_cannot_add_overlapping_new()

        self.assertThreeCorrectlyDisplayed()

        subtest_cannot_edit_to_overlap()
 
        self.assertThreeCorrectlyDisplayed()

        subtest_can_clear_removed()
    
    def test_050_more_validation_subtests(self):

        def subtest_can_attach_currently_attached_device_in_past():
            self.makeNew(self.I1.id, _times[4], _times[6])

        def subtest_can_attach_to_currently_tracked_bird_in_past():
            self.changeDeviceExpectSuccess(self.D2.id)
            self.makeNew(self.I1.id, _times[1], _times[2])

        def subtest_cannot_attach_to_already_tracked_bird():
            self.assertNewNotAcceptedWith(self.I1.id, _times[12], _times[14])

        def subtest_cannot_edit_to_overlap_already_tracked_bird():
            self.makeNew(self.I1.id, _times[9], _times[10])
            self.clickEditExpectSuccess(row=0)
            self.page.inputRemovedChoice(self._datetime_to_inputformat(_times[11]))
            self.page.clickSave()
            self.assertEventually(self.page.hasErrorMessage)
            self.clickCancelExpectSuccess()

        self.makeNew(self.I1.id, _times[10], None)

        subtest_cannot_edit_to_overlap_already_tracked_bird()

        subtest_can_attach_currently_attached_device_in_past()

        subtest_can_attach_to_currently_tracked_bird_in_past()

        subtest_cannot_attach_to_already_tracked_bird()

class WaitTimeout(Exception):
    pass

class StaleAfterRetries(Exception):
    def __init__(self, original_err):
        super(StaleAfterRetries, self).__init__()
        self.original_err = original_err
