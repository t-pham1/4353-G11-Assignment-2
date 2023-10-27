import unittest
from flask_testing import TestCase
from app import app, db, UserCredentials

class TestQuoteRoute(TestCase):
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
        
        self.client.post('/quote', data=dict(gallons=100,
                                             deliveryDate='2023-11-01'), follow_redirects=True)

    def tearDown(self):
        self.client.get('/logout', follow_redirects=True)
        
        test_user = UserCredentials.query.filter_by(username='testuser').first()
        if test_user:
            db.session.delete(test_user)
            db.session.commit()

    def test_quote_access_with_completed_profile(self):
        fullName = 'testuser'
        addressOne = '123 St'
        addressTwo = '345 Dr'
        city = 'Houston'
        state = 'TX'
        zipcode = '77092'

        gallons = 100
        deliveryDate = '2023-11-01'

        self.client.post('/profile', data=dict(fullName=fullName,
                                                        addressOne=addressOne,
                                                        addressTwo=addressTwo,
                                                        city=city,
                                                        state=state,
                                                        zipcode=zipcode), follow_redirects=True)
        
        response = self.client.post('/quote', data=dict(gallons=gallons,
                                             deliveryDate=deliveryDate), follow_redirects=True)
        
        self.assertIn(addressOne.encode(), response.data)
        self.assertIn(addressTwo.encode(), response.data)
        self.assertIn(b'Form complete.', response.data)
    
    def test_quote_access_with_incomplete_profile(self):
        response = self.client.get('/quote', follow_redirects=True)
        self.assertIn(b'Please complete profile before getting a quote.', response.data)

if __name__ == '__main__':
    unittest.main()