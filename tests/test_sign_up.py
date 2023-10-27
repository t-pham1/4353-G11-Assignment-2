import unittest
from flask_testing import TestCase
from app import app, db, UserCredentials

class TestSignupRoute(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
        return app

    def setUp(self):
        username = 'testuser'
        password = 'testpassword'

        self.client.post('/sign_up', data=dict(username=username,
                                               password=password), follow_redirects=True)

    def tearDown(self):
        self.client.get('/logout', follow_redirects=True)

        test_users = ['testuser', 'testuser1']

        for test_user in test_users:
            user = UserCredentials.query.filter_by(username=test_user).first()
            if user:
                db.session.delete(user)
        
        db.session.commit()

    def test_sign_up_access(self):
        response = self.client.get('/sign_up', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_sign_up_with_unique_username(self):
        username = 'testuser1'
        password = 'testpassword'

        response = self.client.post('/sign_up', data=dict(username=username,
                                               password=password), follow_redirects=True)
        
        self.assertIn(b'Registration complete.', response.data)
    
    def test_sign_up_with_existing_username(self):
        username = 'testuser'
        password = 'testpassword'

        response = self.client.post('/sign_up', data=dict(username=username,
                                               password=password), follow_redirects=True)
        
        self.assertIn(b'Username already exists.', response.data)

if __name__ == '__main__':
    unittest.main()