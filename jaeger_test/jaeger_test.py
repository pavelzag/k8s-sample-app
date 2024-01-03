import requests
from opentracing import Tracer, Format
from jaeger_client import Config


def init_tracer(service_name):
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service_name,
    )
    return config.initialize_tracer()


def make_request(url, operation_name, tracer):
    with tracer.start_span(operation_name) as span:
        span.set_tag('http.method', 'GET')
        span.set_tag('span.type', 'http')
        span.set_tag('http.url', url)

        response = requests.get(url)

    return response


if __name__ == "__main__":
    # Replace with the URL of your Flask application
    flask_app_url = "http://172.17.83.119"

    # Initialize Jaeger tracer
    tracer = init_tracer('jaeger_test_client')

    # Make requests to the Flask app and trace them
    response_hello = make_request(f"{flask_app_url}/hello", 'call_hello_world', tracer)
    print(response_hello.text)

    response_square = make_request(f"{flask_app_url}/square/5", 'call_square', tracer)
    print(response_square.text)

    response_fibonacci = make_request(f"{flask_app_url}/fibonacci/5", 'generate_fibonacci', tracer)
    print(response_fibonacci.json())

    # Additional requests to test tracing for endpoints with different status codes
    response_not_found = make_request(f"{flask_app_url}/not_found", 'not_found', tracer)
    print(response_not_found.status_code)

    response_internal_server_error = make_request(f"{flask_app_url}/internal_server_error", 'internal_server_error',
                                                  tracer)
    print(response_internal_server_error.status_code)

    # Close the tracer to flush any remaining traces
    tracer.close()
