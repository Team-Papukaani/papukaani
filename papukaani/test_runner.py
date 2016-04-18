from django.core.cache import caches
from django.test.runner import DiscoverRunner
from papukaaniApp.models_LajiStore import *
from papukaaniApp.services.deviceindividual_service import DeviceIndividual


class TestRunner(DiscoverRunner):
    def teardown_databases(self, old_config, **kwargs):
        self.clear_db()
        self.clear_caches()

    def setup_databases(self, **kwargs):
        self.clear_db()
        self.clear_caches()

    def clear_db(self):
        document.delete_all()
        device.delete_all()
        individual.delete_all()
        DeviceIndividual.delete_all()
        news.delete_all()

    def clear_caches(self):
        try:
            caches['public'].clear()
        except:
            pass
        try:
            caches['routes'].clear()
        except:
            pass
        try:
            caches['default'].clear()
        except:
            pass
