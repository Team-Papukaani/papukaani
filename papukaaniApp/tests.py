from django.test import TestCase
from django.test import Client


class FileUploadTest(TestCase):

    def test_get_to_index_returns_200(self):
         c = Client()
         response = c.get('/papukaani/')
         self.assertTrue(response.status_code == 200)

    def test_post_to_index_returns_200(self):
        c = Client()
        response = c.get('/papukaani/')
        self.assertTrue(response.status_code == 200)

