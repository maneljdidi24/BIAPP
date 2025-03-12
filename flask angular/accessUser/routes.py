from . import access_routes

@access_routes.route('/')
def hello_world():
    return  ({
        'error': "hello",
        'server': "source",
        'code': '300'
                })