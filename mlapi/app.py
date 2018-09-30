from flask import Flask, request, jsonify

from mlapi.document_filter import DocumentFilter
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
    must_have_facets = [Facet(val['Name'], val['Value']) for val in content['MustHaveFacets']]
    must_not_have_facets = [Facet(val['Name'], val['Value']) for val in content['MustNotHaveFacets']]

    documents = DocumentFilter.keep_documents_with_facets(documents, must_have_facets)
    documents = DocumentFilter.keep_documents_without_facets(documents, must_not_have_facets)

    return jsonify(documents)


if __name__ == '__main__':
    LoggerFactory.get_logger(__name__).info("API started")
    app.run(host='0.0.0.0')
