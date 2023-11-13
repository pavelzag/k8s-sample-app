from flask import Flask
import logging
import os
import sys

app = Flask(__name__)


# Configure the logger to write to the log file and stdout
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
logging.getLogger().addHandler(stdout_handler)

# Define the log file path
log_file = '/var/log/sample_app.log'

# Check if the log file exists, and create it if it doesn't
try:
    if not os.path.exists(log_file):
        logging.info(f"{log_file} does not exist")
        open(log_file, 'w').close()
except Exception as e:
    logging.error(f"There was a problem creating a file {e}")
    
@app.route('/')
def hello_world():
    # Log "Hello, World!" to the log file and stdout
    logging.info("Hello, World!")
    return "Hello, World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

