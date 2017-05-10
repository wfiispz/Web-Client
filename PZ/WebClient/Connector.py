from .models import *


class Connector(object):
    def __init__(self, resources, page):
        self.resources = resources
        self.page = page

    def get_resources(self, obj):
        return self.resources

    def get_resource_by_id(self, rid):
        pass

    def delete_resource(self, rid):
        return "Resources with id = "+str(rid)+" deleted."

    def get_measurements(self, resources):
        return self.resources.measurements

    def get_measurements_guid(self, guid):
        pass

    def get_measurements_guid_values(self, guid, values):
        pass

    def delete_measurements_guid_values(self, guid, values):
        return "Deleted all measurements for ona resource"


    # def post_measurements(self, obj):
    #     pass
    #
    # def delete_measurements(self, rid):
    #     return "Measurements with id = "+str(rid)+" deleted."
    #


def main():
    connector = Connector()


if __name__ == "__main__":
    main()
