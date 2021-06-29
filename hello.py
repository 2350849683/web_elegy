from elegy import *
@get("/")
def index(web):
    name=web.input("name")
    return name

@route("/hello/*:name/*:age/")
def hello(web,name,age):
    a=f"hello {name} age {age}"
    return a

run()