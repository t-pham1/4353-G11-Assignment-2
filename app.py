from flask import Flask, render_template, url_for, request, redirect, flash, session

app = Flask(__name__)
app.secret_key = "5473895728547392"

hardcodeUsername = "username"
hardcodePassword = "password"

class PricingModule:
    def __init__(self):
        pass
    
    def get_price_per_gallon(self):
        hardcodePrice = 2.5
        return hardcodePrice

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == hardcodeUsername:
            if password == hardcodePassword:
                flash('Login successful.', category='success')
                return redirect(url_for('index'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('Username does not exist.', category='error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
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

            flash('Profile complete.', category='success')

    return render_template('profile.html')

@app.route('/sign_up', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(username + ' ' + password)

        if len(username) < 1:
            flash('Please enter a username.', category='error')
        elif len(password) < 1:
            flash('Please enter a password.', category='error') 
        else:
            flash('Registration complete.', category='success')
            return redirect(url_for('login'))
        
    return render_template('sign_up.html')

pricing_module = PricingModule()

@app.route('/quote', methods = ['GET', 'POST'])
def quote():
    addressOne = session.get('addressOne', '')
    addressTwo = session.get('addressTwo', '')
    
    if request.method == 'POST':
        if 'addressOne' in session:
            addressOne = session['addressOne']
        elif 'addressTwo' in session:
            addressTwo = session['addressTwo']
        elif 'addressOne' in session and 'addressTwo' in session:
            addressOne = session['addressOne']
            addressTwo = session['addressTwo']
        else:
            flash('Please complete your profile first.', category='error')
            return redirect(url_for('profile'))
        
        gallons = float(request.form.get('gallons'))
        delivery_date = request.form.get('deliveryDate')
        price_per_gallon = pricing_module.get_price_per_gallon()
        total_amount_due = gallons * price_per_gallon
        # print(str(gallons) + ' ' + addressOne + ' ' + addressTwo + ' ' + delivery_date + ' ' + str(price_per_gallon) + ' ' + str(total_amount_due))

        if gallons <= 0:
            flash('Please enter a valid number of gallons.', category='error')
        else:
            flash('Form complete.', category='success')

    return render_template('quote.html',
                           addressOne=addressOne,
                           addressTwo=addressTwo)

@app.route('/history')
def history():
    return render_template('history.html')

if __name__ == '__main__':
    app.run(debug=True)