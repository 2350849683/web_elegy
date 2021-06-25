from wsgiref.simple_server import make_server
_hub=None

class Elegy(object):

    def __init__(self,configuration):
        global _hub
        self.routes=[]
        if _hub is  None:
            _hub=self

        self.config = {
            "port" :8000,
            "host" :""
        }
        if configuration is not None: self.config.update(configuration)

    def route(self, url, func):
        if url is None: url = '/' + func.__name__ + '/'

        self.routes.append(JunoRoute(url, func))




    def run(self): #启动
        run_dev(self.config["host"],self.config["port"])

    def process_func(self,environ):  #获取响应

        request=environ["PATH_INFO"]
        if request[-1] != '/': request += '/'
        for route in self.routes:
            if not route.match(request): continue
            response = route.dispatch()
            if response is not  None:
                return ElegyResponse().render(response)

        return ElegyResponse().render("未注册",None)

class ElegyResponse(object):  #获得的响应
    status_codes = {
        200: '200 OK',
        404: '404 Not Found',
    }
    def render(self,body,env=True):  #响应
        if env :
            status = self.status_codes[200]
        else:
            body = elegy_404()
            status = self.status_codes[404]
        return body, status

class JunoRoute(object):
    def __init__(self, url, func):
        import re
        if url[0] != '/': url = '/' + url
        if url[-1] != '/': url += '/'
        self.old_url = url
        splat_re = re.compile('^\*?:(?P<var>\w+)$')
        buffer = '^'
        for part in url.split('/'):
            if not part: continue
            match_obj = splat_re.match(part)
            if match_obj is None: buffer += '/' + part
            else: buffer += '/(?P<' + match_obj.group('var') + '>[^/]*)/?'
        if buffer[-1] != ')': buffer += '/$'
        else: buffer += '/'
        self.url = re.compile(buffer)
        self.func = func
        self.params = {}

    def match(self, request):
        match_obj = self.url.match(request) #判断是否这个路径
        if match_obj is None: return False
        self.params.update(match_obj.groupdict()) #存储动态路由的值
        return True

    def dispatch(self):  #获取路由响应

        return self.func(**self.params)



def init(configuration=None): #初始化
    global _hub
    if _hub is None:
        _hub = Elegy(configuration)

def elegy_404():  #报错
    return "404"

def run():#启动
    """Start Juno, with an optional mode argument."""
    if _hub is None: init()
    return _hub.run()

def route(url=None):  #路由
    if _hub is None: init()
    def wrap(f): _hub.route(url, f)
    return wrap


def application(environ, start_response):   #返回结果
    body, status = _hub.process_func(environ)

    start_response(status, [('Content-type', 'text/plain')])
    return [body.encode("gbk")]


def run_dev(host,port):  #启动服务
    with make_server(host,port,application) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()

