from flask import Flask, request, jsonify
from mlapi.logger.logger_factory import LoggerFactory
from mlapi.MLJsonEncoder import MLJsonEncoder
from mlapi.model.facet import Facet
app = Flask(__name__)
app.json_encoder = MLJsonEncoder

@app.route('/ML/Analyze',  methods=['POST'])
def ml_analyze():
    documentsUri = request.get_json()
    questions = []
    return jsonify(questions)

@app.route('/ML/Filter/Facets', methods=['POST'])
def filter_document_by_facets():
    content = request.get_json()
    documents = content['documents']
    mustHaveFacets = [Facet(val['name'], val['value']) for val in content['mustHaveFacets']]
    mustNotHaveFacets = [Facet(val['name'], val['value']) for val in content['mustNotHaveFacets']]
    return jsonify()

if __name__ == '__main__':
    LoggerFactory.get_logger(__name__).info("API started")
    app.run(host = '0.0.0.0')