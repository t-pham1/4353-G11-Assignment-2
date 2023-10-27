import unittest
from flask_testing import TestCase
from app import app, db, UserCredentials

class TestLoginRoute(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
        return app

    def setUp(self):
        username = 'testuser'
        password = 'testpassword'

        self.client.post('/sign_up', data=dict(username=username,
                                               password=password), follow_redirects=True)

        self.client.post('/login', data=dict(username=username,
                                             password=password), follow_redirects=True)

    def tearDown(self):
        self.client.get('/logout', follow_redirects=True)
        
        test_user = UserCredentials.query.filter_by(username='testuser').first()
        if test_user:
            db.session.delete(test_user)
            db.session.commit()

    def test_login_success(self):
        username = 'testuser'
        password = 'testpassword'

        response = self.client.post('/login', data=dict(username=username,
                                             password=password), follow_redirects=True)
        self.assertIn(b'Login successful.', response.data)
    
    def test_login_wrong_password(self):
        username = 'testuser'
        password = 'wrongpassword'

        response = self.client.post('/login', data=dict(username=username,
                                             password=password), follow_redirects=True)
        self.assertIn(b'Incorrect password.', response.data)
    
    def test_login_nonexistent_username(self):
        username = 'nonexistentuser'
        password = 'password'

        response = self.client.post('/login', data=dict(username=username,
                                             password=password), follow_redirects=True)
        self.assertIn(b'Username does not exist.', response.data)

if __name__ == '__main__':
    unittest.main()