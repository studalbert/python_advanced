from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)


@app.route("/hello", methods=["GET", "POST"])
@metrics.counter(
    "request_count",
    "Number of requests to the endpoint",
    labels={
        "collection": "test",
        "method": lambda: request.method,
        "status": lambda req: req.status_code,
    },
)
def hello_req():
    return jsonify(message="hello world!")


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, threaded=True)
