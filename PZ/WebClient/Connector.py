import requests
import json
from urllib.parse import urljoin
from .models import *


class Connector(object):
    def __init__(self, url_adr):
        self._url_adr = url_adr
        self._response = None
        self._json_data = None
        self._payload = {}

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, payload):
        self._payload = payload

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def get_resources(self):
        resources_list = []
        self._response = requests.get(self._url_adr, params=self._payload)
        self._json_data = json.loads(self._response.text)

        for item in self._json_data['resources']:
            resources_list.append(Resources(resource_id=item['id'], name=item['name'], description=item['description'],
                                            measurements=item['measurements']))

        page = Page(size=self._json_data['page']['number'], number=self._json_data['page']['totalCount'],
                    total_count=self._json_data['page']['size'])
        return resources_list, page

    def get_resource_id(self, guid):
        self._response = requests.get(urljoin(self._url_adr, guid))
        self._json_data = json.loads(self._response.text)
        return Resources(resource_id=self._json_data['id'], name=self._json_data['name'],
                         description=self._json_data['description'], measurements=self._json_data['measurements'])

    def delete_resource(self, guid):
        self._response = requests.delete(urljoin(self._url_adr, guid))
        self._json_data = json.loads(self._response.text)
        return self._json_data

    def get_measurements(self, endpoints):
        measurements_list = []

        endpoints_data = json.loads(endpoints)
        for endpoint in endpoints_data:
            measurements_list.append(self.get_measurement(endpoint))

        #page = Page(size=self._json_data['page']['number'], number=self._json_data['page']['totalCount'],
        #            total_count=self._json_data['page']['size'])
        return measurements_list

    def get_measurement(self, endpoint):
        self._response = requests.get(endpoint)
        self._json_data = json.loads(self._response.text)
        return Measurements(host=self._json_data['host'], metric=self._json_data['metric'],
                            unit=self._json_data['unit'], max_value=self._json_data['maxValue'],
                            complex_mes=self._json_data['complex'], values=self._json_data['values'])

    def get_measurement_values(self, endpoint):
        values = []
        print(endpoint + '/values')
        self._response = requests.get(endpoint + '/values', params=self._payload)
        self._json_data = json.loads(self._response.text)

        print(self._json_data)

        for item in self._json_data['values']:
            values.append(Values(value=item['value'], datetime=item['timestamp']))

        return values

    def delete_measurement_values(self, guid):
        self._response = requests.delete(urljoin(self._url_adr, guid + 'values'))
        self._json_data = json.loads(self._response.text)
        return self._json_data

    def post_measurements(self):
        self._response = requests.post(self._url_adr, data=json.dumps(self._payload))

    def delete_measurement(self, guid):
        self._response = requests.delete(urljoin(self._url_adr, guid))
