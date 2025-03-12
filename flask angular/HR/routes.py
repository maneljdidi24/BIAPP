from . import hr_routes

@hr_routes.route('/')
def hello_world():
    return  ({
        'error': "hello",
        'server': "source",
        'code': '300'
                })