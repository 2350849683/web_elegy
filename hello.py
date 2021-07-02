from elegy import *
@route("/", method=["POST","GET"])
def index(web):

    return web.input()

@route("/hello")
def hello(web):
    return web.input()

@route("/he")
def hello(web):
    return "hello world"
run()