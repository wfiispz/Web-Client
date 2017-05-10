from django.db import models
from django.contrib.auth.models import User


class Monitors(models.Model):
    monitor_name = models.CharField(max_length=200)
    monitor_domain = models.URLField()
    user_id = models.ForeignKey(User)


class Page(object):
	def __init__(self, size, number, totalCount):
		# self.dict = json.loads(json_obj)
		self.size = size
		self.number = number
		self.totalCount = totalCount

	def set_size(self, size):
		self.size = size
	
	def set_number(self, number):
		self.number = number
	
	def set_totalcount(self, totalCount):
		self.totalCount = totalCount

	def get_size(self):
		return self.size

	def get_number(self):
		return self.number

	def get_totalcount(self):
		return self.totalCount


class Measurements(object):
	# mcomplex because comples is preserved
	def __init__(self, host, metric, unit, maxValue, mcomplex, values):
		self.host = host
		self.metric = metric
		self.unit = unit
		self.maxValue = maxValue
		self.complex = mcomplex
		self.values = values

	def set_host(self, host):
		self.host = host

	def set_metric(self, metric):
		self.metric = metric

	def set_unit(self, unit):
		self.unit = unit

	def set_maxvalue(self, maxValue):
		self.maxValue = maxValue

	def set_complex(self, mcomplex):
		self.complex = mcomplex

	def set_values(self, values):
		self.values = values

	def get_host(self):
		return self.host

	def get_metric(self):
		return self.metric

	def get_unit(self):
		return self.unit

	def get_maxvalue(self):
		return self.maxValue

	def get_complex(self):
		return self.complex

	def get_values(self):
		return self.values


class Values(object):
	def __init__(self, value, datetime):
		self.value = value
		self.datetime = datetime

	def set_value(self,value):
		self.value = value

	def set_datetime(self, datetime):
		self.datetime = datetime

	def get_value(self):
		return self.value

	def get_datetime(self):
		return self.datetime


class Resources(object):
	# rid because id is preserved
	def __init__(self, rid, name, description, measurements):
		# self.dict = json.loads(json_obj)
		self.id = rid
		self.name = name
		self.description = description
		self.measurements = measurements

	def set_id(self, rid):
		self.id = rid

	def set_name(self, name):
		self.name = name

	def set_description(self, description):
		self.description = description

	def set_measurements(self, measurements):
		self.measurements = measurements

	def get_id(self):
		return self.id

	def get_name(self):
		return self.name

	def get_description(self):
		return self.description

	def get_measurements(self):
		return self.measurements


class MyJson(object):
	"""This class is used to process JSON"""
	def __init__(self, resources, page):
		"""Init method"""
		self.resources = resources
		self.page = page

	def to_json(self):
		"""Serializes object to JSON"""
		return json.dumps(self, default=lambda myjson: myjson.__dict__, sort_keys=False, indent=4)