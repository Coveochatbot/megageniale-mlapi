from mlapi import app
from flask import json
import unittest


class FlaskTest(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True

    def test_facets_endpoint(self):
        documents = ['dfsdf', 'sdfsdf','sdfsdf','fsdfsdf']
        result = self.app.post('/ML/Analyze', data=json.dumps(documents), content_type='application/json')
        self.assertEqual(result.status_code, 200)


if __name__ == '__main__':
    unittest.main()