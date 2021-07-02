from elegy import *

@route("/", method=["POST","GET"])
def index(web):
    return web.headers,web.method

@route("/hello")
def hello(web):

    return web.input()

@route("/he")
def hello(web):
    return "hello world"
run()