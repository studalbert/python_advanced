import json
import re


class WsgiApp:
    routes = {}

    def route(self, path):
        def wrapper(func):
            self.routes[path] = func
            return func

        return wrapper

    def __call__(self, environ, start_response):
        req_url = environ["REQUEST_URI"]
        headers = [("Content-Type", "application/json")]
        if req_url == "/hello":
            status = "200 OK"
            response = self.routes[req_url]()
        elif req_url.startswith("/hello/"):
            status = "200 OK"
            username = re.match(r"^/hello/([^/]+)", req_url)
            response = self.routes["/hello/<name>"](username.group(1))
        else:
            status = "404 Not Found"
            response = json.dumps({"error": "Page not found"}, indent=4)
        start_response(status, headers)
        return [response.encode("utf-8")]


application = WsgiApp()


@application.route("/hello")
def say_hello():
    return json.dumps({"response": "Hello, world!"}, indent=4)


@application.route("/hello/<name>")
def say_hello_with_name(name: str):
    return json.dumps({"response": f"Hello, {name}!"}, indent=4)
