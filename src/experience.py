from flask import Blueprint, request, jsonify
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from src.database import Experience, db
from flask_jwt_extended import jwt_required
from datetime import datetime
from flasgger import swag_from

experience = Blueprint("experience", __name__, url_prefix="/api/v1/experiences")

def format_experience(experience):
    return {
        'id': experience.id,
        'company_name': experience.company_name,
        'role_name': experience.role_name,
        'desc_role': experience.desc_role,
        'company_location': experience.company_location,
        'start_date': experience.start_date,
        'end_date': experience.end_date,
        'is_current': experience.is_current,
        'created_at': experience.created_at,
        'updated_at': experience.updated_at
    }

@experience.get('/')
@swag_from('./docs/experience/get_experiences.yaml')
def get_experiences():
    experiences = Experience.query.order_by(Experience.start_date.desc()).all()
    data = [format_experience(exp) for exp in experiences]
    
    return jsonify({'data': data}), HTTP_200_OK

@experience.get('/<int:id>')
@swag_from('./docs/experience/get_experience.yaml')
def get_experience(id):
    experience = Experience.query.get(id)
    if not experience:
        return jsonify({'error': 'Experience not found'}), HTTP_404_NOT_FOUND

    return jsonify(format_experience(experience)), HTTP_200_OK

@experience.post('/')
@jwt_required()
@swag_from('./docs/experience/create_experience.yaml')
def create_experience():
    company_name = request.json.get('company_name')
    role_name = request.json.get('role_name')
    desc_role = request.json.get('desc_role', [])  # Nhận vào là list
    company_location = request.json.get('company_location')
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')
    is_current = request.json.get('is_current', False)

    # Validate required fields
    if not company_name or not role_name or not start_date:
        return jsonify({
            'error': 'Company name, role name and start date are required'
        }), HTTP_400_BAD_REQUEST

    # Convert desc_role list to string with semicolon separator
    if isinstance(desc_role, list):
        desc_role = ';'.join(desc_role)

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date and not is_current:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if end_date < start_date:
                return jsonify({
                    'error': 'End date cannot be earlier than start date'
                }), HTTP_400_BAD_REQUEST
    except ValueError:
        return jsonify({
            'error': 'Invalid date format. Use YYYY-MM-DD'
        }), HTTP_400_BAD_REQUEST

    # If is_current is True, end_date should be None
    if is_current:
        end_date = None

    experience = Experience(
        company_name=company_name,
        role_name=role_name,
        desc_role=desc_role,
        company_location=company_location,
        start_date=start_date,
        end_date=end_date,
        is_current=is_current
    )

    db.session.add(experience)
    db.session.commit()

    return jsonify(format_experience(experience)), HTTP_201_CREATED

@experience.put('/<int:id>')
@experience.patch('/<int:id>')
# @swag_from('./docs/experience/update_experience.yaml')
@jwt_required()
def update_experience(id):
    experience = Experience.query.get(id)
    if not experience:
        return jsonify({'error': 'Experience not found'}), HTTP_404_NOT_FOUND

    company_name = request.json.get('company_name', experience.company_name)
    role_name = request.json.get('role_name', experience.role_name)
    desc_role = request.json.get('desc_role', experience.desc_role.split(';') if experience.desc_role else [])
    company_location = request.json.get('company_location', experience.company_location)
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')
    is_current = request.json.get('is_current', experience.is_current)

    # Convert desc_role list to string with semicolon separator
    if isinstance(desc_role, list):
        desc_role = ';'.join(desc_role)

    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            experience.start_date = start_date
        except ValueError:
            return jsonify({
                'error': 'Invalid start date format. Use YYYY-MM-DD'
            }), HTTP_400_BAD_REQUEST

    if end_date and not is_current:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if end_date < experience.start_date:
                return jsonify({
                    'error': 'End date cannot be earlier than start date'
                }), HTTP_400_BAD_REQUEST
            experience.end_date = end_date
        except ValueError:
            return jsonify({
                'error': 'Invalid end date format. Use YYYY-MM-DD'
            }), HTTP_400_BAD_REQUEST

    # If is_current is True, end_date should be None
    if is_current:
        experience.end_date = None

    experience.company_name = company_name
    experience.role_name = role_name
    experience.desc_role = desc_role
    experience.company_location = company_location
    experience.is_current = is_current

    db.session.commit()

    return jsonify(format_experience(experience)), HTTP_200_OK

@experience.delete('/<int:id>')
@jwt_required()
@swag_from('./docs/experience/delete_experience.yaml')
def delete_experience(id):
    experience = Experience.query.get(id)
    if not experience:
        return jsonify({'error': 'Experience not found'}), HTTP_404_NOT_FOUND

    db.session.delete(experience)
    db.session.commit()

    return jsonify({
        'message': 'Experience deleted successfully'
    }), HTTP_200_OK

@experience.get('/current')
@swag_from('./docs/experience/get_current_experience.yaml')
def get_current_experience():
    current_experience = Experience.query.filter_by(is_current=True).first()
    if not current_experience:
        return jsonify({'message': 'No current experience found'}), HTTP_404_NOT_FOUND
    
    return jsonify(format_experience(current_experience)), HTTP_200_OK
