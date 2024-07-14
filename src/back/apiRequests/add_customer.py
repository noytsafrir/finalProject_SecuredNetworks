import mysql.connector
from flask import Blueprint, request, jsonify
from models import db, Customer
from myfunc import *

add_customer_bp = Blueprint('add_customer_bp', __name__)

@add_customer_bp.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.get_json()
    customer_name = data.get('customer_name')
    company_name = data.get('company_name')
    address = data.get('address')

    # safe mode
    if safe_mode:
        existing_customer = Customer.query.filter_by(customer_name=customer_name).first()
        if existing_customer is not None:
            return jsonify({'message': 'Customer already exists', 'status': 400})

    # unsafe mode
    else:
        try:
            # Database connection setup
            unsecuredConnection, unsecuredCursor = set_unsecured_connection()
            query = f"SELECT * FROM customers WHERE customer_name = '{customer_name}';"
            # Executing the query with multi=True to allow multiple statements
            for result in unsecuredCursor.execute(query, multi=True):
                if result.with_rows:
                    res = result.fetchall()
                    if res:
                        close_unsecured_connection(unsecuredCursor, unsecuredConnection)
                        return jsonify({'message': 'Customer already exists', 'status': 400})
            close_unsecured_connection(unsecuredCursor, unsecuredConnection)
        except mysql.connector.ProgrammingError as e:
            print(f"Error: {e}")
            return jsonify({'message': 'SQL error', 'status': 500})
        
    # safe mode & unsafe mode
    # Add the new customer
    new_customer = Customer(customer_name=customer_name, company_name=company_name, address=address)
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'New Customer was added successfully:', 'status': 200})