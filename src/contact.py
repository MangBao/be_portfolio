from flask import Blueprint, request, jsonify
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from src.database import Contact, db
from flask_jwt_extended import jwt_required
from flasgger import swag_from
import validators

contact = Blueprint("contact", __name__, url_prefix="/api/v1/contacts")

def format_contact(contact):
    return {
        'id': contact.id,
        'name': contact.name,
        'email': contact.email,
        'subject': contact.subject,
        'content': contact.content,
        'status': contact.status,
        'created_at': contact.created_at,
        'updated_at': contact.updated_at
    }

@contact.get('/')
@jwt_required()
@swag_from('./docs/contact/get_contacts.yaml')
def get_contacts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    
    query = Contact.query
    
    if status:
        query = query.filter_by(status=status)
    
    contacts = query.order_by(Contact.created_at.desc())\
        .paginate(page=page, per_page=per_page)
    
    data = [format_contact(contact) for contact in contacts.items]
    
    meta = {
        'page': contacts.page,
        'pages': contacts.pages,
        'total_count': contacts.total,
        'prev_page': contacts.prev_num,
        'next_page': contacts.next_num,
        'has_next': contacts.has_next,
        'has_prev': contacts.has_prev,
    }
    
    return jsonify({
        'data': data,
        'meta': meta
    }), HTTP_200_OK

@contact.get('/<int:id>')
@jwt_required()
def get_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({'error': 'Contact not found'}), HTTP_404_NOT_FOUND
    
    return jsonify(format_contact(contact)), HTTP_200_OK

@contact.post('/')
@swag_from('./docs/contact/create_contact.yaml')
def create_contact():
    name = request.json.get('name')
    email = request.json.get('email')
    subject = request.json.get('subject')
    content = request.json.get('content')
    
    # Validate required fields
    if not all([name, email, subject, content]):
        return jsonify({
            'error': 'All fields (name, email, subject, content) are required'
        }), HTTP_400_BAD_REQUEST
    
    # Validate email format
    if not validators.email(email):
        return jsonify({
            'error': 'Invalid email format'
        }), HTTP_400_BAD_REQUEST
    
    # Validate content length
    if len(content) < 10:
        return jsonify({
            'error': 'Content must be at least 10 characters long'
        }), HTTP_400_BAD_REQUEST
    
    contact = Contact(
        name=name,
        email=email,
        subject=subject,
        content=content,
        status='pending'  # Default status
    )
    
    db.session.add(contact)
    db.session.commit()
    
    return jsonify({
        'message': 'Contact message sent successfully',
        'contact': format_contact(contact)
    }), HTTP_201_CREATED

@contact.patch('/<int:id>/status')
@jwt_required()
@swag_from('./docs/contact/update_contact_status.yaml')
def update_contact_status(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({'error': 'Contact not found'}), HTTP_404_NOT_FOUND
    
    status = request.json.get('status')
    if not status:
        return jsonify({'error': 'Status is required'}), HTTP_400_BAD_REQUEST
    
    # Validate status value
    valid_statuses = ['pending', 'replied', 'spam']
    if status not in valid_statuses:
        return jsonify({
            'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
        }), HTTP_400_BAD_REQUEST
    
    contact.status = status
    db.session.commit()
    
    return jsonify(format_contact(contact)), HTTP_200_OK

@contact.delete('/<int:id>')
@jwt_required()
@swag_from('./docs/contact/delete_contact.yaml')
def delete_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({'error': 'Contact not found'}), HTTP_404_NOT_FOUND
    
    db.session.delete(contact)
    db.session.commit()
    
    return jsonify({
        'message': 'Contact deleted successfully'
    }), HTTP_200_OK

@contact.get('/stats')
@jwt_required()
@swag_from('./docs/contact/get_contact_stats.yaml')
def get_contact_stats():
    total = Contact.query.count()
    pending = Contact.query.filter_by(status='pending').count()
    replied = Contact.query.filter_by(status='replied').count()
    spam = Contact.query.filter_by(status='spam').count()
    
    return jsonify({
        'total': total,
        'pending': pending,
        'replied': replied,
        'spam': spam
    }), HTTP_200_OK

@contact.get('/latest')
@jwt_required()
@swag_from('./docs/contact/get_latest_contacts.yaml')
def get_latest_contacts():
    contacts = Contact.query.filter_by(status='pending')\
        .order_by(Contact.created_at.desc())\
        .limit(5)\
        .all()
    
    data = [format_contact(contact) for contact in contacts]
    
    return jsonify({'data': data}), HTTP_200_OK
