import requests
import json

from .models import *

class Connector(object):
    def __init__(self, url_adr):
        self.url_adr = url_adr
        self.response = None
        self.json_data = None
        self.payload = {}

    def set_url(self, url_adr):
        self.url_adr = url_adr

    def set_request_args(self, payload):
        self.payload = payload

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def get_resources(self):
        resources_list = []
        self.response = requests.get(self.url_adr, params=self.payload)
        self.json_data = json.loads(self.response.text)

        for item in self.json_data['resources']:
            resources_list.append(Resources(resource_id=item['id'], name=item['name'], description=item['description'],
                                            measurements=item['measurements']))

        page = Page(size=self.json_data['page']['number'], number=self.json_data['page']['totalCount'],
                    total_count=self.json_data['page']['size'])
        return [resources_list, page]

    def get_resource_by_id(self, rid):
        self.url_adr += rid
        self.response = requests.get(self.url_adr)
        self.json_data = json.loads(self.response.text)
        return Resources(id=self.json_data['id'], name=self.json_data['name'], description=self.json_data['description']
                         , measurements=self.json_data['measurements'])

    def delete_resource(self, rid):
        self.url_adr += rid
        self.response = requests.delete(self.url_adr)
        self.json_data = json.loads(self.response.text)
        return self.json_data

    def get_measurements(self):
        measurements_list = []
        self.response = requests.get(self.url_adr, params=self.payload)
        self.json_data = json.loads(self.response.text)

        for item in self.json_data['measurements']:
            measurements_list.append(Measurements(host=item['host'], metric=item['metric'], unit=item['unit'],
                                                  max_value=item['maxValue'], complex_mes=item['complex'],
                                                  values=item['values']))

        page = Page(size=self.json_data['page']['number'], number=self.json_data['page']['totalCount'],
                    total_count=self.json_data['page']['size'])
        return [measurements_list, page]

    def get_measurements_guid(self, guid):
        self.url_adr += guid
        self.response = requests.get(self.url_adr)
        self.json_data = json.loads(self.response.text)
        return Measurements(host=self.json_data['host'], metric=self.json_data['metric'], unit=self.json_data['unit'],
                            max_value=self.json_data['maxValue'], complex_mes=self.json_data['complex'],
                            values=self.json_data['values'])

    def get_measurements_guid_values(self, guid):
        values = []
        self.url_adr += (guid+'/values')
        self.response = requests.get(self.url_adr, params=self.payload)
        self.json_data = json.loads(self.response.text)

        for item in self.json_data['values']:
            values.append(Values(value=item['value'], datetime=item['datetime']))

        return values

    def delete_measurements_guid_values(self, guid):
        self.url_adr += guid+"/values"
        self.response = requests.delete(self.url_adr)
        self.json_data = json.loads(self.response.text)
        return self.json_data

    def post_measurements(self):
        self.response = requests.post(self.url_adr, data=json.dumps(self.payload))

    def delete_measurements_guid(self, guid):
        self.url_adr += guid+"/"
        self.response = requests.delete(self.url_adr)
        self.json_data = json.loads(self.response.text)
        return self.json_data
