from flask import Flask, request, jsonify
from mlapi.logger.logger_factory import LoggerFactory
from mlapi.serialization.object_encoder import ObjectEncoder
from mlapi.model.facet import Facet

app = Flask(__name__)
app.json_encoder = ObjectEncoder


@app.route('/ML/Analyze', methods=['POST'])
def ml_analyze():
    documentsUri = request.get_json()
    questions = []
    return jsonify(questions)


@app.route('/ML/Filter/Facets', methods=['POST'])
def filter_document_by_facets():
    content = request.get_json()
    documents = content['Documents']
    mustHaveFacets = [Facet(val['Name'], val['Value']) for val in content['MustHaveFacets']]
    mustNotHaveFacets = [Facet(val['Name'], val['Value']) for val in content['MustNotHaveFacets']]
    return jsonify()


if __name__ == '__main__':
    LoggerFactory.get_logger(__name__).info("API started")
    app.run(host='0.0.0.0')
