from flask import Flask, request, jsonify

from definitions import Definitions
from mlapi.document_filter import DocumentFilter
from mlapi.model.facet import Facet
from mlapi.facet_extractor import FacetExtractor
from mlapi.logger.logger_factory import LoggerFactory
from mlapi.serialization.object_encoder import ObjectEncoder

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
    documents_to_filter = content['Documents']

    ############### Replace with actual dictionary when created
    extractor = FacetExtractor()
    all_documents = extractor.get_facets_by_document_in_directory(Definitions.FACETS_DIR)
    documents = dict((k, all_documents[k]) for k in documents_to_filter if k in all_documents)
    ###############

    if "MustHaveFacets" in content:
        must_have_facets = [Facet(val['Name'], val['Value']) for val in content['MustHaveFacets']]
        documents = DocumentFilter.keep_documents_with_facets(documents, must_have_facets)

    if "MustNotHaveFacets" in content:
        must_not_have_facets = [Facet(val['Name'], val['Value']) for val in content['MustNotHaveFacets']]
        documents = DocumentFilter.keep_documents_without_facets(documents, must_not_have_facets)

    return jsonify(list(documents.keys()))


if __name__ == '__main__':
    LoggerFactory.get_logger(__name__).info("API started")
    app.run(host='0.0.0.0')
