# netlify/functions/flask_function.py
import json
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Hello, Netlify!")

def handler(event, context):
    from flask import request
    from werkzeug.datastructures import Headers
    from werkzeug.wrappers import Request

    headers = Headers(event['headers'])
    body = event.get('body', '')

    request = Request({
        'wsgi.url_scheme': 'http',
        'REQUEST_METHOD': event['httpMethod'],
        'PATH_INFO': event['path'],
        'QUERY_STRING': '',
        'CONTENT_TYPE': headers.get('content-type', ''),
        'wsgi.input': body,
        'CONTENT_LENGTH': headers.get('content-length', '0'),
        'SERVER_NAME': 'localhost',
        'SERVER_PORT': '5000',
        'HTTP_HOST': headers.get('host', ''),
        'HTTP_USER_AGENT': headers.get('user-agent', ''),
    }, headers=headers)

    response = app.full_dispatch_request()
    return {
        'statusCode': response.status_code,
        'body': response.data.decode('utf-8'),
        'headers': dict(response.headers)
    }
