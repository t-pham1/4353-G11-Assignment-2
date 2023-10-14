import unittest
from app import app

class TestProfile(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_profile_access(self):
        response = self.app.get('/profile')
        self.assertEqual(response.status_code, 200)
    
    def test_profile_no_access(self):
        response = self.app.get('/profile')
        self.assertEqual(response.status_code, 302)
    
    def test_profile_submission(self):
        data = {'fullName': 'Mr. Krabs',
                'addressOne': '123 street',
                'addressTwo': '456 street',
                'city': 'Houston',
                'state': 'TX',
                'zipcode': '77005'}

        response = self.app.post('/profile', data=data, follow_redirects=True)
        self.assertIn(b'Form complete.', response.data)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()