from flask import Blueprint, request, jsonify
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from src.database import About, db
from flask_jwt_extended import jwt_required
from flasgger import swag_from

about = Blueprint("about", __name__, url_prefix="/api/v1/about")

@about.get('/')
@swag_from('./docs/about/get_about.yaml')
def get_about():
    about = About.query.first()
    if not about:
        return jsonify({'message': 'No about information found'}), HTTP_404_NOT_FOUND
    
    return jsonify({
        'id': about.id,
        'title': about.title.split(';') if about.title else [],
        'content': about.content.split(';') if about.content else [],
        'image': about.image,
        'created_at': about.created_at,
        'updated_at': about.updated_at
    }), HTTP_200_OK

@about.post('/')
@jwt_required()
@swag_from('./docs/about/create_about.yaml')
def create_about():
    # Kiểm tra xem đã có about chưa
    existing_about = About.query.first()
    if existing_about:
        return jsonify({'error': 'About information already exists. Please update instead.'}), HTTP_400_BAD_REQUEST
    
    title = request.json.get('title', [])
    content = request.json.get('content', [])
    image = request.json.get('image')
    
    if not title or not content:
        return jsonify({'error': 'Title and content are required'}), HTTP_400_BAD_REQUEST

    if isinstance(content, list):
        content = ";".join(content)  # Chuyển list thành chuỗi phân tách bởi dấu `;`
        
    if isinstance(title, list):
        title = ";".join(title)
        
    about = About(
        title=title,
        content=content,
        image=image
    )

    try:
        db.session.add(about)
        db.session.commit()
        return jsonify({
            'id': about.id,
            'title': about.title.split(';'),
            'content': about.content.split(';'),
            'image': about.image,
            'created_at': about.created_at,
            'updated_at': about.updated_at
        }), HTTP_201_CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to create about information'
        }), HTTP_500_INTERNAL_SERVER_ERROR

@about.put('/')
@jwt_required()
@swag_from('./docs/about/update_about.yaml')
def update_about():
    about = About.query.first()
    if not about:
        return jsonify({'error': 'No about information found'}), HTTP_404_NOT_FOUND

    title = request.json.get('title')
    content = request.json.get('content')
    image = request.json.get('image', about.image)
    
    # Use existing values if not provided
    if title is None:
        title = about.title
    if content is None:
        content = about.content

    try:
        # Handle title and content conversion if they are lists
        if isinstance(title, list):
            title = ";".join(title)
        if isinstance(content, list):
            content = ";".join(content)
            
        about.title = title
        about.content = content
        about.image = image

        db.session.commit()
        return jsonify({
            'id': about.id,
            'title': about.title.split(';') if about.title else [],
            'content': about.content.split(';') if about.content else [],
            'image': about.image,
            'created_at': about.created_at,
            'updated_at': about.updated_at
        }), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to update about information'
        }), HTTP_500_INTERNAL_SERVER_ERROR

@about.delete('/')
@jwt_required()
@swag_from('./docs/about/delete_about.yaml')
def delete_about():
    about = About.query.first()
    if not about:
        return jsonify({'error': 'No about information found'}), HTTP_404_NOT_FOUND

    try:
        db.session.delete(about)
        db.session.commit()
        return jsonify({'message': 'About information deleted successfully'}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to delete about information'
        }), HTTP_500_INTERNAL_SERVER_ERROR
