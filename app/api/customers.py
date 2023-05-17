from flask import jsonify, g, request, session
from .. import db
from . import api
from ..models import Customer
from ..exceptions import ValidationError

@api.route('/active_customer', methods=['GET'])
def get_active_customer():
    if session['active_customer_id'] is None:
        raise ValidationError('No active customer.')

    customer_id = int(session['active_customer_id'])
    c = Customer.query.get_or_404(customer_id)
    if c is None:
        raise ValidationError('No active customer.')
        
    return jsonify({'active_customer_id': int(session['active_customer_id'])})

@api.route('/active_customer/<int:id>', methods=['PUT'])
def set_active_customer(id):
    session['active_customer_id'] = id
    c = Customer.query.get_or_404(id)
    if c is not None:
        session['active_customer_id'] = c.id
    return jsonify({'active_customer_id': c.id})
 
@api.route('/delete_customer', methods=['DELETE'])
def delete_customer():
    request_data = request.get_json()
    if 'id' not in request_data:
        return jsonify({'error': 'id parameter is required'}), 400
    id = request_data['id']
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'success': f'Customer with id {id} has been deleted'}), 200

@api.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify({'customers': [c.to_json() for c in customers]})

@api.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify(customer.to_json())