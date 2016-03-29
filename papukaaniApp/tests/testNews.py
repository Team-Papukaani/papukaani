from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from papukaaniApp.models_LajiStore import news, individual
from papukaaniApp.models import *
from datetime import datetime
import json

_URL = '/papukaani/news/'


class TestNews(TestCase):
    def setUp(self):
        self.c = Client()
        self.A = news.create('title', 'test', 'fi')
        self.B = news.create('title2', 'test2', 'en', None, [1])

    def tearDown(self):
        news.delete_all()

    def test_post(self):
        postdata = {
            "content": "p>test</p>",
            "language": "en",
            "targets": [],
            "publishDate": "2016-03-01T00:00:00+00:00",
            "title": "test3"
        }
        response = self.c.post(_URL, postdata)

        self.assertEquals(len(news.find()), 3)

    def test_post_with_bad_date(self):
        postdata = {
            "content": "p>test</p>",
            "language": "en",
            "targets": [],
            "publishDate": "532452345",
            "title": "test3"
        }
        response = self.c.post(_URL, postdata)

        self.assertEquals(len(news.find()), 2)

    def test_post_with_bad_title(self):
        postdata = {
            "content": "p>test</p>",
            "language": "en",
            "title": ""
        }
        response = self.c.post(_URL, postdata)

        self.assertEquals(len(news.find()), 2)

    def test_post_with_bad_content(self):
        postdata = {
            "content": "",
            "language": "en",
            "title": "test"
        }
        response = self.c.post(_URL, postdata)

        self.assertEquals(len(news.find()), 2)

    def test_post_with_targets(self):
        I = individual.create("test", "test")
        I2 = individual.create("test", "test")
        targets = []
        targets.append(I.id)
        targets.append(I2.id)
        postdata = {
            "content": "p>test</p>",
            "language": "en",
            "targets": json.dumps(targets),
            "publishDate": "2016-3-1",
            "title": "test3"
        }
        response = self.c.post(_URL, postdata)

        self.assertEquals(len(news.find()), 3)

    def test_delete(self):
        response = self.c.delete(_URL + self.A.id)
        self.assertEquals(len(news.find()), 1)

    def test_list(self):
        response = self.c.get(_URL + "list")
        self.assertTrue("title2" in str(response.content))

    def test_read(self):
        response = self.c.get(_URL + self.A.id)
        self.assertTrue("title" in str(response.content))
        self.assertTrue("test" in str(response.content))
        self.assertTrue("fi" in str(response.content))

    def test_post_with_targets(self):
        I = individual.create("test", "test")
        I2 = individual.create("test", "test")
        targets = []
        targets.append(I.id)
        targets.append(I2.id)
        postdata = {
            "content": "p>test</p>",
            "language": "en",
            "targets": json.dumps(targets),
            "publishDate": "2016-3-1",
            "title": "test3"
        }
        response = self.c.post(_URL, postdata)
        self.assertEquals(len(news.find()), 3)

    def test_bad_targets(self):
        postdata = {
            "content": "p>test</p>",
            "language": "en",
            "targets": "12345645",
            "publishDate": "2016-3-1",
            "title": "test3"
        }
        response = self.c.post(_URL, postdata)
        self.assertEquals(len(news.find()), 2)

    def test_bad_targets2(self):
        postdata = {
            "content": "p>test</p>",
            "language": "en",
            "targets": "",
            "publishDate": "2016-3-1",
            "title": "test3"
        }
        response = self.c.post(_URL, postdata)
        self.assertEquals(len(news.find()), 2)

    def test_bad_targets2(self):
        postdata = {
            "content": "p>test</p>",
            "language": "en",
            "targets": " 12341234,12341234",
            "publishDate": "2016-3-1",
            "title": "test3"
        }
        response = self.c.post(_URL, postdata)
        self.assertEquals(len(news.find()), 2)
