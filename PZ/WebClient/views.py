from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import Monitors
from .models import Hosts


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

            return render_to_response('create_monitor.html', args)
        else:
            m = Monitors(monitor_name=name, monitor_domain=domain, user_id=request.user)
            m.save()

            return HttpResponseRedirect("/monitors/")

    args.update(csrf(request))
    return render_to_response('create_monitor.html', args)


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

    args = {}
    args.update(csrf(request))

    args['form'] = UserCreationForm()

    return render_to_response('register.html', args)

def hosts(request, monitor_id):
    # TODO Take information about hosts from monitor
    host_list = Hosts.objects.filter(monitor_id_id=monitor_id)
    return render_to_response('hosts.html', {"host_list": host_list})