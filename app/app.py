from flask import Flask, request, jsonify
import time

app = Flask(__name__)


class InventoryItem:
    def __init__(self, id, name, image):
        self.id = id
        self.name = name
        self.image = image


inventory_items = [
    InventoryItem(1, "T Shirt", "https://emoji.aranja.com/static/emoji-data/img-apple-160/1f455.png"),
    InventoryItem(2, "Pants", "https://emoji.aranja.com/static/emoji-data/img-apple-160/1f456.png"),
    InventoryItem(3, "Shoes", "https://emoji.aranja.com/static/emoji-data/img-apple-160/1f462.png"),
    InventoryItem(4, "Hat", "https://emoji.aranja.com/static/emoji-data/img-apple-160/1f9e2.png"),
    InventoryItem(5, "Socks", "https://emoji.aranja.com/static/emoji-data/img-apple-160/1f9e6.png"),
    InventoryItem(6, "Gloves", "https://emoji.aranja.com/static/emoji-data/img-apple-160/1f9e4.png"),
    InventoryItem(7, "Scarf", "https://emoji.aranja.com/static/emoji-data/img-apple-160/1f9e3.png"),
    InventoryItem(8, "Jacket", "https://emoji.aranja.com/static/emoji-data/img-apple-160/1f9e5.png"),
    InventoryItem(9, "Kimono", "https://emoji.aranja.com/static/emoji-data/img-apple-160/1f458.png"),
    InventoryItem(10, "Purse", "https://emoji.aranja.com/static/emoji-data/img-apple-160/1f45b.png"),
    InventoryItem(11, "Tophat", "https://emoji.aranja.com/static/emoji-data/img-apple-160/1f3a9.png"),
    InventoryItem(12, "Watch", "https://emoji.aranja.com/static/emoji-data/img-apple-160/231a.png"),
    InventoryItem(13, "Sunglasses", "https://emoji.aranja.com/static/emoji-data/img-apple-160/1f576-fe0f.png"),
    InventoryItem(14, "Womans Hat", "https://emoji.aranja.com/static/emoji-data/img-apple-160/1f452.png"),
    InventoryItem(15, "Sandal", "https://emoji.aranja.com/static/emoji-data/img-apple-160/1f461.png"),
    InventoryItem(16, "Bracelet", "https://emoji.aranja.com/static/emoji-data/img-apple-160/1f4ff.png"),
    InventoryItem(17, "Ring", "https://emoji.aranja.com/static/emoji-data/img-apple-160/1f48d.png"),
    InventoryItem(18, "Suit", "https://emoji.aranja.com/static/emoji-data/img-apple-160/1f454.png"),
    InventoryItem(19, "Dress", "https://emoji.aranja.com/static/emoji-data/img-apple-160/1f457.png"),
    InventoryItem(20, "Eyeglasses", "https://emoji.aranja.com/static/emoji-data/img-apple-160/1f453.png")
]


@app.route('/inventory', methods=['GET'])
def get_inventory():
    print("Returning inventory")
    return jsonify([item.__dict__ for item in inventory_items])


@app.route('/buy', methods=['POST'])
def buy_product():
    product_id = request.args.get('id', type=int)
    print(f"Buying product with id {product_id}")
    time.sleep(1)
    return jsonify({"message": "Product purchased successfully"})


if __name__ == '__main__':
    app.run(debug=False, port=80, host='0.0.0.0')

# from flask import Flask, jsonify
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor
# from opentelemetry.instrumentation.flask import FlaskInstrumentor
#
#
# from opentelemetry import trace
# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
#
# app = Flask(__name__)
#
# # Set up a TracerProvider
# trace.set_tracer_provider(TracerProvider())
#
#
# # Create an OTLP span exporter
# otlp_exporter = OTLPSpanExporter(
#     # Endpoint of the Collector or Jaeger service accepting OTLP over gRPC
#     # Adjust the endpoint to your Jaeger gRPC endpoint if different
#     endpoint="my-release-jaeger-operator-metrics.istio-system:4317",  # Default OTLP gRPC endpoint
#     insecure=True,  # For demo purposes, use insecure connection
# )
#
#
# # Configure the Jaeger exporter to export traces to Jaeger
# # jaeger_exporter = JaegerExporter(
# #     agent_host_name='localhost',
# #     agent_port=6831,
# # )
#
# # Configure the tracer to use the Jaeger exporter
# trace.get_tracer_provider().add_span_processor(
#     BatchSpanProcessor(otlp_exporter)
# )
#
# # Instrument Flask app with OpenTelemetry middleware to trace requests
# FlaskInstrumentor().instrument_app(app)
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
#     app.run(debug=True, port=80)
