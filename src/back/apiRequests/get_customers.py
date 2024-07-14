from flask import Blueprint, request, jsonify
from models import db, Customer
from sqlalchemy import text
from myfunc import safe_mode

get_customers_bp = Blueprint('get_customers_bp', __name__)

@get_customers_bp.route('/get_customers', methods=['GET'])
def get_customers():
    search_field = request.args.get('searchField')
    search_type = request.args.get('searchType')
    search_data = request.args.get('searchData')

    if safe_mode:
        query = Customer.query
        if search_field and search_type and search_data:
            if search_type == 'contains':
                query = query.filter(getattr(Customer, search_field).like(f'%{search_data}%'))
            elif search_type == 'equals':
                query = query.filter(getattr(Customer, search_field) == search_data)
        result = query.all()
        customers = [
            {
                'customer_name': customer.customer_name,
                'company_name': customer.company_name,
                'address': customer.address
            }
            for customer in result
        ]
    else:
        query = None
        if not search_field or not search_type or not search_data:
            query = text("SELECT customer_name, company_name, address FROM customers")
        else:
            if search_type == 'contains':
                query = text(f"SELECT customer_name, company_name, address FROM customers WHERE {search_field} LIKE '%{search_data}%'")
            elif search_type == 'equals':
                query = text(f"SELECT customer_name, company_name, address FROM customers WHERE {search_field} = '{search_data}'")
        customers = [
            {
                'customer_name': row[0],
                'company_name': row[1],
                'address': row[2]
            }
            for row in result
        ]
        result = db.session.execute(query)

  
    return jsonify(customers)