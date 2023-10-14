import unittest
from app import app

class TestSignUp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_sign_up_access(self):
        response = self.app.get('/sign_up')
        self.assertEqual(response.status_code, 200)
    
    def test_sign_up_no_access(self):
        response = self.app.get('/sign_up')
        self.assertEqual(response.status_code, 302)
    
    def test_sign_up_submission(self):
        data = {'username': 'username',
                'password': 'password'}

        response = self.app.post('/sign_up', data=data, follow_redirects=True)
        self.assertIn(b'Form complete.', response.data)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()