from controllers import AddFileHandler, FilesHandler, LogHandler, PopulateHandler

routes = [
    (r'/', FilesHandler),
    (r'/add', AddFileHandler),
    (r'/log/([a-zA-Z\-0-9]*)', LogHandler),
    (r'/populate', PopulateHandler),
]
