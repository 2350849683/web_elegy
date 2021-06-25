from elegy import *
@route("/")
def index():
    return "OK"

@route("/hello/*:name/*:age/")
def hello(name,age):
    a=f"hello {name} age {age}"
    return a

run()