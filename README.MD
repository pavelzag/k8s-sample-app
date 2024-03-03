# K8S Sample App
## _The best application in the world to test K8S_

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)



[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

K8S Sample App is a small Python Flask based application the checks that your Kubernetes Cluster is configured properly

## Features

- **Framework**: Flask
- **Extensions**:
  - Flask-RESTx for API operations
  - PyYAML for YAML file operations
- **Configuration**: The application is configured to run on a specific server name.
- **Functionality**: The API includes routes for basic mathematical operations and a Fibonacci sequence generator.

## Application Setup

1. **Flask Application Initialization**:
   - Flask app instance creation.
   - Configuration of the server name.
   - Initialization of the Flask-RESTx API with versioning and description.

2. **Namespace**: A namespace for the main operations (`api`) is defined to organize the endpoints.

## Utility Functions

- **Conversion of OrderedDict to Dict**: A recursive function to convert Python's `OrderedDict` objects to standard `dict` objects.
- **OpenAPI YAML Generation**:
  - Generates an OpenAPI specification YAML file.
  - Utilizes the Flask application context.
  - Converts the Flask-RESTx schema to a regular dictionary and dumps it into a YAML file.

## Mathematical Operations

1. **Square**: Returns the square of a given number.
2. **Cube**: Returns the cube of a given number.
3. **Fibonacci Sequence**: Generates a Fibonacci sequence up to a specified length.

## API Endpoints

### Index Page

- **Endpoint**: `/`
- **Method**: GET
- **Description**: Serves an "Under Construction" HTML page.

### Hello World

- **Endpoint**: `/hello`
- **Method**: GET
- **Description**: Returns a simple "Hello, World" message in JSON format.

### Square

- **Endpoint**: `/square/<int:num>`
- **Method**: GET
- **Description**: Returns the square of the specified number in JSON format.

### Cube

- **Endpoint**: `/cube/<int:num>`
- **Method**: GET
- **Description**: Returns the cube of the specified number in JSON format.

### Fibonacci Sequence

- **Endpoint**: `/fibonacci/<int:n>`
- **Method**: GET
- **Description**: Returns a Fibonacci sequence up to the specified length in JSON format.

## Running the Application

The application can be started with Flask's built-in server by calling `app.run()`, specifying the host, port, and debug mode. Additionally, the OpenAPI YAML file is generated on application startup.

- 💰 Cash 💰
- 💰 Rules 💰
- 💰 Everything 💰
- 💰 Around 💰
- 💰 Me 💰

