import unittest
from app import app

class TestLogout(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
    
    def test_log_out_access(self):
        response = self.app.get('/log_out')
        self.assertEqual(response.status_code, 200)
    
    def test_log_out_no_access(self):
        response = self.app.get('/log_out')
        self.assertEqual(response.status_code, 302)

    def test_logout_logged_in(self):
        with self.app.session_transaction() as session:
            session['username'] = 'testuser'

        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'You have been logged out.', response.data)
        self.assertEqual(response.status_code, 200)

    def test_logout_not_logged_in(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'You are not currently logged in.', response.data)
        self.assertEqual(response.status_code, 200)

    def test_protected_page_after_logout(self):
        with self.app.session_transaction() as session:
            session['username'] = 'testuser'

        self.app.get('/logout', follow_redirects=True)
        response = self.app.get('/profile', follow_redirects=True)
        self.assertIn(b'You are not currently logged in.', response.data)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()