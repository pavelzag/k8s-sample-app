from flask import Flask, jsonify
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app, version='1.0', title='Sample API',
          description='A simple API')

ns = api.namespace('api', description='Main operations')  # Define a namespace


# Adjust the functions to not directly interact with request objects
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
    app.run(debug=False, port=80, host='0.0.0.0')



# from flask import Flask, jsonify
#
# app = Flask(__name__)
#
#
# def square(x):
#     return f"The square of {x} is {x ** 2}"
#
#
# def cube(x):
#     return f"The cube of {x} is {x ** 4}"
#
#
# def calculate_fibonacci(n):
#     fib_sequence = [0, 1]
#     while len(fib_sequence) < n:
#         fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
#     return fib_sequence
#
#
# @app.route('/')
# def hello_world():
#     return 'Hello, World from Flask with OpenTelemetry!'
#
#
# @app.route('/square/<int:num>')
# def call_square(num):
#     result = square(num)
#     return jsonify({"result": result})
#
#
# @app.route('/cube/<int:num>')
# def call_cube(num):
#     result = cube(num)
#     return jsonify({"result": result})
#
#
# @app.route('/fibonacci/<int:n>')
# def generate_fibonacci(n):
#     result = calculate_fibonacci(n)
#     return jsonify({"fibonacci_sequence": result})
#
#
# if __name__ == '__main__':
#     app.run(debug=False, port=80, host='0.0.0.0')
