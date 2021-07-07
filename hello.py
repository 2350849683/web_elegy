
from elegy import *

@route("/", method=["POST","GET"])
def index():

    return request.args,request.headers,request.method

@route("/hello")
def hello1():

    return template("hello.html", {"name":"刘赢杰","age":"20"})

@route("/he")
def hello():
    return "hello worlda大苏打"
run()