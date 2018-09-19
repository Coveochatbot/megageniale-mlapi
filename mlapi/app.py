from flask import Flask, request, jsonify
from mlapi.logger.logger_factory import LoggerFactory
from mlapi.model.document import Document
from mlapi.MLJsonEncoder import MLJsonEncoder
app = Flask(__name__)
app.json_encoder = MLJsonEncoder

@app.route('/ML/Analyze',  methods=['POST'])
def ml_analyze():
    content = request.get_json()
    documents = [Document(val["Title"], val["Uri"], val["PrintableUri"], val["Summary"], val["Excerpt"]) for val in content]
    questions = []
    return jsonify(questions)

if __name__ == '__main__':
    LoggerFactory.get_logger(__name__).info("API started")
    app.run(host = '0.0.0.0')