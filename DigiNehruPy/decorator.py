from .utils import get_token
from students.models import Students
from staff.models import Staff
from django.core.urlresolvers import resolve
from django.http.response import JsonResponse


def send_200(data):
    return JsonResponse(data=data, status=200)


def send_400(data):
    return JsonResponse(data=data, status=400)


def init_response(res_str=None, data=None):
    response = {}
    response["res_str"] = ""
    response["res_data"] = {}
    if res_str is not None:
        response["res_str"] = res_str
    if data is not None:
        response["res_data"] = data
    return response


def check_login(func):

    def __init__(self):
        self.response = init_response()

    def inner(self, request, *args, **kwargs):
        import ipdb
        ipdb.set_trace()
        data = {}
        method = request.method
        current_url_name = resolve(request.path_info).url_name
        method_const = []
        if method == 'GET':
            data = request.GET
            method_const = '0'
        elif method == 'POST':
            data = request.POST
            method_const = '1'
        token = data.get('token')
        if 'roll' in data.keys():
            try:
                Students.objects.get(roll=data['roll'], token=token)
            except:
                self.response['res_str'] = "logged-out"
                return send_400(self.response)
        if 'empid' in data.keys():
            if not get_token(data.get('empid')) == token:
                self.response['res_str'] = "Time Out"
                return send_400(self.response)
            try:
                staff = Staff.objects.select_related(
                    'role').get(empid=data.get('empid'))
                permissions = staff.role.permissions.filter(
                    api_name=current_url_name)
                if method_const not in permissions[0].method:
                    self.response['res_str'] = "Unauthorized"
                    return send_400(self.response)
            except Exception as e:
                self.response['res_str'] = str(e)
                return send_400(self.response)
        return func(self, request, *args, **kwargs)
    return inner
