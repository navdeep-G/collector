from controllers import AddFeedbackHandler, FeedbacksHandler, LogHandler, PopulateHandler

routes = [
    (r'/', FeedbacksHandler),
    (r'/add', AddFeedbackHandler),
    (r'/log/([a-zA-Z\-0-9]*)', LogHandler),
    (r'/populate', PopulateHandler),
]
