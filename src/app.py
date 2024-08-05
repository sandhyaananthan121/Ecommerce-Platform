from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample product data
products = [
    {
        'name': 'Product 1',
        'price': '$10.00',
        'description': 'Description of Product 1'
    },
    {
        'name': 'Product 2',
        'price': '$20.00',
        'description': 'Description of Product 2'
    },
    {
        'name': 'Product 3',
        'price': '$30.00',
        'description': 'Description of Product 3'
    }
]

@app.route('/')
def home():
    return render_template('index.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Here you would typically check the username and password
        username = request.form['username']
        password = request.form['password']
        # Dummy check for demonstration purposes
        if username == 'admin' and password == 'password':
            return redirect(url_for('home'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
