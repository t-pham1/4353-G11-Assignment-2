from flask import Flask, render_template, url_for, request, flash

app = Flask(__name__)
app.secret_key = "5473895728547392"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # if username in username database and password is correct:
        # flash('Login successful.', category='success')

    return render_template('login.html')

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

        flash('Profile complete.', category='success')

    return render_template('profile.html')

@app.route('/sign_up', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # print(username + ' ' + password)

        if len(username) < 1:
            flash('Please enter a username.', category='error')
        elif len(password) < 1:
            flash('Please enter a password.', category='error') 
        else:

            flash('Registration complete.', category='success')
        
    return render_template('sign_up.html')

@app.route('/quote', methods = ['GET', 'POST'])
def quote():
    return render_template('quote.html')

@app.route('/history')
def history():
    return render_template('history.html')

if __name__ == '__main__':
    app.run(debug=True)