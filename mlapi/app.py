from flask import Flask
from mlapi.logger.logger_factory import LoggerFactory
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World!"

if __name__ == '__main__':
    LoggerFactory.get_logger(__name__).info("API started")
    app.run(host = '0.0.0.0')