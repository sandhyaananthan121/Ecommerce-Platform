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
@app.cli.command('drop-db')
def drop_db():
    db.drop_all()
    print('Database tables dropped.')

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
            Product(name='Product 1', description='Description of Product 1', price=10.0, image_filename='static/pics/s33.jpg'),
            Product(name='Product 2', description='Description of Product 2', price=20.0, image_filename='static/pics/s2.jpg'),
            Product(name='Product 3', description='Description of Product 3', price=30.0, image_filename='static/pics/s3.jpg'),
            Product(name='Product 4', description='Description of Product 4', price=10.0, image_filename='static/pics/s4.jpg'),
            Product(name='Product 5', description='Description of Product 5', price=20.0, image_filename='static/pics/s5.jpg'),
            Product(name='Product 6', description='Description of Product 6', price=30.0, image_filename='static/pics/s6.jpg'),
            Product(name='Product 7', description='Description of Product 7', price=10.0, image_filename='static/pics/s7.jpg'),
            Product(name='Product 8', description='Description of Product 8', price=20.0, image_filename='static/pics/s8.jpg'),
            Product(name='Product 9', description='Description of Product 9', price=101.0, image_filename='static/pics/s9.jpg'),
            Product(name='Product 10', description='Description of Product 10', price=201.0, image_filename='static/pics/s10.jpg'),
            Product(name='Product 11', description='Description of Product 11', price=130.0, image_filename='static/pics/s11.jpg'),
            Product(name='Product 12', description='Description of Product 12', price=910.0, image_filename='static/pics/s12.jpg'),
            Product(name='Product 13', description='Description of Product 13', price=200.0, image_filename='static/pics/s13.jpg'),
            Product(name='Product 14', description='Description of Product 14', price=300.0, image_filename='static/pics/s14.jpg'),
            Product(name='Product 15', description='Description of Product 15', price=90.0, image_filename='static/pics/s15.jpg'),
            Product(name='Product 16', description='Description of Product 16', price=800.0, image_filename='static/pics/s16.jpg'),
            Product(name='Product 17', description='Description of Product 17', price=100.0, image_filename='static/pics/s17.jpg'),
            Product(name='Product 18', description='Description of Product 18', price=220.0, image_filename='static/pics/s18.jpg'),
            Product(name='Product 19', description='Description of Product 19', price=330.0, image_filename='static/pics/s19.jpg'),
            Product(name='Product 20', description='Description of Product 20', price=108.0, image_filename='static/pics/s20.jpg'),
            Product(name='Product 21', description='Description of Product 21', price=209.0, image_filename='static/pics/s21.jpg'),
            Product(name='Product 22', description='Description of Product 22', price=300.0, image_filename='static/pics/s22.jpg'),
            Product(name='Product 23', description='Description of Product 23', price=10.0, image_filename='static/pics/s23.jpg'),
            Product(name='Product 24', description='Description of Product 24', price=20.0, image_filename='static/pics/s24.jpg'),
            Product(name='Product 25', description='Description of Product 25', price=10.0, image_filename='static/pics/s25.jpg'),
            Product(name='Product 26', description='Description of Product 26', price=200.0, image_filename='static/pics/s26.jpg'),
            Product(name='Product 27', description='Description of Product 27', price=3000.0, image_filename='static/pics/s27.jpg'),
            Product(name='Product 28', description='Description of Product 28', price=109.0, image_filename='static/pics/s28.jpg'),
            Product(name='Product 29', description='Description of Product 29', price=208.0, image_filename='static/pics/s29.jpg'),
            Product(name='Product 30', description='Description of Product 30', price=301.0, image_filename='static/pics/s30.jpg'),
            Product(name='Product 31', description='Description of Product 31', price=10.90, image_filename='static/pics/s31.jpg'),
            Product(name='Product 32', description='Description of Product 32', price=200.0, image_filename='static/pics/s32.jpg'),
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

if __name__ == '__main__:
    app.run(host='0.0.0.0', port=5000)
    #app.run(debug=True)
