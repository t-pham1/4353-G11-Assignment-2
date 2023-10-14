import unittest
from app import app

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_login_access(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
    
    def test_login_no_access(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 302)
    
    def test_login_submission(self):
        data = {'username': 'username',
                'password': 'password'}

        response = self.app.post('/login', data=data, follow_redirects=True)
        self.assertIn(b'Form complete.', response.data)
        self.assertEqual(response.status_code, 200)
    
    def test_successful_login(self):
        data = {'username': 'username',
                'password': 'password'}

        response = self.app.post('/login', data=data, follow_redirects=True)
        self.assertIn(b'Login successful.', response.data)
        self.assertEqual(response.status_code, 200)
    
    def test_incorrect_password(self):
        data = {'username': 'username',
                'password': 'wrong_password'}
        response = self.app.post('/login', data=data, follow_redirects=True)
        
        self.assertIn(b'Incorrect password.', response.data)
        self.assertEqual(response.status_code, 200)
    
    def test_nonexistent_username(self):
        data = {'username': 'nonexistent_user',
                'password': 'password'}
        response = self.app.post('/login', data=data, follow_redirects=True)
        
        self.assertIn(b'Username does not exist.', response.data)
        self.assertEqual(response.status_code, 200)
    
    def test_already_logged_in(self):
        with self.app.session_transaction() as session:
            session['username'] = 'testuser'

        response = self.app.get('/login', follow_redirects=True)
        self.assertIn(b'You are already signed in!', response.data)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()