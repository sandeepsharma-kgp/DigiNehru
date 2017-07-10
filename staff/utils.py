
def check_access(func):
    def inner(request, *args, **kwargs):
        current_url_name = resolve(request.path_info).url_name
        method = request.method
        if method == 'GET':
            data = request.GET
            method_const = 0
        elif method == 'POST':
            data = request.POST
            method_const = 1
        # elif method == request.PUT:
        #     data = get_data_from_request(request)
        #     method_const = 2
        # elif method == request.DELETE:
        #     data = get_data_from_request(request)
        #     method_const = 3
        staff = Staff.objects.select_related('role').prefetch_related(
            'role__permission').get(empid=data.get('empid'))
        permissions = staff.role.permission.filter(
            method=method_const).values_list('api_name', flat=True)
        if current_url_name not in permissions:
            return 'Un-Auauthorized'  # return http_response  for frontend
        return func(request, *args, **kwargs)
    return inner
