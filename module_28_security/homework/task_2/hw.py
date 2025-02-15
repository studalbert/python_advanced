from flask import Flask, render_template_string, request, Response

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <title>Title</title>
</head>
<body>
 {{ user_input | safe }}
</body>
</html>
"""


@app.route("/")
def index():
    user_input = request.args.get("user_input", "")
    return render_template_string(HTML, user_input=user_input)


@app.after_request
def apply_csp(response: Response):
    response.headers["Content-Security-Policy"] = "script-src 'self'"
    return response


if __name__ == "__main__":
    app.run(debug=True)
