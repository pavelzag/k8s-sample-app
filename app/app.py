from flask import Flask, jsonify
from flask_restx import Api, Resource
import yaml

app = Flask(__name__)

app.config['SERVER_NAME'] = 'localhost:80'
api = Api(app, version='1.0', title='Sample API',
          description='A simple API')

ns = api.namespace('api', description='Main operations')  # Define a namespace


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


def square(x):
    return f"The square of {x} is {x ** 2}"


def cube(x):
    return f"The cube of {x} is {x ** 4}"


def calculate_fibonacci(n):
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence


# Redefine routes as classes inheriting from Resource
@ns.route('/hello')  # Default namespace
class HelloWorld(Resource):
    @staticmethod
    def get():
        return jsonify('Hello, World from Flask with OpenTelemetry!')


@ns.route('/square/<int:num>')  # Use the namespace for API-specific routes
class Square(Resource):
    @staticmethod
    def get(num):
        result = square(num)
        return jsonify({"result": result})


@ns.route('/cube/<int:num>')
class Cube(Resource):
    @staticmethod
    def get(num):
        result = cube(num)
        return jsonify({"result": result})


@ns.route('/fibonacci/<int:n>')
class Fibonacci(Resource):
    @staticmethod
    def get(n):
        result = calculate_fibonacci(n)
        return jsonify({"fibonacci_sequence": result})


if __name__ == '__main__':
    generate_openapi_yaml(app, api)  # Save the OpenAPI spec to YAML within app context
    app.run(debug=False, port=80, host='0.0.0.0')
