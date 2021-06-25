from elegy import *
@route("/")
def index():
    return [b"OK"]

@route("/hello/*:name/")
def hello(name):
    a="hello %s " % name
    return [a.encode("utf-8")]

run()