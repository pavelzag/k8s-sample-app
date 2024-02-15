from flask import Flask, jsonify

app = Flask(__name__)


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
    app.run(debug=False, port=80, host='0.0.0.0')
