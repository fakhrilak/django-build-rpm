import requests
import requests_staticmock
import json


class MyTestClass(requests_staticmock.BaseMockClass):
    def _api_v1_idea(self, request):
        return json.dumps({
            "test":"1"
        })

session = requests.Session()
with requests_staticmock.mock_session_with_class(session, MyTestClass, 'http://test_context.com'):
    # will return a response object with the contents 'woop woop'
    response = session.request('get', 'http://test_context.com/api/v1/idea')
    session.close()
    print(json.loads(response.text))