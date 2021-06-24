from wsgiref.simple_server import make_server


class Elegy(object):

    def __init__(self):
        self.config = {
            "port" :8000,
            "host" :""
        }

    def run(self):
        run_dev(self.config["host"],self.config["port"])

    def process_func(self,environ):
        response=ElegyResponse()
        return response.render(environ["PATH_INFO"])


class ElegyResponse(object):  #获得的响应
    def __init__(self):
        self.status_codes = {
            200: '200 OK',
            404: '404 Not Found',
        }
        self.route_dict = {
            '/': self.index,
            '/hello': self.hello
        }

    def index(self):
        return [b"OK"]

    def hello(self):
        return [b"hello"]

    def elegy_404(self):
        return [b"404"]

    def render(self,env):
        if env in self.route_dict:
            body = self.route_dict[env]()
            status = self.status_codes[200]
        else:
            body = self.elegy_404()
            status = self.status_codes[404]
        return body, status

def application(environ, start_response):
    elegy=Elegy()
    body, status = elegy.process_func(environ)

    start_response(status, [('Content-type', 'text/plain')])

    return body


def run_dev(host,port):
    with make_server(host,port,application) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()

Elegy().run()
