from flask import Blueprint, request, jsonify
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from src.database import Project, db
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from datetime import datetime

project = Blueprint("project", __name__, url_prefix="/api/v1/projects")

def format_project(project):
    return {
        'id': project.id,
        'title': project.title,
        'image': project.image,
        'description': project.description,
        'project_url': project.project_url,
        'github_url': project.github_url,
        'technologies': project.technologies,
        'start_date': project.start_date,
        'end_date': project.end_date,
        'created_at': project.created_at,
        'updated_at': project.updated_at
    }

@project.get('/')
@swag_from('./docs/project/get_projects.yaml')
def get_projects():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Validate pagination parameters
    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:
        per_page = min(max(per_page, 1), 100)  # Limit to max 100 items per page
    
    projects = Project.query.order_by(Project.start_date.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    data = [format_project(project) for project in projects.items]
    
    meta = {
        'page': projects.page,
        'pages': projects.pages,
        'total_count': projects.total,
        'prev_page': projects.prev_num,
        'next_page': projects.next_num,
        'has_next': projects.has_next,
        'has_prev': projects.has_prev,
    }

    return jsonify({
        'data': data,
        'meta': meta
    }), HTTP_200_OK

@project.get('/<int:id>')
@swag_from('./docs/project/get_project.yaml')
def get_project(id):
    project = Project.query.get(id)
    if not project:
        return jsonify({'error': 'Project not found'}), HTTP_404_NOT_FOUND

    return jsonify(format_project(project)), HTTP_200_OK

@project.post('/')
@jwt_required()
@swag_from('./docs/project/create_project.yaml')
def create_project():
    title = request.json.get('title')
    image = request.json.get('image')
    description = request.json.get('description')
    project_url = request.json.get('project_url')
    github_url = request.json.get('github_url')
    technologies = request.json.get('technologies')
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')

    if not title or not description or not start_date:
        return jsonify({
            'error': 'Title, description and start date are required'
        }), HTTP_400_BAD_REQUEST

    try:
        # Parse start_date to string format YYYYMMDD for storage
        start_date_parsed = datetime.strptime(start_date, '%Y-%m-%d')
        start_date_str = start_date_parsed.strftime('%Y%m%d')
        
        if end_date:
            end_date_parsed = datetime.strptime(end_date, '%Y-%m-%d')
            end_date_str = end_date_parsed.strftime('%Y%m%d')
            if end_date_parsed < start_date_parsed:
                return jsonify({
                    'error': 'End date cannot be earlier than start date'
                }), HTTP_400_BAD_REQUEST
        else:
            end_date_str = None
    except ValueError:
        return jsonify({
            'error': 'Invalid date format. Use YYYY-MM-DD'
        }), HTTP_400_BAD_REQUEST

    project = Project(
        title=title,
        image=image,
        description=description,
        project_url=project_url,
        github_url=github_url,
        technologies=technologies,
        start_date=start_date_str,
        end_date=end_date_str
    )

    try:
        db.session.add(project)
        db.session.commit()
        return jsonify(format_project(project)), HTTP_201_CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to create project'
        }), HTTP_500_INTERNAL_SERVER_ERROR

@project.put('/<int:id>')
@project.patch('/<int:id>')
@jwt_required()
@swag_from('./docs/project/update_project.yaml')
def update_project(id):
    project = Project.query.get(id)
    if not project:
        return jsonify({'error': 'Project not found'}), HTTP_404_NOT_FOUND

    title = request.json.get('title', project.title)
    image = request.json.get('image', project.image)
    description = request.json.get('description', project.description)
    project_url = request.json.get('project_url', project.project_url)
    github_url = request.json.get('github_url', project.github_url)
    technologies = request.json.get('technologies', project.technologies)
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')

    if start_date:
        try:
            start_date_parsed = datetime.strptime(start_date, '%Y-%m-%d')
            start_date_str = start_date_parsed.strftime('%Y%m%d')
            project.start_date = start_date_str
        except ValueError:
            return jsonify({
                'error': 'Invalid start date format. Use YYYY-MM-DD'
            }), HTTP_400_BAD_REQUEST

    if end_date:
        try:
            # Get current start_date for comparison
            current_start = datetime.strptime(project.start_date, '%Y%m%d') if project.start_date else None
            end_date_parsed = datetime.strptime(end_date, '%Y-%m-%d')
            end_date_str = end_date_parsed.strftime('%Y%m%d')
            if current_start and end_date_parsed < current_start:
                return jsonify({
                    'error': 'End date cannot be earlier than start date'
                }), HTTP_400_BAD_REQUEST
            project.end_date = end_date_str
        except ValueError:
            return jsonify({
                'error': 'Invalid end date format. Use YYYY-MM-DD'
            }), HTTP_400_BAD_REQUEST

    try:
        project.title = title
        project.image = image
        project.description = description
        project.project_url = project_url
        project.github_url = github_url
        project.technologies = technologies

        db.session.commit()
        return jsonify(format_project(project)), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to update project'
        }), HTTP_500_INTERNAL_SERVER_ERROR

@project.delete('/<int:id>')
@jwt_required()
@swag_from('./docs/project/delete_project.yaml')
def delete_project(id):
    project = Project.query.get(id)
    if not project:
        return jsonify({'error': 'Project not found'}), HTTP_404_NOT_FOUND

    try:
        db.session.delete(project)
        db.session.commit()
        return jsonify({
            'message': 'Project deleted successfully'
        }), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to delete project'
        }), HTTP_500_INTERNAL_SERVER_ERROR

@project.get('/latest')
@swag_from('./docs/project/get_latest_projects.yaml')
def get_latest_projects():
    projects = Project.query.order_by(Project.start_date.desc()).limit(3).all()
    data = [format_project(project) for project in projects]
    
    return jsonify({'data': data}), HTTP_200_OK
