from controllers import AddFileHandler, DescriptionHandler, FileHandler


def get_routes(list_path=None, add_path=None):
    routes = [
        (r'/', DescriptionHandler, dict(path=list_path)),
        (r'/add', AddFileHandler, dict(path=add_path)),
        (r'/file/([a-zA-Z\-0-9]*)', FileHandler),
    ]
    return routes
