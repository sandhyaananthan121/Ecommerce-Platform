from flask import Flask, render_template

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

if __name__ == '__main__':
    app.run(debug=True)
