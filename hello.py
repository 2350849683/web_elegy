from elegy import *
@route("/")
def index():
    return "首页"

@route("/hello/*:name/*:age/")
def hello(name,age):
    a=f"hello {name} age {age}"
    return a

run()