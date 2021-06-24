from wsgiref.simple_server import make_server


def index():
    return [b"OK"]


def hello():
    return [b"hello"]

def elegy_404():
    return [b"404"]

route_dict = {
    '/': index,
    '/hello': hello
}


class Elegy(object):

    def __init__(self,configuration):
        global _hub

        if _hub is  None:
            _hub=self

        self.config = {
            "port" :8000,
            "host" :""
        }
        if configuration is not None: self.config.update(configuration)
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

    def render(self,env):
        if env in route_dict:
            body = route_dict[env]()
            status = self.status_codes[200]
        else:
            body = elegy_404()
            status = self.status_codes[404]
        return body, status

_hub=None

def init(configuration=None):
    global _hub
    if _hub is None:
        _hub = Elegy(configuration)


def run():
    """Start Juno, with an optional mode argument."""
    if _hub is None: init()
    return _hub.run()


def application(environ, start_response):
    body, status = _hub.process_func(environ)

    start_response(status, [('Content-type', 'text/plain')])

    return body


def run_dev(host,port):
    with make_server(host,port,application) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()

init({"port":9000})
run()

