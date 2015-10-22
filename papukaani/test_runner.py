
from django.test.runner import DiscoverRunner
from papukaaniApp.models_LajiStore import *

class TestRunner(DiscoverRunner):

    def teardown_databases(self, old_config, **kwargs):
        self.clear_db()

    def setup_databases(self, **kwargs):
        self.clear_db()

    def clear_db(self):
        document.delete_all()
        device.delete_all()
        individual.delete_all()
