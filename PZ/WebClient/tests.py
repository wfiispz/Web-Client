from django.test import TestCase
from .models import *
from .Connector import *

# Create your tests here.
url_local = 'http://localhost:8002/'
url_resources = 'http://localhost:8002/resources/'
url_measurements = 'http://localhost:8002/measurements/'

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

    def test_get_resources(self):
        print("Tests if get_resources returns not empty list of resources")
        con = Connector(url_resources)
        self.assertTrue(len(con.get_resources())>0)

    def test_get_resource(self):
        print("Test if get_resource returns resource")
        con = Connector(url_resources)
        self.assertTrue(con.get_resource_id('a20eec48-b949-4cb6-ba21-86c61b6ba282'))

    def test_is_get_resource_instance_of_resources(self):
        print("Tests if get_resource returns Resources object")
        con = Connector(url_resources)
        self.assertIsInstance(con.get_resource_id('a20eec48-b949-4cb6-ba21-86c61b6ba282'), Resources)

    def test_delete_resources(self):
        print("Tests if delete_resources works good")
        con = Connector(url_resources)
        self.assertTrue(con.delete_resource('a20eec48-b949-4cb6-ba21-86c61b6ba282'))

    def test_get_measurements(self):
        print("Tests does get_measurements returns not empty list of measurements")
        con = Connector(url_measurements)
        self.assertTrue(len(con.get_measurements('["http://localhost:8002/measurements/61c7524a-84da-4aef-a14b-38f0ad87e08f","http://localhost:8002/measurements/fe274228-c241-4b9c-9784-b38e16813f61"]')) > 0)

    def test_get_measurement(self):
        print("Tests does get_measurement returns resource")
        con = Connector(url_measurements)
        self.assertTrue(con.get_measurement('http://localhost:8002/measurements/61c7524a-84da-4aef-a14b-38f0ad87e08f'))

    def test_is_get_resource_instance_of_measurements(self):
        print("Tests if get_measurement returns Resources object")
        con = Connector(url_measurements)
        self.assertIsInstance(con.get_measurement('http://localhost:8002/measurements/61c7524a-84da-4aef-a14b-38f0ad87e08f'), Measurements)

    def test_get_measurement_values(self):
        print("Tests if get_measurement_values returns proper values - empty list")
        con = Connector(url_measurements)
        self.assertTrue(len(con.get_measurement_values('http://localhost:8002/measurements/61c7524a-84da-4aef-a14b-38f0ad87e08f')) == 0)

    def test_delete_measurement_values(self):
        print("Tests if delete_measuremnt_values returns empty json")
        con = Connector(url_measurements)
        self.assertNotEqual(None, con.delete_measurement_values('61c7524a-84da-4aef-a14b-38f0ad87e08f'))

    def test_post_measurements(self):
        print("Tests post_measurements method")
        con = Connector(url_measurements)
        con.payload = {'key' : 'value'}
        self.assertEqual(None, con.post_measurements())

    def test_delete_measurement(self):
        print("Tests delete_measurement_")
        con = Connector(url_measurements)
        self.assertEquals(None,con.delete_measurement('61c7524a-84da-4aef-a14b-38f0ad87e08f'))