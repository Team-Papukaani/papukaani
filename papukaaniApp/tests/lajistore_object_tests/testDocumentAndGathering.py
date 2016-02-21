from django.test import TestCase
from papukaaniApp.models_LajiStore import *


class testDocumentAndGathering(TestCase):
    def setUp(self):
        gatherings = [gathering.Gathering("2015-09-15T08:00:00+03:00", [68.93023632, 23.19298104])]

        dict = {
            "deviceID" : "TestDevice",
            "dateCreated":"2015-09-14T15:29:28+03:00",
            "dateEdited":"2015-09-14T15:29:28+03:00",
            "gatherings": gatherings
            }
        self.doc = document.create(**dict)

    def tearDown(self):
        self.doc.delete()

    def test_create_and_delete(self):
        self.assertTrue(hasattr(self.doc,"id"))
        self.assertEquals("2015-09-14T15:29:28+03:00", self.doc.dateCreated)
        self.assertEquals([68.93023632, 23.19298104], self.doc.gatherings[0].geometry)

    def test_update_and_get(self):
        self.doc.gatherings[0].temperature = 4

        self.doc.update()
        self.doc = document.get(self.doc.id)

        self.assertEquals(4, self.doc.gatherings[0].temperature)

    def test_get_all(self):
        self.assertGreater(len(document.find()), 0)
