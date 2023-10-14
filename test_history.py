import unittest
from app import app

class TestHistoryPage(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
    
    def test_history_access(self):
        response = self.app.get('/history')
        self.assertEqual(response.status_code, 200)
    
    def test_history_no_access(self):
        response = self.app.get('/history')
        self.assertEqual(response.status_code, 302)

    def test_history_logged_in(self):
        with self.app.session_transaction() as session:
            session['username'] = 'testuser'

        response = self.app.get('/history')

        self.assertEqual(response.status_code, 200)

    def test_history_not_logged_in(self):
        response = self.app.get('/history', follow_redirects=True)
        self.assertIn(b'You are not currently logged in.', response.data)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()