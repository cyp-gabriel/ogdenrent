from flask import jsonify, g, request, session
from .. import db
from . import api
from ..models import Customer
from ..exceptions import ValidationError
import os

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
 
@api.route('/delete_customer/<int:id>', methods=['DELETE'])
def delete_customer(id):
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

@api.route('/customer_photo', methods=['POST'])
def set_customer_picture():
        # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    filename = os.path.basename(file.filename)
    
    customer_id = int(session['active_customer_id'])

    # Save the file to the uploads folder
    file_path = os.path.join(os.path.abspath('app/uploads/'), filename)
    
    with open(file_path, 'wb') as f:
        f.write(file.read())

    # Return a response with the file name and path
    return jsonify({
        'filename': filename,
        'filepath': f'uploads/customer{customer_id}/{filename}'
    }), 200