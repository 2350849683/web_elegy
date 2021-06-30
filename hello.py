from elegy import *
@get("/")
def index(web):

    return web.input()

@post("/hello")
def hello(web):
    return web.input()


run()