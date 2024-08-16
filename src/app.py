from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Product

app = Flask(__name__)
app.config['SECRET_KEY'] = '12i323uy3ut132ui1'  # Replace with a strong secret key in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.cli.command('create-db')
def create_db():
    db.create_all()
    print('Database tables created.')

@app.cli.command('seed-db')
def seed_db():
    if not User.query.filter_by(username='admin').first():
        admin_user = User(username='admin')
        admin_user.set_password('password')
        db.session.add(admin_user)

    if not User.query.filter_by(username='user1').first():
        user1 = User(username='sandhya')
        user1.set_password('sandhu2000')
        db.session.add(user1)

    if Product.query.count() == 0:
        products = [
            Product(name='Product 1', description='Description of Product 1', price=10.0),
            Product(name='Product 2', description='Description of Product 2', price=20.0),
            Product(name='Product 3', description='Description of Product 3', price=30.0),
            Product(name='Product 4', description='Description of Product 4', price=10.0),
            Product(name='Product 5', description='Description of Product 5', price=20.0),
            Product(name='Product 6', description='Description of Product 6', price=30.0),
            Product(name='Product 7', description='Description of Product 7', price=10.0),
            Product(name='Product 8', description='Description of Product 8', price=20.0),
        ]
        db.session.add_all(products)

    db.session.commit()
    print('Database seeded.')

@app.context_processor
def inject_user():
    return dict(username=session.get('username'))

@app.route('/')
def home():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_form = request.form['username']
        password_form = request.form['password']
        user = User.query.filter_by(username=username_form).first()
        if user and user.check_password(password_form):
            session['username'] = user.username
            flash('Successfully logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username_form = request.form['username']
        password_form = request.form['password']
        user = User.query.filter_by(username=username_form).first()
        if user:
            flash('Username already exists. Please choose another.', 'danger')
        else:
            new_user = User(username=username_form)
            new_user.set_password(password_form)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully. Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Successfully logged out!', 'success')
    return redirect(url_for('home'))


@app.route('/products', methods=['GET'])
def products():
    category = request.args.get('category')
    max_price = request.args.get('price')

    query = Product.query

    if category:
        query = query.filter_by(category=category)

    if max_price:
        query = query.filter(Product.price <= float(max_price))

    products = query.all()
    return render_template('products.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
