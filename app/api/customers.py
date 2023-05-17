from flask import jsonify, g, request, session
from .. import db
from . import api
from ..models import Customer

@api.route('/active_customer', methods=['GET'])
def get_active_customer():
	active_customer_id = session['active_customer']
	return jsonify({'active_customer_id': active_customer_id})

@api.route('/active_customer/<int:id>', methods=['PUT'])
def set_active_customer(id):
	active_customer = Customer.query.get_or_404(id)
	session['active_customer'] = id
	return jsonify(active_customer.to_json())
 
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