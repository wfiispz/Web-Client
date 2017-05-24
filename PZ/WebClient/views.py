from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .Connector import *
from django.shortcuts import render
from graphos.sources.simple import SimpleDataSource

from graphos.renderers.yui import LineChart


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/monitors/')
    else:
        return HttpResponseRedirect('/login/')


def login(request):
    c = {}
    c.update(csrf(request))

    return render_to_response('login.html', c)


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

    return render_to_response('monitors.html',
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
    return render_to_response('create_monitor.html', {"full_name": request.user.username}, args)


def delete_monitor(request, monitor_id):
    Monitors.objects.get(id=monitor_id, user_id=request.user.id).delete()
    return HttpResponseRedirect("/monitors/")


def invalid_login(request):
    return render_to_response('invalid_login.html')


def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')


def register_success(request):
    return render_to_response('register_success.html')


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

    return render_to_response('register.html', args)


def hosts(request, monitor_id):
    current_monitor = Monitors.objects.get(id=monitor_id)
    c = Connector(urljoin(current_monitor.monitor_domain, 'resources'))

    if request.method == 'GET':
        search_query = request.GET.get('name', None)
        c._payload = {"name": search_query}

    host_list, page = c.get_resources()
    return render_to_response('hosts.html', {"get_name": search_query, "full_name": request.user.username,
                                             'monitor_domain': current_monitor.monitor_domain, 'monitor_id': monitor_id,
                                             'host_list': host_list})


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

    return render_to_response('archives.html', {'host_list': host_list, 'measurements_list': measurements_list,
                                                'monitor_id': monitor_id})


def measurements(request, monitor_id, host_id):
    c = Connector(Monitors.objects.get(id=monitor_id).monitor_domain)

    measurements_endpoints = c.get_resource_id('resources/' + host_id).measurements
    measurements_list = c.get_measurements(str(measurements_endpoints).replace("\'", "\""))

    for measurement in measurements_list:
        value = str(measurement.values)
        measurement.values = value.split('/')[len(value.split('/')) - 2]

    return render_to_response('measurements.html',
                              {"full_name": request.user.username, 'resources_list': measurements_list,
                               'monitor_id': monitor_id, 'host_id': host_id})


def values(request, monitor_id, host_id, measurement_id):
    c = Connector(Monitors.objects.get(id=monitor_id).monitor_domain)

    measurements_endpoints = c.get_resource_id('resources/' + host_id).measurements
    for endpoint in measurements_endpoints:
        if endpoint.__contains__(measurement_id):
            measurements_endpoint = endpoint

    values_list = c.get_measurement_values(measurements_endpoint)
    print(values_list)

    return render_to_response('values.html', {"full_name": request.user.username, 'values_list': values_list})


def graph(request, monitor_id, host_id, measurement_id):
    c = Connector(Monitors.objects.get(id=monitor_id).monitor_domain)

    measurements_endpoints = c.get_resource_id('resources/' + host_id).measurements
    for endpoint in measurements_endpoints:
        if endpoint.__contains__(measurement_id):
            measurements_endpoint = endpoint

    values_list = c.get_measurement_values(measurements_endpoint)

    data = [
        ['DateTime', 'values']
    ]

    for val in values_list:
        data.append([val.datetime, val.value])

    data_source = SimpleDataSource(data=data)

    chart = LineChart(data_source)

    return render_to_response('graph.html',
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
        ['DateTime', 'values']
    ]

    for val in values_list:
        data.append([val.datetime, val.value])

    data_source = SimpleDataSource(data=data)

    chart = LineChart(data_source)

    chart.get_options_json = '{"title": "Chart"}'
    return render(request, 'update_graph.html',
                  {"full_name": request.user.username, 'values_list': values_list, 'monitor_id': monitor_id,
                   'host_id': host_id, 'measurement_id': measurement_id, 'chart': chart})
