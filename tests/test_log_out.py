import unittest
from flask_testing import TestCase
from app import app, db, UserCredentials

class TestLogoutRoute(TestCase):
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

    def test_log_out(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Successfully signed out!', response.data)

if __name__ == '__main__':
    unittest.main()