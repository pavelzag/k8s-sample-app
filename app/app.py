from flask import Flask, jsonify
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor


from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

app = Flask(__name__)

# Set up a TracerProvider
trace.set_tracer_provider(TracerProvider())
# Set the tracer provider

# Create an OTLP span exporter
otlp_exporter = OTLPSpanExporter(
    # Endpoint of the Collector or Jaeger service accepting OTLP over gRPC
    # Adjust the endpoint to your Jaeger gRPC endpoint if different
    endpoint="localhost:4317",  # Default OTLP gRPC endpoint
    insecure=True,  # For demo purposes, use insecure connection
)


# Configure the Jaeger exporter to export traces to Jaeger
# jaeger_exporter = JaegerExporter(
#     agent_host_name='localhost',
#     agent_port=6831,
# )

# Configure the tracer to use the Jaeger exporter
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

# Instrument Flask app with OpenTelemetry middleware to trace requests
FlaskInstrumentor().instrument_app(app)


def square(x):
    return f"The square of {x} is {x ** 2}"


def cube(x):
    return f"The cube of {x} is {x ** 4}"


def calculate_fibonacci(n):
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence


@app.route('/')
def hello_world():
    return 'Hello, World from Flask with OpenTelemetry!'


@app.route('/square/<int:num>')
def call_square(num):
    result = square(num)
    return jsonify({"result": result})


@app.route('/cube/<int:num>')
def call_cube(num):
    result = cube(num)
    return jsonify({"result": result})


@app.route('/fibonacci/<int:n>')
def generate_fibonacci(n):
    result = calculate_fibonacci(n)
    return jsonify({"fibonacci_sequence": result})


if __name__ == '__main__':
    app.run(debug=True, port=80)

# from flask import Flask, jsonify
# from jaeger_client import Config
# from flask_opentracing import FlaskTracing
#
# app = Flask(__name__)
#
# # Jaeger configuration
# config = Config(
#     config={
#         'sampler': {'type': 'const', 'param': 1},
#         'logging': True,
#         'reporter_batch_size': 1,
#     },
#     service_name="k8s-sample-app-service"
# )
# jaeger_tracer = config.initialize_tracer()
# tracing = FlaskTracing(jaeger_tracer, True, app)
#
#
# # def square(x):
# #     with tracing.start_span('square') as span:
# #         span.set_tag('number', x)
# #         return f"The square of {x} is {x ** 2}"
# #
# #
# # def cube(x):
# #     with tracing.start_span('cube') as span:
# #         span.set_tag('number', x)
# #         return f"The cube of {x} is {x ** 4}"
# #
# #
# # def calculate_fibonacci(n):
# #     fib_sequence = [0, 1]
# #     while len(fib_sequence) < n:
# #         fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
# #     return fib_sequence
#
#
# @app.route('/hello')
# def hello_world():
#     with tracing.start_span('hello') as span:
#         # Add tags or logs to the span as needed
#         span.set_tag('result_length', 'something')
#         return 'Hello from Flask!'
#
#
# if __name__ == '__main__':
#     # Run the Flask app on port 80 (requires root privileges)
#     app.run(host='0.0.0.0', port=80)
#
# # @app.route('/square/<int:num>')
# # def call_square(num):
# #     with tracing.start_span('square') as span:
# #         span.log_kv({'message': 'Hello from square endpoint'})
# #         result = square(num)
# #         return jsonify({"result": result})
# #
# #
# # @app.route('/cube/<int:num>')
# # def call_cube(num):
# #     with tracing.start_span('cube') as span:
# #         span.log_kv({'message': 'Hello from cube app!'})
# #         result = cube(num)
# #         return jsonify({"result": result})
# #
# #
# # @app.route('/fibonacci/<int:n>')
# # def generate_fibonacci(n):
# #     with tracing.start_span('fibonacci') as span:
# #         span.log_kv({'message': 'Hello from fibonacci endpoint!'})
# #         result = calculate_fibonacci(n)
# #         return jsonify({"fibonacci_sequence": result})
#
#
# # if __name__ == '__main__':
# #     # Run the Flask app on port 80 (requires root privileges)
# #     app.run(host='0.0.0.0', port=80)
#
# # from flask import Flask, jsonify, abort
# # import logging
# # import os
# # import sys
# # from opentelemetry import trace
# # from opentelemetry.exporter.jaeger.thrift import JaegerExporter
# # from opentelemetry.sdk.trace import TracerProvider
# # from opentelemetry.sdk.trace.export import BatchSpanProcessor
# #
# # trace.set_tracer_provider(TracerProvider())
# #
# # jaeger_exporter = JaegerExporter(
# #     agent_host_name='localhost',
# #     agent_port=6831,
# #     # optional: configure also collector
# #     # collector_endpoint='http://localhost:14268/api/traces?format=jaeger.thrift',
# #     # username=xxxx, # optional
# #     # password=xxxx, # optional
# #     # max_tag_value_length=None # optional
# # )
# #
# # span_processor = BatchSpanProcessor(jaeger_exporter)
# #
# # trace.get_tracer_provider().add_span_processor(span_processor)
# #
# # tracer = trace.get_tracer(__name__)
# #
# # with tracer.start_as_current_span("foo"):
# #     with tracer.start_as_current_span("bar"):
# #         with tracer.start_as_current_span("baz"):
# #             print("Hello world from OpenTelemetry Python!")
# #
# # stdout_handler = logging.StreamHandler(sys.stdout)
# # stdout_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
# # logging.getLogger().addHandler(stdout_handler)
# #
# # POD_NAME = os.getenv('HOSTNAME', 'default')
# # K8S_SAMPLE_APP_SERVICE_SERVICE_HOST = os.getenv('K8S_SAMPLE_APP_SERVICE_SERVICE_HOST', 'default')
# # app = Flask(__name__)
# #
# #
# # def square(x):
# #     return f"The square of {x} is {x ** 2}"
# #
# #
# # def cube(x):
# #     return f"The cube of {x} is {x ** 4}"
# #
# #
# # def calculate_fibonacci(n):
# #     fib_sequence = [0, 1]
# #     while len(fib_sequence) < n:
# #         fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
# #     return fib_sequence
# #
# #
# # @app.route('/hello')
# # def hello_world():
# #     with tracer.start_as_current_span("hello"):
# #         logging.info(f"Hello from {POD_NAME}!")
# #         return f"Hello from {POD_NAME} and {K8S_SAMPLE_APP_SERVICE_SERVICE_HOST}!"
# #
# #
# # @app.route('/fibonacci/<int:n>')
# # def generate_fibonacci(n):
# #     with tracer.start_as_current_span("fibonacci"):
# #         result = calculate_fibonacci(n)
# #         return jsonify({"fibonacci_sequence": result})
# #
# #
# # if __name__ == '__main__':
# #     app.run(host='0.0.0.0', port=80)
#
# # from flask import Flask, jsonify, abort
# # import logging
# # import os
# # import sys
# # from jaeger_client import Config
# # from flask_opentracing import FlaskTracing
# # from opentelemetry import trace
# # from opentelemetry.sdk.trace import TracerProvider
# # from opentelemetry.sdk.trace.export import (
# #     ConsoleSpanExporter,
# #     SimpleExportSpanProcessor,
# # )
# # from opentelemetry.instrumentation.flask import FlaskInstrumentor
# #
# # trace.set_tracer_provider(TracerProvider())
# # trace.get_tracer_provider().add_span_processor(
# #     SimpleExportSpanProcessor(ConsoleSpanExporter())
# # )
# #
# # app = Flask(__name__)
# # FlaskInstrumentor().instrument_app(app)
# #
# # config = Config(
# #     config={
# #         'sampler':
# #             {'type': 'const',
# #              'param': 1},
# #         'logging': True,
# #         'reporter_batch_size': 1, },
# #     service_name="k8s-sample-app-service")
# # jaeger_tracer = config.initialize_tracer()
# # tracing = FlaskTracing(jaeger_tracer, True, app)
# #
# # log_file = 'sample_app.log'
# # # log_file = '/var/log/sample_app.log'
# #
# # # Configure the logger to write to the log file and stdout
# # logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
# # stdout_handler = logging.StreamHandler(sys.stdout)
# # stdout_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
# # logging.getLogger().addHandler(stdout_handler)
# #
# # POD_NAME = os.getenv('HOSTNAME', 'default')
# # K8S_SAMPLE_APP_SERVICE_SERVICE_HOST = os.getenv('K8S_SAMPLE_APP_SERVICE_SERVICE_HOST', 'default')
# #
# # try:
# #     if not os.path.exists(log_file):
# #         logging.info(f"{log_file} does not exist")
# #         open(log_file, 'w').close()
# # except Exception as e:
# #     logging.error(f"There was a problem creating a file {e}")
# #
# #
# # def square(x):
# #     return f"The square of {x} is {x ** 2}"
# #
# #
# # def cube(x):
# #     return f"The cube of {x} is {x ** 4}"
# #
# #
# # def calculate_fibonacci(n):
# #     fib_sequence = [0, 1]
# #     while len(fib_sequence) < n:
# #         fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
# #     return fib_sequence
# #
# #
# # @app.route('/hello')
# # def hello_world():
# #     logging.info(f"Hello from {POD_NAME}!")
# #     return f"Hello from {POD_NAME} and {K8S_SAMPLE_APP_SERVICE_SERVICE_HOST}!"
# #
# #
# # @app.route('/square/<int:num>')
# # def call_square(num):
# #     result = square(num)
# #     return f"Calling square function: {result}"
# #
# #
# # @app.route('/cube/<int:num>')
# # def call_cube(num):
# #     result = cube(num)
# #     return f"Calling cube function: {result}"
# #
# #
# # @app.route('/fibonacci/<int:n>')
# # def generate_fibonacci(n):
# #     result = calculate_fibonacci(n)
# #     return jsonify({"fibonacci_sequence": result})
# #
# #
# # @app.route('/my_name_is/<string:name>')
# # def my_name_is(name):
# #     if "_" in name:
# #         names_list = name.split("_")
# #     return f"My name is: {names_list[0].capitalize()} {names_list[1].capitalize()}"
# #
# #
# # @app.route('/not_found')
# # def not_found():
# #     abort(404)
# #
# #
# # @app.route('/internal_server_error')
# # def internal_server_error():
# #     abort(500)
# #
# #
# # if __name__ == '__main__':
# #     app.run(host='0.0.0.0', port=80)
