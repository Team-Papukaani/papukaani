testOk = False

_device = {
    "id": 0,
    "deviceId": "ABCD1234567",
    "deviceType": "Type",
    "deviceManufacturer": "Manufacturer",
    "createdAt": "2015-09-29T14:00:00+03:00",
    "createdBy": "SomeUser",
    "lastModifiedAt": "2015-09-29T14:00:00+03:00",
    "lastModifiedBy": "SomeUser",
    "facts": []

}

_document = {
    "id": 2,
    "lastModifiedAt": "2015-09-15T11:25:58+03:00",
    "lastModifiedBy": "SomeUser",
    "documentId": "ABCDTESTTEST",

    "createdAt": "2015-09-15T11:25:58+03:00",
    "createdBy": "SomeUser",
    "facts": [],
    "gatherings": [],
}

_individual = {
    "id": 3,
    "individualId": "INDIVIDUALABCD",
    "taxon": "test test"
}


def get_all_devices(**kwargs):
    return [_device]


def get_device(id):
    d = _device.copy()
    d.id = id
    return d


def post_device(**kwargs):
    kwargs['id'] = 1
    return kwargs


def update_device(**kwargs):
    return kwargs


def get_all_documents(**kwargs):
    return [_document]


def get_document(id):
    d = _document.copy()
    d.id = id
    return d


def post_document(**kwargs):
    kwargs['id'] = 1
    return kwargs


def update_document(**kwargs):
    return kwargs


def get_all_individuals(**kwargs):
    return [_individual]


def get_individual(id):
    d = _individual.copy()
    d.id = id
    return d


def post_individual(**kwargs):
    kwargs['id'] = 1
    return kwargs


def update_individual(**kwargs):
    return kwargs
