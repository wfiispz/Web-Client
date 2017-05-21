from django.test import TestCase
from .models import *
from .Connector import *
from unittest import mock
from urllib.parse import urljoin

url_local = 'https://www.example.com/'
url_resources = 'https://www.example.com/resources/'
url_measurements = 'https://www.example.com/measurements/'

mock_json_resources = '{"resources": [{"id": "a20eec48-b949-4cb6-ba21-86c61b6ba282","name": "pz_lap","description": "pz_laptop","measurements": ["http://example.com/measurements/61c7524a-84da-4aef-a14b-38f0ad87e08f","http://example.com/measurements/fe274228-c241-4b9c-9784-b38e16813f61"]}], "page": {"size": "100","number": "1","totalCount": "1"}}'
mock_resource = '{"id" : "a20eec48-b949-4cb6-ba21-86c61b6ba282","name" : "pz_lap","description" : "pz_laptop","measurements": ["http://example.com/measurements/61c7524a-84da-4aef-a14b-38f0ad87e08f","http://example.com/measurements/fe274228-c241-4b9c-9784-b38e16813f61"]}'
mock_json_measurements = '{"measurements": [{"host": "https://www.example.com/resources/a20eec48-b949-4cb6-ba21-86c61b6ba282","metric": "MemoryUsage","unit": "Megabytes","complex": false,"maxValue": 8173,"values": "http://example.com/measurements/61c7524a-84da-4aef-a14b-38f0ad87e08f/values"}]"page": {"size":"1","number":"2","totalCount":"5"}}'
mock_measure = '{"host": "http://www.example.com/resources/a20eec48-b949-4cb6-ba21-86c61b6ba282","metric": "MemoryUsage","unit": "Megabytes","complex": false,"maxValue": 8173,"values": "http://www.example.com/measurements/61c7524a-84da-4aef-a14b-38f0ad87e08f/values"}'

guid = 'a20eec48-b949-4cb6-ba21-86c61b6ba282'
measure_guid = '61c7524a-84da-4aef-a14b-38f0ad87e08f'
endpoints = '["http://www.example.com/measurements/61c7524a-84da-4aef-a14b-38f0ad87e08f", "http://www.example.com/measurements/fe274228-c241-4b9c-9784-b38e16813f61"]'
endpoint = 'http://www.example.com/measurements/61c7524a-84da-4aef-a14b-38f0ad87e08f'
values = '{"values" : [{"value":"1231","datetime":"2009-06-15T13:45:00"},{"value":"13","datetime":"2009-06-15T13:46:00"}]}'

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
        self.text = str(json_data)

    def json(self):
        return self.json_data

def mocked_requests_get(*args, **kwargs):
    if args[0] == url_resources:
        return MockResponse(mock_json_resources, 200)
    elif args[0] == urljoin(url_resources, guid):
        return MockResponse(mock_resource, 200)
    elif args[0] == url_measurements:
        return MockResponse(mock_json_measurements, 200)
    elif args[0] == endpoint:
        return MockResponse(mock_measure, 200)
    return MockResponse(None, 404)

class ConnectorTests(TestCase):

    def test_initialization(self):
        print("Tests if object belongs to Connector class")
        con = Connector(url_local)
        self.assertIsInstance(con, Connector)

    def test_empty_url(self):
        print("Tests if url is empty")
        con = Connector('')
        self.assertEqual(con._url_adr, '')

    def test_not_empty_url(self):
        print("Tests if string given as an argument of Connector init method is not empty url")
        con = Connector(url_local)
        self.assertEqual(con._url_adr, url_local)

    def test_payload_empty(self):
        print("Tests if payload is empty")
        con = Connector(url_local)
        self.assertFalse(con.payload)

    def test_payload_not_empty(self):
        print("Tests if payload is not empty")
        con = Connector(url_local)
        con.payload = {'key': 'value'}
        self.assertTrue(con.payload)

    def test_set_payload(self):
        print("Tests if payload is set porperly")
        con = Connector(url_local)
        con.payload = {'key': 'value'}
        self.assertEqual(con.payload, {'key': 'value'})

    def test_get_payload(self):
        print("Test does payload returns good values")
        con = Connector(url_local)
        con.payload = {'key': 'value'}
        self.assertEqual({'key': 'value'}, con.payload)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_resources_id(self, mock_get):
        print("Tests if resources list is not empty")
        connector = Connector(url_resources)
        self.assertTrue(len(connector.get_resources()) > 0)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_resource(self, mock_get):
        print("Test if get_resource returns resource")
        connector = Connector(url_resources)
        self.assertTrue(connector.get_resource_id(guid))

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_is_get_resource_instance_of_resources(self, mock_get):
        print("Tests if get_resource returns Resources object")
        connector = Connector(url_resources)
        self.assertIsInstance(connector.get_resource_id(guid), Resources)

    def test_delete_resources(self):
        print("Tests if delete_resources works good")
        con = Connector(url_resources)
        self.assertEquals(404, con.delete_resource(guid))

    # @mock.patch('requests.get', side_effect=mocked_requests_get)
    # def test_get_measurements(self, mock_get):
    #     print("Tests does get_measurements returns not empty list of measurements")
    #     con = Connector(url_measurements)
    #     self.assertTrue(len(con.get_measurements(endpoints) > 0))

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_measurement(self, mock_get):
        print("Tests does get_measurement returns measurement")
        connector = Connector(url_measurements)
        self.assertTrue(connector.get_measurement(endpoint))

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_is_get_measurement_instance_of_measurements(self, mock_get):
        print("Tests if get_measurement returns Resources object")
        connector = Connector(url_measurements)
        self.assertIsInstance(connector.get_measurement(endpoint), Measurements)

    # @mock.patch('requests.get', side_effect=mocked_requests_get)
    # def test_get_measurement_values(self, mock_get):
    #     print("Tests if get_measurement_values returns proper values - empty list")
    #     connector = Connector(endpoint2)
    #     self.assertTrue(len(connector.get_measurement_values(endpoint2)) == 0)

    def test_delete_measurement_values(self):
        print("Tests if delete_measuremnt_values returns empty json")
        con = Connector(url_measurements)
        self.assertEqual(404, con.delete_measurement_values(measure_guid))

    def test_post_measurements(self):
        print("Tests post_measurements method")
        con = Connector(url_measurements)
        con.payload = {'key' : 'value'}
        self.assertEqual(404, con.post_measurements())

    def test_delete_measurement(self):
        print("Tests delete_measurement")
        con = Connector(url_measurements)
        self.assertEquals(404, con.delete_measurement(measure_guid))