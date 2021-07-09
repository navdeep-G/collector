import os

import sys
sys.path.append("..")

import tornado.ioloop
import tornado.web

from routes import get_routes


def make_app() -> tornado.web.Application:
    return tornado.web.Application(
        get_routes(list_path='example/templates/list_entries.html', add_path='example/templates/add_entry.html'),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
