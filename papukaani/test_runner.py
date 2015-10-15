
from django.test.runner import DiscoverRunner
from papukaaniApp.models_LajiStore import *

class TestRunner(DiscoverRunner):

    def teardown_databases(self, old_config, **kwargs):
        document.delete_all()
        device.delete_all()
        individual.delete_all()