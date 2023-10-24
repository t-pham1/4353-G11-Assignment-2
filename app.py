from flask import Flask, render_template, url_for, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = "5473895728547392"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    fullName = db.Column(db.String(50))
    addressOne = db.Column(db.String(100))
    addressTwo = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.Integer)

    quotes = db.relationship('Quote')

    # def init(self, username, password):
    #     self.username = username
    #     self.password = password
    # def repr(self):
    #     return '<Username %r>' % self.username

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gallons = db.Column(db.Integer)
    deliveryDate = db.Column(db.String(10))
    # may need to add other information related to this class for quote

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

hardcodeUsername = "admin"
hardcodePassword = "password"

class User1:
    def __init__(self, id, username, password):
        self.id = 1
        self.username = username
        self.password = password
    
    def __repr__(self):
        return f'<User: {self.id}, {self.username}, {self.password}>'


users = []
users.append(User1(id=1, username=hardcodeUsername, password=hardcodePassword))

class PricingModule:
    def __init__(self):
        self.hardcodePrice = 2.5
        self.quote_id = 1
        self.quote_history = []
    
    def get_price_per_gallon(self):
        # hardcodePrice = 2.5
        return self.hardcodePrice
    
    def update_quote_history(self, quote_details):
        quote_details['quote_id'] = self.quote_id
        self.quote_id += 1
        self.quote_history.append(quote_details)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if session["username"] != None:
        flash('You are already signed in! Please log out before trying to login into another account.', category='error')
        return render_template('sign_up.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            user = [x for x in users if x.username == username][0]  # user contains ID number
        except IndexError:
            flash('Username does not exist.', category='error')
            return render_template('login.html')
        
        if user and user.password == password and check_password_hash(user.password, password):
            session["username"] = username
            flash('Login successful.', category='success')
            return redirect(url_for('index'))
        elif user and user.password != password:
            flash('Incorrect password.', category='error')
    
    return render_template('login.html')

@app.route('/logout')
#@login_required
def logout():
 #   logout_user
    session["username"] = None
    return redirect(url_for('index'))

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    if session['username'] == None:
        flash("User is not signed in! Please login before accessing the profile\'s page.", category='error')
        return render_template('profile.html')
    else:
        if request.method == 'POST':
            fullName = request.form.get('fullName')
            addressOne = request.form.get('addressOne')
            addressTwo = request.form.get('addressTwo')
            city = request.form.get('city')
            state = request.form.get('state')
            zipcode = request.form.get('zipcode')
            # print(fullName + ' ' + addressOne + ' ' + addressTwo + ' ' + city + ' ' + state + ' ' + zipcode)

            if len(fullName) <= 0:
                flash('Full Name must be at least 1 character long.', category='error')
            elif len(fullName) > 50:
                flash('Full Name can be at most 50 characters long.', category='error')
            elif len(addressOne) <= 0:
                flash('Address 1 must be at least 1 character long.', category='error')
            elif len(addressOne) > 100:
                flash('Address 1 can be at most 100 characters long.', category='error')
            elif len(addressTwo) > 100:
                flash('Address 2 can be at most 100 characters long.', category='error')
            elif len(city) > 100:
                flash('City can be at most 100 characters long.', category='error')
            elif len(zipcode) < 5:
                flash('Zipcode must be at least 5 digits long.', category='error')
            elif len(zipcode) > 9:
                flash('Zipcode can be at most 9 digits long.', category='error')
            else:
                session['addressOne'] = request.form.get('addressOne')
                session['addressTwo'] = request.form.get('addressTwo')

                flash('Updated profile.', category='success')
        return render_template('profile.html')

@app.route('/sign_up', methods = ['GET', 'POST'])
def sign_up():
    if session["username"] != None:
        flash('You are already signed in!', category='error')
        return render_template('sign_up.html')
    if request.method == 'POST':
        
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username = username).first()
        if user:
            # testing user = [x for x in users if x.username == username][0]  # user contains ID number
            flash('Username already exists.', category='error')
            return render_template('sign_up.html')
        if len(username) < 1:
            flash('Please enter a username.', category='error')
        elif len(password) < 1:
                flash('Please enter a password.', category='error')
        else:
                #users.append(User(id=0, username=username, password=password))
                #users[len(users)-1].id = len(users)
                # print(users)
            new_user = User(username=username, password = generate_password_hash(password, method ='sha256'))
            db.session.add(new_user)
            db.session.commit()
            #login_user(new_user, remember=True)
            flash('Registration complete.', category='success')
            return redirect(url_for('login'))
        
        return render_template('sign_up.html')
        
    return render_template('sign_up.html', user=current_user)

pricing_module = PricingModule()

@app.route('/quote', methods = ['GET', 'POST'])
def quote():
    addressOne = session.get('addressOne', '')
    addressTwo = session.get('addressTwo', '')
    
    if request.method == 'POST':
        gallons = float(request.form.get('gallons'))
        delivery_date = request.form.get('deliveryDate')
        price_per_gallon = pricing_module.get_price_per_gallon()
        total_amount_due = gallons * price_per_gallon
        # print(str(gallons) + ' ' + addressOne + ' ' + addressTwo + ' ' + delivery_date + ' ' + str(price_per_gallon) + ' ' + str(total_amount_due))

        if gallons <= 0:
            flash('Please enter a valid number of gallons.', category='error')
        else:
            quote_details = {
                'quote_id': None,
                'gallons': gallons,
                'addressOne': addressOne,
                'addressTwo': addressTwo,
                'delivery_date': delivery_date,
                'price_per_gallon': price_per_gallon,
                'total_amount_due': total_amount_due
            }
            
            pricing_module.update_quote_history(quote_details)
            flash('Form complete.', category='success')

    return render_template('quote.html',
                           addressOne=addressOne,
                           addressTwo=addressTwo)

@app.route('/history')
def history():
    return render_template('history.html',
                           fuel_quote=pricing_module.quote_history)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)