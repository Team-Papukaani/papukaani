from django.test import TestCase
from papukaaniApp.models_LajiStore import individual,device,document, gathering


class TestIndividual(TestCase):
    def setUp(self):
        indiv = {
                    self.id = id
        self.nickname = nickname
        self.taxon = taxon
        self.ringID = ringID
        self.deleted = deleted
            "taxon": "test test"
        }
        indiv2 = {
            "taxon": "test test2"
        }

        self.ind = individual.create(**indiv)
        self.ind2 = individual.create(**indiv2)

    def tearDown(self):
        self.ind.delete()
        self.ind2.delete()

    def test_find(self):
        self.assertGreater(individual.find(individualId=self.ind.individualId).__len__(), 0)  # simple test because LajiStore not ready

    def test_get_all(self):
        individuals = individual.get_all()
        self.assertGreater(individuals.__len__(), 0)

    def test_get(self):
        self.assertEquals(self.ind.individualId, individual.get(self.ind.id).individualId)

    def test_create(self):
        self.assertEquals(self.ind.individualId, self.ind.individualId)
        self.assertEquals("test test", self.ind.taxon)

    def test_get_gatherings(self):
        dev = device.create("DeviceId", "Type", "Manu", "2000-02-02T20:20:20+00:00", "2000-02-02T20:20:20+00:00")
        doc = document.create("DocumentId", [gathering.Gathering("2012-01-01T00:00:00+00:00", [10.0, 10.0], publicity="public"),
                                             gathering.Gathering("2013-02-02T00:00:00+00:00", [11.0, 11.0], publicity="public"),
                                             gathering.Gathering("2013-02-02T00:00:00+00:00", [10.0, 10.0], publicity="private")], "DeviceId")

        dev.attach_to(self.ind, "2013-01-01T00:00:00+00:00")
        dev.update()

        gatherings = self.ind.get_gatherings()

        self.assertEquals(1, len(gatherings))

