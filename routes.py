from controllers import AddFileHandler, DescriptionHandler, FileHandler

routes = [
    (r'/', DescriptionHandler),
    (r'/add', AddFileHandler),
    (r'/file/([a-zA-Z\-0-9]*)', FileHandler),
]
