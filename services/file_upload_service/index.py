import tornado.web
import tornado.ioloop

class uploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

    def post(self):
        files = self.request.files["imgFile"]
        for f in files:
            fh = open(f"img/{f.filename}", "wb")
            fh.write(f.body)
            fh.close()
        self.write(f"<a href = 'http://localhost:8080/img/{f.filename}'")

if (__name__ == "__main__"):
    app = tornado.web.Application([
        ("/", uploadHandler),
        ("/img/(.*)", tornado.web.StaticFileHandler, {"path" : "img"})
    ])

    app.listen(8080)
    print("Listening on port 8080")

    tornado.ioloop.IOLoop.instance().start()
