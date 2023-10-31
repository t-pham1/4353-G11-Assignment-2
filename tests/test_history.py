import unittest
from flask_testing import TestCase
from app import app, db, UserCredentials, PricingModule

#test1

class TestHistoryRoute(TestCase):
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

    def test_history_access(self):
        response = self.client.get('/history', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_history_after_quote_submission(self):
        fullName = 'testuser'
        addressOne = '123 St'
        addressTwo = '345 Dr'
        city = 'Houston'
        state = 'TX'
        zipcode = '77092'

        pricing_module = PricingModule()
        gallons = 100
        deliveryDate = '2023-11-01'
        pricePerGallon = pricing_module.get_price_per_gallon()
        totalAmountDue = gallons * pricePerGallon

        self.client.post('/profile', data=dict(fullName=fullName,
                                                        addressOne=addressOne,
                                                        addressTwo=addressTwo,
                                                        city=city,
                                                        state=state,
                                                        zipcode=zipcode), follow_redirects=True)
        
        self.client.post('/quote', data=dict(gallons=gallons,
                                             deliveryDate=deliveryDate), follow_redirects=True)
        
        response = self.client.get('/history', follow_redirects=True)
        self.assertIn(str(gallons).encode(), response.data)
        self.assertIn(addressOne.encode(), response.data)
        self.assertIn(addressTwo.encode(), response.data)
        self.assertIn(deliveryDate.encode(), response.data)
        self.assertIn(str(pricePerGallon).encode(), response.data)
        self.assertIn(str(totalAmountDue).encode(), response.data)

if __name__ == '__main__':
    unittest.main()