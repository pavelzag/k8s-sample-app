from flask import Flask, jsonify, make_response
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


@ns.route('/')
class IndexPage(Resource):
    @staticmethod
    def get():
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


@ns.route('/hello')
class HelloWorld(Resource):
    @staticmethod
    def get():
        return jsonify('Hello, World from Flask with OpenTelemetry!')


@ns.route('/square/<int:num>')
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
        # test
        result = calculate_fibonacci(n)
        return jsonify({"fibonacci_sequence": result})


if __name__ == '__main__':
    generate_openapi_yaml(app, api)
    app.run(debug=True, port=80, host='0.0.0.0')
