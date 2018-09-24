from flask import Flask, request, jsonify
from mlapi.logger.logger_factory import LoggerFactory
from mlapi.MLJsonEncoder import MLJsonEncoder
app = Flask(__name__)
app.json_encoder = MLJsonEncoder

@app.route('/ML/Analyze',  methods=['POST'])
def ml_analyze():
    documentsUri = request.get_json()
    questions = []
    return jsonify(questions)

if __name__ == '__main__':
    LoggerFactory.get_logger(__name__).info("API started")
    app.run(host = '0.0.0.0')