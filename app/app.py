from flask import Flask, jsonify, abort
import logging
import os
import sys
from jaeger_client import Config
from flask_opentracing import FlaskTracing
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleExportSpanProcessor,
)
from opentelemetry.instrumentation.flask import FlaskInstrumentor

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    SimpleExportSpanProcessor(ConsoleSpanExporter())
)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

config = Config(
    config={
        'sampler':
            {'type': 'const',
             'param': 1},
        'logging': True,
        'reporter_batch_size': 1, },
    service_name="k8s-sample-app-service")
jaeger_tracer = config.initialize_tracer()
tracing = FlaskTracing(jaeger_tracer, True, app)

log_file = 'sample_app.log'
# log_file = '/var/log/sample_app.log'

# Configure the logger to write to the log file and stdout
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
logging.getLogger().addHandler(stdout_handler)

POD_NAME = os.getenv('HOSTNAME', 'default')
K8S_SAMPLE_APP_SERVICE_SERVICE_HOST = os.getenv('K8S_SAMPLE_APP_SERVICE_SERVICE_HOST', 'default')

try:
    if not os.path.exists(log_file):
        logging.info(f"{log_file} does not exist")
        open(log_file, 'w').close()
except Exception as e:
    logging.error(f"There was a problem creating a file {e}")


def square(x):
    return f"The square of {x} is {x ** 2}"


def cube(x):
    return f"The cube of {x} is {x ** 4}"


def calculate_fibonacci(n):
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence


@app.route('/hello')
def hello_world():
    logging.info(f"Hello from {POD_NAME}!")
    return f"Hello from {POD_NAME} and {K8S_SAMPLE_APP_SERVICE_SERVICE_HOST}!"


@app.route('/square/<int:num>')
@tracing.trace()
def call_square(num):
    result = square(num)
    return f"Calling square function: {result}"


@app.route('/cube/<int:num>')
@tracing.trace()
def call_cube(num):
    result = cube(num)
    return f"Calling cube function: {result}"


@app.route('/fibonacci/<int:n>')
@tracing.trace()
def generate_fibonacci(n):
    result = calculate_fibonacci(n)
    return jsonify({"fibonacci_sequence": result})


@app.route('/my_name_is/<string:name>')
@tracing.trace()
def my_name_is(name):
    if "_" in name:
        names_list = name.split("_")
    return f"My name is: {names_list[0].capitalize()} {names_list[1].capitalize()}"


@app.route('/not_found')
@tracing.trace()
def not_found():
    abort(404)


@app.route('/internal_server_error')
@tracing.trace()
def internal_server_error():
    abort(500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
