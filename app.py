from flask import Flask, render_template, url_for, request, redirect, flash

app = Flask(__name__)
app.secret_key = "5473895728547392"

hardcodeUsername = "username"
hardcodePassword = "password"

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
                flash('Incorrect password', category='error')
        else:
            flash('Username does not exist', category='error')

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

@app.route('/quote', methods = ['GET', 'POST'])
def quote():
    return render_template('quote.html')

@app.route('/history')
def history():
    return render_template('history.html')

if __name__ == '__main__':
    app.run(debug=True)