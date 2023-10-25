import unittest
from app import app, db, UserCredentials
from flask_testing import TestCase
from werkzeug.security import generate_password_hash, check_password_hash

class FlaskTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'
        app.config['WTF_CSRF_ENABLED'] = False  # To simplify form submissions
        return app

    def setUp(self):
        with app.app_context():
            db.create_all()
            hashed_password = generate_password_hash("testing", method='hello123')
            test_user = UserCredentials(username="test", password=hashed_password)
            db.session.add(test_user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_correct_login(self):
        response = self.client.post("/login", 
                                    data={"username": "test", "password": "testing"},
                                    follow_redirects=True)
        self.assertIn(b'Login successful.', response.data)

    def test_wrong_password_login(self):
        response = self.client.post("/login", 
                                    data={"username": "test", "password": "wrongpass"},
                                    follow_redirects=True)
        self.assertIn(b'Incorrect password.', response.data)

if __name__ == "__main__":
    unittest.main()

