from django.test import TestCase
from papukaaniApp.models_LajiStore import individual, device, document, gathering


class TestIndividual(TestCase):
    def setUp(self):
        indiv = {
            "nickname": "Lintuli",
            "taxon": "test test"
        }
        indiv2 = {
            "nickname": "Varpuli",
            "taxon": "test test2"
        }

        self.ind = individual.create(**indiv)
        self.ind2 = individual.create(**indiv2)

    def tearDown(self):
        self.ind.delete()
        self.ind2.delete()

    def test_find(self):
        self.assertGreater(individual.find(deleted=self.ind.deleted).__len__(), 0)

    def test_get_all(self):
        individuals = individual.find()
        self.assertGreater(individuals.__len__(), 0)

    def test_get(self):
        self.assertEquals(self.ind.id, individual.get(self.ind.id).id)

    def test_create(self):
        self.assertEquals("Lintuli", self.ind.nickname)
        self.assertEquals("test test", self.ind.taxon)

    def test_get_gatherings(self):
        dev = device.create("Type", "Manu", "DeviceId", "2000-02-02T20:20:20+00:00", "2000-02-02T20:20:20+00:00")
        document.create(
            [gathering.Gathering("2012-01-01T00:00:00+00:00", [10.0, 10.0], publicityRestrictions="MZ.publicityRestrictionsPublic"),
             gathering.Gathering("2013-02-02T00:00:00+00:00", [11.0, 11.0], publicityRestrictions="MZ.publicityRestrictionsPublic"),
             gathering.Gathering("2013-02-02T00:00:00+00:00", [10.0, 10.0], publicityRestrictions="MZ.publicityRestrictionsPrivate")],
            dev.id)

        dev.attach_to(self.ind.id, "2013-01-01T00:00:00+00:00")

        gatherings = self.ind.get_gatherings()

        self.assertEquals(1, len(gatherings))
