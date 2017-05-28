from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .Connector import *
from django.shortcuts import render
from graphos.sources.simple import SimpleDataSource

from graphos.renderers.yui import LineChart
from datetime import datetime, timedelta

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/monitors/')
    else:
        return HttpResponseRedirect('/login/')


def login(request):
    c = {}
    c.update(csrf(request))

    return render(request, 'login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/monitors/')
    else:
        return HttpResponseRedirect('/invalid/')


def monitors(request):
    user_monitor_list = Monitors.objects.filter(user_id=request.user.id)

    return render(request, 'monitors.html',
                              {"full_name": request.user.username,
                               "monitors_list": user_monitor_list})


def create_monitor(request):
    args = {}

    if request.method == "POST":
        name = request.POST.get('monitor_name', '')
        domain = request.POST.get('monitor_domain', '')

        if Monitors.objects.filter(Q(monitor_name=name) | Q(monitor_domain=domain), user_id=request.user.id):

            args.update(csrf(request))
            args['error'] = 'You already created monitor with selected name or domain. Choose another one.'

            return render_to_response('create_monitor.html', {"full_name": request.user.username}, args)
        else:
            m = Monitors(monitor_name=name, monitor_domain=domain, user_id=request.user)
            m.save()

            return HttpResponseRedirect("/monitors/")

    args.update(csrf(request))
    return render(request, 'create_monitor.html', {"full_name": request.user.username}, args)


def delete_monitor(request, monitor_id):
    Monitors.objects.get(id=monitor_id, user_id=request.user.id).delete()
    return HttpResponseRedirect("/monitors/")


def invalid_login(request):
    return render(request, 'invalid_login.html')


def logout(request):
    auth.logout(request)
    return render(request, 'logout.html')


def register_success(request):
    return render(request, 'register_success.html')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/register_success/")
    else:
        form = UserCreationForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form

    return render(request, 'register.html', args)


def hosts(request, monitor_id):
    current_monitor = Monitors.objects.get(id=monitor_id)
    connection = Connector(urljoin(current_monitor.monitor_domain, 'resources'))

    if request.method == 'GET':
        search_query = request.GET.get('name', None)
        connection.payload = {"name": search_query}

    host_list, page = connection.get_resources()
    return render(request, 'hosts.html', {"get_name": search_query, "full_name": request.user.username, 'monitor_domain' : current_monitor.monitor_domain, 'monitor_id' : monitor_id, 'host_list' : host_list})


def measurements(request, monitor_id, host_id):
    current_monitor = Monitors.objects.get(id=monitor_id)
    connection = Connector(current_monitor.monitor_domain)

    measurements_endpoints = connection.get_resource_id('resources/' + host_id).measurements
    measurements_list = connection.get_measurements(str(measurements_endpoints).replace("\'", "\""))

    for measurement in measurements_list:
        value =  str(measurement.values)
        measurement.values = value.split('/')[len(value.split('/')) - 2]

    return render(request, 'measurements.html', {"full_name": request.user.username, 'monitor_domain' : current_monitor.monitor_domain, 'resources_list' : measurements_list, 'monitor_id' : monitor_id, 'host_id' : host_id})


def values(request, monitor_id, host_id, measurement_id, page_id = 1):
    current_monitor = Monitors.objects.get(id=monitor_id)
    connection = Connector(current_monitor.monitor_domain)

    measurements_endpoints = connection.get_resource_id('resources/' + host_id).measurements
    for endpoint in measurements_endpoints:
        if endpoint.__contains__(measurement_id):
            measurements_endpoint = endpoint

    connection.payload = {"from" : datetime.now() - timedelta(minutes= int(page_id) * 1), "to" : datetime.now() - timedelta(minutes= (int(page_id) - 1) * 1)}
    values_list = connection.get_measurement_values(measurements_endpoint)
    values_list.reverse()

    connection.payload = {"from" : datetime.now() - timedelta(minutes= (int(page_id)+1) * 1), "to" : datetime.now() - timedelta(minutes= int(page_id) * 1)}
    next_values_list = connection.get_measurement_values(measurements_endpoint)

    if int(page_id) <= 1:
        previous_index = int(page_id)
        next_index = int(page_id) + 1
    else:
        previous_index = int(page_id) - 1
        next_index = int(page_id) + 1

    if not next_values_list:
        next_index = int(page_id)

    return render(request, 'values.html', {'full_name': request.user.username, 'monitor_domain' : current_monitor.monitor_domain, 'values_list': values_list,  'monitor_id' : monitor_id, 'host_id' : host_id, 'measurement_id': measurement_id, 'previous_index': previous_index, 'next_index': next_index})

def graph(request, monitor_id, host_id, measurement_id):
    c = Connector(Monitors.objects.get(id=monitor_id).monitor_domain)

    measurements_endpoints = c.get_resource_id('resources/' + host_id).measurements
    for endpoint in measurements_endpoints:
        if endpoint.__contains__(measurement_id):
            measurements_endpoint = endpoint

    values_list = c.get_measurement_values(measurements_endpoint)

    data = [
        ['datetime', 'values']
    ]

    for val in values_list:
        data.append([val.datetime, val.value])

    data_source = SimpleDataSource(data=data)

    chart = LineChart(data_source)
    return render(request, 'graph.html',
                              {"full_name": request.user.username, 'values_list': values_list, 'monitor_id': monitor_id,
                               'host_id': host_id, 'measurement_id': measurement_id, 'chart': chart})


def update_graph(request, monitor_id, host_id, measurement_id):
    c = Connector(Monitors.objects.get(id=monitor_id).monitor_domain)

    measurements_endpoints = c.get_resource_id('resources/' + host_id).measurements
    for endpoint in measurements_endpoints:
        if endpoint.__contains__(measurement_id):
            measurements_endpoint = endpoint

    values_list = c.get_measurement_values(measurements_endpoint)

    data = [
        ['datetime', 'values']
    ]

    for val in values_list:
        data.append([val.datetime, val.value])


    data_source = SimpleDataSource(data=data)
    chart = LineChart(data_source)
    return render(request, 'update_graph.html',
                  {"full_name": request.user.username, 'values_list': values_list, 'monitor_id': monitor_id,
                   'host_id': host_id, 'measurement_id': measurement_id, 'chart': chart})

def archives(request, monitor_id):
    current_monitor = Monitors.objects.get(id=monitor_id)
    c = Connector(urljoin(current_monitor.monitor_domain, 'resources'))

    host_list, page = c.get_resources()
    measurements_list = []
    for host in host_list:
        m1 = host.measurements
        measurements_list = measurements_list + c.get_measurements(str(m1).replace("\'", "\""))

    for measurement in measurements_list:
        value = str(measurement.values)
        host = str(measurement.host)
        measurement.values = value.split('/')[len(value.split('/')) - 2]
        measurement.host = host.split('/')[4]

    return render(request, 'archives.html', {'host_list': host_list, 'measurements_list': measurements_list, 'monitor_id': monitor_id})
