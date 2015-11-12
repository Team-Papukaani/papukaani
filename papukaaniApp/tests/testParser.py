from papukaaniApp.utils.parser import *
from django.test import TestCase
from django.conf import settings
from papukaaniApp.models_LajiStore import document, gathering


class FileParserTest(TestCase):
    def tearDown(self):
        document.delete_all()


    def test_create_points_method_correctly_updates_existing_documents(self):
        _create_points_from_ecotone("/Ecotones_gps_pos_doc_create_test.csv")
        _create_points_from_ecotone("/Ecotones_gps_pos_doc_create_test2.csv")
        assert len(document.get_all()) == 3

    def test_merge_and_delete_if_three_documents_found_for_same_device(self):

        gatherings = [gathering.Gathering("2015-09-15T08:00:00+03:00", [68.93023632, 23.19298104])]
        dict = {
            "documentId": "TestId0000001",
            "deviceId" : "48500691564",
            "createdAt":"2015-09-14T15:29:28+03:00",
            "lastModifiedAt":"2015-09-14T15:29:28+03:00",
            "facts": [],
            "gatherings": gatherings
            }
        document.create(**dict)
        document.create(**dict)
        document.create(**dict)
        assert len(document.get_all()) == 3

        _create_points_from_ecotone("/Ecotones_gps_pos_test.csv")
        assert len(document.get_all()) == 1

    def test_document_does_not_contain_duplicate_gathering(self):
        _create_points_from_ecotone("/Ecotones_gps_pos_gathering_duplicate_test.csv")
        _create_points_from_ecotone("/Ecotones_gps_pos_gathering_duplicate_test2.csv")
        documents = document.get_all()
        self.assertEqual(len(documents[0].gatherings), 1)

    def test_byholm_data_goes_lajiStroe_succesfully(self):
        path = settings.OTHER_ROOT + "/byholm_test.txt"
        file = open(path, "rb")
        entries = prepare_file(file, "byholm")
        create_points(entries, "byholm")
        documents = document.get_all()
        self.assertEqual(len(documents), 1)
        self.assertEqual(len(documents[0].gatherings), 5)


def _create_points_from_ecotone(filename):
        path = settings.OTHER_ROOT + filename
        file = open(path, "rb")
        entries = prepare_file(file, "ecotone")
        create_points(entries, "ecotone")
