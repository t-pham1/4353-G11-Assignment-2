import unittest
from flask_testing import TestCase
from app import app, db, UserCredentials

class TestProfileRoute(TestCase):
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

    def test_profile_access(self):
        response = self.client.get('/profile', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_profile_completed_successfully(self):
        fullName = 'testuser'
        addressOne = '123 St'
        addressTwo = '345 Dr'
        city = 'Houston'
        state = 'TX'
        zipcode = '77092'

        response = self.client.post('/profile', data=dict(fullName=fullName,
                                                        addressOne=addressOne,
                                                        addressTwo=addressTwo,
                                                        city=city,
                                                        state=state,
                                                        zipcode=zipcode), follow_redirects=True)
        self.assertIn(b'Updated profile.', response.data)

if __name__ == '__main__':
    unittest.main()