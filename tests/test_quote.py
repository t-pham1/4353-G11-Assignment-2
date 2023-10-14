import unittest
from app import app, PricingModule

class TestQuote(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_quote_access(self):
        response = self.app.get('/quote')
        self.assertEqual(response.status_code, 200)
    
    def test_quote_no_access(self):
        response = self.app.get('/quote')
        self.assertEqual(response.status_code, 302)
    
    def test_quote_submission(self):
        data = {'gallons': '10',
                'deliveryDate': '2023-10-20'}

        response = self.app.post('/quote', data=data, follow_redirects=True)
        self.assertIn(b'Form complete.', response.data)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()