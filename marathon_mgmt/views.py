from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from marathon import MarathonClient
from django.views.decorators.csrf import csrf_exempt
from marathon_mgmt.utils import *
import json
import html
import traceback
from config_template.models import *
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied

# Create your views here.
@csrf_exempt
@login_required
@permission_required('auth.can_init_app', raise_exception=True)
def new_app(request, type):
    data = {}
    if request.method == 'POST':
        data['msg'] = "Post"
        post_params = {}
        for key in request.POST:
            if key.startswith("filehidden"):
                fkey = key[11:]
                if(request.FILES.get(fkey, None)):
                    post_file = request.FILES[fkey]
                    file_content=""
                    for chunk in post_file.chunks():
                        file_content += chunk.decode("utf8")
                    post_params[fkey] = convert(file_content)
                else:
                    post_params[fkey] = request.POST[key]
            else:
                post_params[key] = request.POST[key]


        template = Template.objects.get(pk=post_params['template_id'])
        content = template.content%post_params
        data['content'] = content
        mc = MarathonClient('http://{}:{}'.format(settings.MARATHON['host'], settings.MARATHON['port']))
        try:
            if(type == "app"):
                mc.create_app_by_json(content)
            elif(type == "group"):
                mc.create_group(content)
            data['result'] = "Success"
        except Exception as e:
            data['result'] = str(e)

    if(type == "app"):
        data['type'] = "Application"
        templates = Template.objects.filter(type="marathon-app").all()
    elif(type == "group"):
        data['type'] = "Group"
        templates = Template.objects.filter(type="marathon-group").all()
    for template in templates:
        template.params = template.param_set.order_by('id')

    data['templates'] = templates
    return render(request, 'marathon_mgmt/new_app.html', data)

@login_required
def list_app(request):
    mc = MarathonClient('http://{}:{}'.format(settings.MARATHON['host'], settings.MARATHON['port']))
    apps = mc.list_apps()
    apps = sorted(apps, key=lambda app: app.id)
    for app in apps:
        app.tag_id = app.id.replace("/","__")
    data = {'apps': apps}
    return render(request, 'marathon_mgmt/list_app.html', data)


@csrf_exempt
@permission_required('auth.can_run_app', raise_exception=True)
@login_required
def send_to_marathon(request):
    try:
        if request.method == 'POST':
            action = request.POST.get('action', None)
            app_id = request.POST.get('id', None)
            mc = MarathonClient('http://{}:{}'.format(settings.MARATHON['host'], settings.MARATHON['port']))
            if action == 'stop':
                mc.scale_app(app_id, 0, force=True)
            elif action == 'start':
                mc.scale_app(app_id, 1)
            elif action == 'destroy':
                if request.user.has_perm("auth.can_init_app"):
                    mc.delete_app(app_id)
                else:
                    raise PermissionDenied
            elif action == 'restart':
                mc.restart_app(app_id)
            elif action == 'scale':
                mc.scale_app(app_id, int(request.POST.get('number_instance')))
            elif action == 'update':
                app = mc.get_app(app_id)
                app.cpus = float(request.POST.get('cpus'))
                app.mem = float(request.POST.get('mem'))
                app.container.docker.image = request.POST.get('version')
                mc.update_app(app_id, app)
            result = '{"status":"success", "msg": "%(action)s success"}'%{"action":action}
    except Exception as e:
        result = '{"status":"error", "msg": "%(action)s fail: %(error)s" }'%{"action":action, "error": html.escape(str(e))}
    return HttpResponse(result)

@login_required
def ajax_list_apps(request):
    mc = MarathonClient('http://{}:{}'.format(settings.MARATHON['host'], settings.MARATHON['port']))
    apps = mc.list_apps()
    apps = sorted(apps, key=lambda app: app.id)
    filter_name = request.GET.get('filter_name', "")
    if filter_name != "":
        for app in apps[:]:
            app.tag_id = app.id.replace("/","__")
            if app.id.find(filter_name) == -1:
                apps.remove(app)
    else:
        for app in apps:
            app.tag_id = app.id.replace("/","__")
    data = {'apps': apps}
    return render(request, 'marathon_mgmt/ajax_list_apps.html', data)
