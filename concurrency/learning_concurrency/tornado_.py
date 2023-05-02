
""" event-driven and reactive libraries """
# Tornado
# is a Python web framework and asynchronous networking library;
# It utilizes non-blocking network I/O and can subsequently scale to tens of
# thousands of connections;
# RESTful API
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

# Flask
