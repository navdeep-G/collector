import os

import tornado.ioloop
import tornado.web

from routes import routes


def make_app() -> tornado.web.Application:
    return tornado.web.Application(
        routes,
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
