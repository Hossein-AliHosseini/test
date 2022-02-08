import re

class SQLMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.method == 'POST' or request.method == 'GET' and re.search('^/admin/nobitex/(trades|market)/.+', request.path):
            print('\n\t\033[1mDatabase Accessed\033[0m\n')
        return response # not confirmed
