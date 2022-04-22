import unittest
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class TestWebhook(unittest.TestCase):
    '''
    La mayoría de clases/metodos build no están completamente desarrollados, ya que estos tests son inciales, no
    son muy amplios
    '''

    @classmethod 
    def setUpClass(cls): # This function will be excecuted at the beggining of the program, only once time, example of use: create a database
        pass


    @classmethod
    def tearDownClass(cls): # This function will be excecuted at the end of the excecution of the program. only once time
        pass

    def setUp(self): # this code runs before every single test, for not being declaring two employees in every test
        self.token = os.getenv('MESSENGER_VERIFY_TOKEN')
        self.url = 'https://meta-apis-consumer.herokuapp.com/webhook'

    def tearDown(self): # this code runs after every single test
        pass

    def test_get(self):
        print('Test - GET Request - Token validation')
        
        ok_url = self.url + '?hub.challenge=CHALLENGE_ACCEPTED&hub.mode=subscribe&hub.verify_token=' + str(self.token)
        print(ok_url)
        ok_request = requests.get(url = ok_url)
        bad_request = requests.get(url = self.url + '?hub.verify_token=NotARealToken&hub.challenge=CHALLENGE_ACCEPTED&hub.mode=subscribe')
        
        # atributo 'ok' de un request.models.Response devuelve True si la respuesta fue Response[200]
        self.assertTrue(ok_request.ok) 
        self.assertFalse(bad_request.ok)


    def test_post(self):
        print('Test - POST Request - Receiving Messages Validation')

        # Recreo el siguiente curl 
        # curl -H "Content-Type: application/json" -X POST "https://meta-apis-consumer.herokuapp.com/webhook" -d '{"object": "page", "entry": [{"messaging": [{"message": "TEST_MESSAGE"}]}]}'
        headers = {
            "content-type": "application/json"
        }
        data = '''{
            "object": "page", 
            "entry": [{"messaging": [{"message": "TEST_MESSAGE"}]}]
        }'''

        response = requests.post(url = self.url, headers = headers, data = data)

        self.assertTrue(response.ok)

if __name__ == '__main__':
    unittest.main()