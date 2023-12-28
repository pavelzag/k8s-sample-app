from flask import Flask, jsonify
import logging
import os
import sys
from jaeger_client import Config
from flask_opentracing import FlaskTracing

app = Flask(__name__)
config = Config(
    config={
        'sampler':
            {'type': 'const',
             'param': 1},
        'logging': True,
        'reporter_batch_size': 1, },
    service_name="k8s-sample-app")
jaeger_tracer = config.initialize_tracer()
tracing = FlaskTracing(jaeger_tracer, True, app)
# Define the log file path
log_file = '/var/log/sample_app.log'

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
def call_square(num):
    result = square(num)
    return f"Calling square function: {result}"


@app.route('/fibonacci/<int:n>')
def generate_fibonacci(n):
    result = calculate_fibonacci(n)
    return jsonify({"fibonacci_sequence": result})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
