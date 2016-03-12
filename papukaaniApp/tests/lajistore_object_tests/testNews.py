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
        individual.delete_all()

    def test_create(self):
        self.assertEquals("Good News!", self.n.title)
        self.assertEquals("newsnewsnews", self.n.content)
        self.assertEquals("en", self.n.language)
        self.assertEquals(set(), self.n.targets)

    def test_get_nonexisting(self):
        self.assertEquals(None, news.get(0))

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
            "title": "notempty",
            "content": "notempty",
            "language": "sv"
        }

        news.create(**new)
        self.assertEquals(len(news.find()), 2)

    def test_update_badly(self):
        with self.assertRaises(ValueError):
            self.n.title = ""
            self.n.update()

        with self.assertRaises(ValueError):
            self.n.language = ""
            self.n.update()

        with self.assertRaises(ValueError):
            self.n.content = ""
            self.n.update()

    def test_publishedDate(self):
        self.assertEquals(None, self.n.publishDate)
        gotten = news.get(self.n.id)
        self.assertEquals(None, gotten.publishDate)

        t = "2016-01-01T01:02:03+00:00"
        self.n.publishDate = t
        self.n.update()
        gotten = news.get(self.n.id)
        self.assertEquals(t, gotten.publishDate)

        with self.assertRaises(ValueError):
            self.n.publishDate = "I'm not a valid time"
            self.n.update()

    def test_getting_attached_is_empty(self):
        self.assertEqual(set(), self.n.get_attached_individuals())

    def test_is_attached_when_not_attached(self):
        self.assertFalse(self.n.is_attached())

    def test_delete(self):
        self.n.delete()
        self.assertIsNone(news.get(self.n.id))

    def test_attach(self):
        A, B = self._create_individuals()
        self.n.attach_to(A.id.rsplit('/', 1)[-1])
        self.assertEquals(len(self.n.get_attached_individuals()), 1)
        self.n.attach_to(B.id.rsplit('/', 1)[-1])
        self.assertEquals(len(self.n.get_attached_individuals()), 2)
        self.assertTrue(self.n.is_attached())

    def test_detach(self):
        A, B = self._create_individuals()
        self.n.attach_to(A.id)
        self.n.attach_to(B.id)
        self.assertEquals(len(self.n.get_attached_individuals()), 2)
        self.assertTrue(self.n.is_attached())

        self.assertTrue(self.n.detach_from(A.id))
        birds = list(self.n.get_attached_individuals())
        self.assertEquals(len(birds), 1)
        self.assertTrue(self.n.is_attached())
        self.assertEquals(birds[0], B.id)

        self.n.detach_from(B.id)
        self.assertFalse(self.n.is_attached())

    def test_attach_and_detach_actually_update_lajistore(self):
        A, B = self._create_individuals()
        self.n.attach_to(A.id)
        self.assertEquals(1, len(news.get(self.n.id).targets))
        self.n.detach_from(A.id)
        self.assertEquals(0, len(news.get(self.n.id).targets))

    def test_dont_allow_multiples_of_same_individual(self):
        A, B = self._create_individuals()
        self.assertTrue(self.n.attach_to(A.id))
        self.assertTrue(self.n.attach_to(A.id))
        self.assertEquals(len(self.n.get_attached_individuals()), 1)

    def test_dont_mess_up_removing_nonexisting_individuals(self):
        A, B = self._create_individuals()
        self.n.attach_to(A.id)
        self.assertFalse(self.n.detach_from(B.id))
        birds = list(self.n.get_attached_individuals())
        self.assertEquals(len(birds), 1)
        self.assertEquals(birds[0], A.id)

    def test_dont_add_nonexisting_birds(self):
        A, B = self._create_individuals()
        A.deleted = True
        A.update()
        self.assertFalse(self.n.attach_to(A.id))
        B.delete()
        self.assertFalse(self.n.attach_to(B.id))

    def test_detach_removes_nonexisting_birds(self):
        A, B = self._create_individuals()
        self.assertTrue(self.n.attach_to(A.id))
        self.assertTrue(self.n.attach_to(B.id))
        A.deleted = True
        A.update()
        self.assertTrue(self.n.detach_from(B.id))
        self.assertEquals(0, len(self.n.targets))

    def _create_individuals(self):
        return individual.create("LintuA", "TaxonA"), individual.create("LintuB", "TaxonB")
