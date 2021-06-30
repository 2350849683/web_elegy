from wsgiref.simple_server import make_server
import cgi,json
from urllib.parse import parse_qs

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

    def route(self, url, func,method):
        if url is None: url = '/' + func.__name__ + '/'

        self.routes.append( ElegyRoute(url, func,method))




    def run(self): #启动
        run_dev(self.config["host"],self.config["port"])

    def process_func(self,environ,method='*'):  #获取响应
        req_obj = ElegyRequest(environ)
        request=environ["PATH_INFO"]
        if request[-1] != '/': request += '/'
        for route in self.routes:
            if not route.match(request,method): continue
            response = route.dispatch(req_obj)
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

class ElegyRequest(object): #返回请求信息
    def __init__(self,request):
        if request['PATH_INFO'][-1] != '/': request['PATH_INFO'] += '/'
        self.raw = request
        self.raw['input'] = {}
        self.location = request['PATH_INFO']
        self.combine_request_dicts()

    def combine_request_dicts(self):
        input_dict = self.raw['QUERY_DICT'].copy()
        for k, v in self.raw['POST_DICT'].items():
            if k in input_dict.keys():
                input_dict[k].extend(v)
            else:
                input_dict[k] = v

        for k, v in input_dict.items():
            try:
                if len(v) == 1: input_dict[k] = v[0]
            except:
                pass
        self.raw['input'] = input_dict

    def input(self, arg=None):
        if arg is None: return self.raw['input']
        if arg in self.raw['input']:
            return self.raw['input'][arg]
        return None



class  ElegyRoute(object):
    def __init__(self, url, func,method):
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
        self.method = method.upper()
        self.params = {}

    def match(self, request,method):
        match_obj = self.url.match(request) #判断是否这个路径
        if match_obj is None: return False
        if self.method != '*' and self.method != method: return False
        self.params.update(match_obj.groupdict()) #存储动态路由的值
        return True

    def dispatch(self,req):  #获取路由响应

        return self.func(req,**self.params)



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


def route(url=None, method='*'):
    if _hub is None: init()
    def wrap(f): _hub.route(url, f, method)
    return wrap

def post(url=None):   return route(url, 'post')
def get(url=None):    return route(url, 'get')


def application(environ, start_response):   #返回结果

    environ['QUERY_DICT']=cgi.parse_qs(environ['QUERY_STRING'],
                 keep_blank_values=1)

    if environ['REQUEST_METHOD'] in 'POST':
        request_body = environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH", 0)))
        try:
            environ['POST_DICT'] = json.loads(request_body)  #json格式
        except:
            environ['POST_DICT'] = parse_qs(str(request_body, encoding='utf-8'))
    else:
        environ['POST_DICT']={}

    body, status = _hub.process_func(environ,environ['REQUEST_METHOD'])

    start_response(status, [('Content-type', 'text/plain')])
    return [str(body).encode("gbk")]


def run_dev(host,port):  #启动服务
    with make_server(host,port,application) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()

