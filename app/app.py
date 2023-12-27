from flask import Flask, request
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
    service_name="service")
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

try:
    if not os.path.exists(log_file):
        logging.info(f"{log_file} does not exist")
        open(log_file, 'w').close()
except Exception as e:
    logging.error(f"There was a problem creating a file {e}")


@app.route('/hello')
def hello_world():
    logging.info(f"Hello from {POD_NAME}!")
    return f"Hello from {POD_NAME}!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
