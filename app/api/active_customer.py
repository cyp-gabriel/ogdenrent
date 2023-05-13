from flask import jsonify, g, request
from .. import db
from . import api
from ..models import Customer

@api.route('active_customer')
def get_active_customer():
	active_customer_id = g.session['active_customer']
	return jsonify({'active_customer_id': active_customer_id})

@api.route('active_customer/<int:id>', methods=['PUT'])
def set_active_customer(id):
	active_customer = Customer.query.get_or_404(id)
	g.session['active_customer'] = id
	return jsonify(active_customer.to_json())