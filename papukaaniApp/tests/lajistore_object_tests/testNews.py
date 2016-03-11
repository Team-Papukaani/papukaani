from django.test import TestCase
from papukaaniApp.models_LajiStore import *


class TestNews(TestCase):
    def setUp(self):
        new = {
            "title": "Good News!",
            "content": "newsnewsnews",
            "language": "en"
        }

        self.n = news.create(**new)

    def tearDown(self):
        news.delete_all()

    def test_create(self):
        self.assertEquals("Good News!", self.n.title)
        self.assertEquals("newsnewsnews", self.n.content)
        self.assertEquals("en", self.n.language)

    def test_bad_create(self):
        with self.assertRaises(TypeError):
            news.create({})

    def test_update_and_get(self):
        str = "fi"
        self.n.language = str
        self.n.update()
        gotten = news.get(self.n.id)
        self.assertEquals(str, gotten.language)

    def test_get_all(self):
        self.assertEquals(len(news.find()), 1)

    def test_get_all_with_two(self):
        new = {
            "title": "",
            "content": "",
            "language": "se"
        }

        news.create(**new)
        self.assertEquals(len(news.find()), 2)

    # def test_attach(self):
    #     A, B = self._create_individuals()
    #     self.d.attach_to(A.id, "2015-10-10T10:10:10+00:00")
    #     self.assertEquals(A.id, self.d.get_attached_individualid())
    #     self._delete_individuals([A, B])
    #
    # def test_device_not_attach_if_unremoved_devices_in_individuals(self):
    #     self.d.individuals = []
    #
    #     A, B = self._create_individuals()
    #     self.d.attach_to(A.id, "2015-10-10T10:10:10+00:00")
    #     self.d.attach_to(B.id, "2015-10-10T10:10:10+00:00")
    #     attachments = self.d.get_attachments()
    #
    #     self.assertEquals(len(attachments), 1)
    #     self.assertTrue(attachments[0]["removed"] is None)
    #
    #     self._delete_individuals([A, B])
    #
    # def test_another_device_can_be_attached_after_removal(self):
    #     self.d.individuals = []
    #
    #     A, B = self._create_individuals()
    #     self.d.attach_to(A.id, "2015-10-10T10:10:10+00:00")
    #     self.d.detach_from(A.id, "2015-10-10T10:10:10+00:00")
    #     self.assertTrue(self.d.attach_to(B.id, "2015-10-10T10:10:10+00:00") is None)
    #
    #     self._delete_individuals([A, B])
    #
    # def test_remove(self):
    #     A, B = self._create_individuals()
    #     self.d.attach_to(A.id, "2015-10-10T10:10:10+00:00")
    #     self.d.detach_from(A.id, "2015-10-10T10:10:10+00:00")
    #     individuals = self.d.get_attachments()
    #     self.assertEquals(len(individuals), 1)
    #     self.assertTrue(individuals[0]["removed"] is not None)
    #
    #     self._delete_individuals([A, B])

    def test_getting_attached_is_empty(self):
        self.assertEqual([], self.n.get_attached_individuals())

        # def test_getting_individuals(self):
        #     A, B = self._create_individuals()
        #     self.d.attach_to(A.id, "2015-10-10T10:10:10+00:00")
        #     self.d.detach_from(A.id, "2015-10-10T10:10:10+00:01")
        #     self.d.attach_to(B.id, "2015-10-10T10:10:10+00:02")
        #     individuals = self.d.get_attachments()
        #     self.assertEquals(len(individuals), 2)
        #
        #     self._delete_individuals([A, B])
        #
        # def test_checking_if_an_individual_is_attached(self):
        #     self.assertFalse(self.d.is_attached())
        #
        #     A, B = self._create_individuals()
        #     self.d.attach_to(A.id, "2015-10-10T10:10:10+00:00")
        #     self.assertTrue(self.d.is_attached())
        #
        #     self._delete_individuals([A, B])

        # def _create_individuals(self):
        #     return individual.create("LintuA", "TaxonA"), individual.create("LintuB", "TaxonB")
        #
        # def _delete_individuals(self, inds):
        #     for i in inds:
        #         i.delete()
