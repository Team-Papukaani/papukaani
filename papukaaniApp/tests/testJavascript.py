from django.test import TestCase
import subprocess


class TestChoose(TestCase):

    def test_javascript_unit_tests(self):
        self.assertEqual(0, subprocess.call('jasmine-ci', shell=True))
