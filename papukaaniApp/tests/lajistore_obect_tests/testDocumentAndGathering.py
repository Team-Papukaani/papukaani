from django.test import TestCase
from papukaaniApp.models_LajiStore import document


class testDocumentAndGathering(TestCase):
    def setUp(self):
        dict = {
            "documentId": "TestId0000001",
            "createdAt":"2015-09-14T15:29:28+03:00",
            "lastModifiedAt":"2015-09-14T15:29:28+03:00",
            "facts": [],
            "gatherings": [
                            {
                             "timeStart": "2015-09-15T08:00:00+03:00",
                             "wgs84Geometry": {
                                "type": "Point",
                                "coordinates": [68.93023632, 23.19298104]
                             },
                             "temperatureCelsius": -3,
                             "facts": [],
                             "units": [],
                             "publicity":"public"
                           }
                    ]
            }
        self.doc = document.create(**dict)

    def tearDown(self):
        self.doc.delete()

    def test_create_and_delete(self):
        self.assertEquals("TestId0000001", self.doc.documentId)
        self.assertEquals("2015-09-14T15:29:28+03:00", self.doc.createdAt)
        self.assertEquals([68.93023632, 23.19298104], self.doc.gatherings[0].geometry)

    def test_update_and_get(self):
        self.doc.lastModifiedAt = "2015-10-06T15:29:28+03:00"
        self.doc.gatherings[0].temperature = 4

        self.doc.update()
        self.doc = document.get(self.doc.id)

        self.assertEquals("2015-10-06T15:29:28+03:00", self.doc.lastModifiedAt)
        self.assertEquals(4, self.doc.gatherings[0].temperature)

    def test_get_all(self):
        self.assertGreater(len(document.get_all()), 0)
