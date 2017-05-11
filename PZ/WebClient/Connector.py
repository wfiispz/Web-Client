import requests
import json

# from PZ.WebClient.models import *


class Connector(object):
    def __init__(self, url_adr):
        self.url_adr = url_adr
        self.response = object()
        self.json_data = object()
        self.payload = {}

    def set_url(self, url_adr):
        self.url_adr = url_adr

    def set_request_args(self, payload):
        self.payload = payload

    def get_resources(self):
        resources_list = []
        resource = None
        page = None
        self.response = requests.get(self.url_adr, params=self.payload)
        self.json_data = json.loads(self.response.text)

        # for item in self.json_data['resources']:
        # print(self.json_data['page'])
        for item in self.json_data['resources']:
            # resource = Resources()
            # resource.id = item['id']
            # resource.name = item['name']
            # resource.description = item['description']
            # resource.measurements = item['measurements']
            # resources_list.append(resource)
            # test line ****************************************
            resources_list.append((item['id'], item['name'], item['description'], item['measurements']))

        print(self.json_data['page']['number'], self.json_data['page']['totalCount'], self.json_data['page']['size'])
        # page.size = self.json_data['page']['number']
        # page.number = self.json_data['page']['totalCount']
        # page.total_count = self.json_data['page']['size']

        return [resources_list, page]


    def get_resource_by_id(self, rid):
        self.url_adr += rid
        self.response = requests.get(self.url_adr)
        self.json_data = json.loads(self.response.text)
        # resource = Resources()
        # resource.id = self.request['id']
        # resource.name = self.request['name']
        # resource.description = self.request['description']
        # resource.measurements = self.request['measurements']
        # return resource


    def delete_resource(self, rid):
        self.url_adr += rid
        self.response = requests.delete(self.url_adr)
        # self.json_data = json.loads(self.response.text)

    def get_measurements(self):
        measurements_list = []
        measurement = None
        page = None
        self.response = requests.get(self.url_adr, params=self.payload)
        self.json_data = json.loads(self.response.text)

        # for item in self.json_data['resources']:
        # print(self.json_data['page'])
        for item in self.json_data['measurements']:
            # measurement = Measurements()
            # measurement.host = item['host']
            # measurement.metric = item['metric']
            # measurement.unit = item['unit']
            # measurement.max_value = item['maxValue']
            # measurement.complex_mes = item['complex']
            # measurement.values = item['values']
            # resources_list.append(resource)
            # test line ****************************************
            measurements_list.append((item['host'], item['metric'], item['unit'], item['maxValue'], item['complex'], item['values']))

        print(self.json_data['page']['number'], self.json_data['page']['totalCount'], self.json_data['page']['size'])
        # page.size = self.json_data['page']['number']
        # page.number = self.json_data['page']['totalCount']
        # page.total_count = self.json_data['page']['size']

        return [measurements_list, page]

    def get_measurements_guid(self, guid):
        self.url_adr += guid
        self.response = requests.get(self.url_adr)
        self.json_data = json.loads(self.response.text)
        # measurement = Measurements()
        # measurement.host = item['host']
        # measurement.metric = item['metric']
        # measurement.unit = item['unit']
        # measurement.max_value = item['maxValue']
        # measurement.complex_mes = item['complex']
        # measurement.values = item['values']
        # return measurement

    def get_measurements_guid_values(self, guid):
        values = []
        self.url_adr += (guid+'/')
        self.response = requests.get(self.url_adr, params=self.payload)
        self.json_data = json.loads(self.response.text)
        return self.json_data
        # return values

    def delete_measurements_guid_values(self, guid):
        self.url_adr += guid+"/values"
        # print(self.url_adr)
        self.response = requests.delete(self.url_adr)

    def post_measurements(self):
        #post with json
        self.response = requests.post(self.url_adr, data=json.dumps(self.payload))


    def delete_measurements_guid(self, guid):
        self.url_adr += guid+"/"
        self.response = requests.delete(self.url_adr)

# testowanie
# def main():
#     # r = requests.request('GET', 'http://localhost:8000/resources/')
#     # print(r.text)
#     # connector = Connector()
#     connector = Connector('http://localhost:8000/resources/')
#     conn2 = Connector('http://localhost:8000/measurements/')
#     # print(conn2.get_measurements())
#     # print(connector.get_resource_by_id('571ccc31-9efa-452b-b19a-12d8703774bc'))
#     # print(connector.get_resourcaes())
#     # print(conn2.delete_measurements_guid_values('fe274228-c241-4b9c-9784-b38e16813f61'))
#
# if __name__ == "__main__":
#     main()
