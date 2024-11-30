from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

@app.route('/expenses', methods=['GET'])
def get_expenses():
    expenses = Expense.query.all()
    return jsonify([{
        "id": expense.id,
        "category": expense.category,
        "description": expense.description,
        "amount": expense.amount,
        "date": expense.date.strftime('%Y-%m-%d')
    } for expense in expenses])

@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.get_json()
    new_expense = Expense(
        category=data['category'],
        description=data['description'],
        amount=data['amount'],
        date=datetime.strptime(data['date'], '%Y-%m-%d')
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({"message": "Expense added successfully"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
