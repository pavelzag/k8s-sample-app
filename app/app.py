import os

from flask import Flask, jsonify, make_response, send_from_directory
import requests
import yaml

from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry import trace

app = Flask(__name__)


def setup_open_telemetry():
    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer("k8s-sample-app")

    # Initialize OTLP Exporter - adjust the endpoint as necessary
    otlp_exporter = OTLPSpanExporter(endpoint="http://jaeger-collector.istio-system:4317", insecure=True)

    # Add Span Processor
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

    # Instrument Flask and Requests
    FlaskInstrumentor().instrument_app(app)
    RequestsInstrumentor().instrument()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


def convert_ordered_dict_to_dict(input_ordered_dict):
    if isinstance(input_ordered_dict, dict):
        return {key: convert_ordered_dict_to_dict(value) for key, value in input_ordered_dict.items()}
    elif isinstance(input_ordered_dict, list):
        return [convert_ordered_dict_to_dict(element) for element in input_ordered_dict]
    else:
        return input_ordered_dict


def generate_openapi_yaml(app, api, filename='api_spec.yaml'):
    """
    Generates a YAML file for the OpenAPI specification.

    :param app: The Flask application instance
    :param api: The Flask-RESTx Api object
    :param filename: The output filename for the YAML specification
    """
    with app.app_context():  # Pushes an application context
        openapi_spec = api.__schema__
    openapi_spec = convert_ordered_dict_to_dict(openapi_spec)

    with open(filename, 'w') as yaml_file:
        yaml.safe_dump(openapi_spec, yaml_file, allow_unicode=True, sort_keys=False)


def calculate_square(x):
    return f"The square of {x} is {x ** 2}"


def calculate_cube(x):
    return f"The cube of {x} is {x ** 4}"


def calculate_fibonacci(n):
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence


@app.route('/')
def index():
    html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Under Construction</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f0f0f0;
                        text-align: center; /* Center the content */
                        padding-top: 50px;
                    }
                    h1 {
                        color: #333;
                    }
                    p {
                        color: #666;
                    }
                    .container {
                        width: 80%;
                        margin: auto;
                        background-color: #fff;
                        padding: 20px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        border-radius: 8px;
                    }
                    img {
                        max-width: 100%;
                        height: auto;
                        border-radius: 8px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Under Construction</h1>
                    <p>This page is under construction. Please check back later.</p>
                    <img src="/static/wix.gif" alt="Wix">
                    <img src="/static/under_construction.gif" alt="Under Construction">
                    <img src="/static/wix.gif" alt="Wix">
                </div>
            </body>
            </html>
            """
    response = make_response(html_content)
    response.headers['Content-Type'] = 'text/html'
    return response


@app.route('/hello')
def hello():
    return jsonify('Hello, World from Flask with OpenTelemetry!')


@app.route('/square/<int:num>')
def square(num):
    result = calculate_square(num)
    return jsonify({"result": result})


@app.route('/cube/<int:num>')
def cube(num):
    result = calculate_cube(num)
    return jsonify({"result": result})


@app.route('/fibonacci/<int:n>')
def fibonacci(n):
    result = calculate_fibonacci(n)
    return jsonify({"fibonacci_sequence": result})


@app.route('/')
def hello_world():
    return 'Hello, World!'
# Flask Routes
@app.route('/')
def home():
    return "Hello, OpenTelemetry!"


@app.route('/external')
def external_call():
    response = requests.get("https://httpbin.org/get")
    return f"External API called! Status code: {response.status_code}"


# Main Entry Point
if __name__ == '__main__':
    setup_open_telemetry()  # Setup OpenTelemetry instrumentation
    app.run(port=8080)