from elegy import *

@route("/", method=["POST","GET"])
def index():

    return request.args,request.headers,request.method

@route("/hello")
def hello1():

    return request.method

@route("/he")
def hello():
    return "hello world"
run()