from flask import Blueprint, request, jsonify
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from src.database import Skill, db
from flask_jwt_extended import jwt_required
from flasgger import swag_from

skill = Blueprint("skill", __name__, url_prefix="/api/v1/skills")

def format_skill(skill):
    return {
        'id': skill.id,
        'skill_name': skill.skill_name,
        'icon_skill': skill.icon_skill,
        'short_desc': skill.short_desc,
        'proficiency': skill.proficiency,
        'category': skill.category,
        'created_at': skill.created_at,
        'updated_at': skill.updated_at
    }

@skill.get('/')
@swag_from('./docs/skill/get_skills.yaml')
def get_skills():
    category = request.args.get('category')
    query = Skill.query

    if category:
        query = query.filter_by(category=category)
    
    skills = query.order_by(Skill.category, Skill.proficiency.desc()).all()
    
    # Nhóm skills theo category
    categorized_skills = {}
    for skill in skills:
        category = skill.category or 'Other'
        if category not in categorized_skills:
            categorized_skills[category] = []
        categorized_skills[category].append(format_skill(skill))
    
    return jsonify({
        'data': categorized_skills,
        'categories': list(categorized_skills.keys())
    }), HTTP_200_OK

@skill.get('/categories')
@swag_from('./docs/skill/get_categories.yaml')
def get_categories():
    categories = db.session.query(Skill.category)\
        .filter(Skill.category.isnot(None))\
        .distinct()\
        .all()
    categories = [cat[0] for cat in categories if cat[0]]
    
    return jsonify({'categories': categories}), HTTP_200_OK

@skill.get('/<int:id>')
@swag_from('./docs/skill/get_skill.yaml')
def get_skill(id):
    skill = Skill.query.get(id)
    if not skill:
        return jsonify({'error': 'Skill not found'}), HTTP_404_NOT_FOUND

    return jsonify(format_skill(skill)), HTTP_200_OK

@skill.post('/')
@jwt_required()
@swag_from('./docs/skill/create_skill.yaml')
def create_skill():
    skill_name = request.json.get('skill_name')
    icon_skill = request.json.get('icon_skill')
    short_desc = request.json.get('short_desc')
    proficiency = request.json.get('proficiency', 0)
    category = request.json.get('category')

    if not skill_name:
        return jsonify({
            'error': 'Skill name is required'
        }), HTTP_400_BAD_REQUEST

    # Validate proficiency range (0-100)
    if not isinstance(proficiency, (int, float)) or proficiency < 0 or proficiency > 100:
        return jsonify({
            'error': 'Proficiency must be a number between 0 and 100'
        }), HTTP_400_BAD_REQUEST

    # Check if skill already exists
    existing_skill = Skill.query.filter_by(skill_name=skill_name).first()
    if existing_skill:
        return jsonify({
            'error': 'Skill with this name already exists'
        }), HTTP_400_BAD_REQUEST

    skill = Skill(
        skill_name=skill_name,
        icon_skill=icon_skill,
        short_desc=short_desc,
        proficiency=proficiency,
        category=category
    )

    db.session.add(skill)
    db.session.commit()

    return jsonify(format_skill(skill)), HTTP_201_CREATED

@skill.put('/<int:id>')
@skill.patch('/<int:id>')
@jwt_required()
@swag_from('./docs/skill/update_skill.yaml')
def update_skill(id):
    skill = Skill.query.get(id)
    if not skill:
        return jsonify({'error': 'Skill not found'}), HTTP_404_NOT_FOUND

    skill_name = request.json.get('skill_name', skill.skill_name)
    icon_skill = request.json.get('icon_skill', skill.icon_skill)
    short_desc = request.json.get('short_desc', skill.short_desc)
    proficiency = request.json.get('proficiency', skill.proficiency)
    category = request.json.get('category', skill.category)

    # Validate proficiency range (0-100)
    if not isinstance(proficiency, (int, float)) or proficiency < 0 or proficiency > 100:
        return jsonify({
            'error': 'Proficiency must be a number between 0 and 100'
        }), HTTP_400_BAD_REQUEST

    # Check if new skill name already exists (excluding current skill)
    if skill_name != skill.skill_name:
        existing_skill = Skill.query.filter_by(skill_name=skill_name).first()
        if existing_skill:
            return jsonify({
                'error': 'Skill with this name already exists'
            }), HTTP_400_BAD_REQUEST

    skill.skill_name = skill_name
    skill.icon_skill = icon_skill
    skill.short_desc = short_desc
    skill.proficiency = proficiency
    skill.category = category

    db.session.commit()

    return jsonify(format_skill(skill)), HTTP_200_OK

@skill.delete('/<int:id>')
@jwt_required()
@swag_from('./docs/skill/delete_skill.yaml')
def delete_skill(id):
    skill = Skill.query.get(id)
    if not skill:
        return jsonify({'error': 'Skill not found'}), HTTP_404_NOT_FOUND

    db.session.delete(skill)
    db.session.commit()

    return jsonify({
        'message': 'Skill deleted successfully'
    }), HTTP_200_OK

@skill.post('/batch')
@jwt_required()
@swag_from('./docs/skill/batch_create_skills.yaml')
def batch_create_skills():
    skills_data = request.json.get('skills', [])
    
    if not isinstance(skills_data, list):
        return jsonify({
            'error': 'Skills data must be a list'
        }), HTTP_400_BAD_REQUEST
    
    created_skills = []
    errors = []
    
    for skill_data in skills_data:
        try:
            skill_name = skill_data.get('skill_name')
            if not skill_name:
                errors.append(f'Skill name is required')
                continue
                
            proficiency = skill_data.get('proficiency', 0)
            if not isinstance(proficiency, (int, float)) or proficiency < 0 or proficiency > 100:
                errors.append(f'Invalid proficiency for skill: {skill_name}')
                continue
                
            existing_skill = Skill.query.filter_by(skill_name=skill_name).first()
            if existing_skill:
                errors.append(f'Skill already exists: {skill_name}')
                continue
                
            skill = Skill(
                skill_name=skill_name,
                icon_skill=skill_data.get('icon_skill'),
                short_desc=skill_data.get('short_desc'),
                proficiency=proficiency,
                category=skill_data.get('category')
            )
            
            db.session.add(skill)
            created_skills.append(skill)
            
        except Exception as e:
            errors.append(f'Error processing skill {skill_name}: {str(e)}')
    
    if created_skills:
        db.session.commit()
    
    return jsonify({
        'created': [format_skill(skill) for skill in created_skills],
        'errors': errors
    }), HTTP_201_CREATED if created_skills else HTTP_400_BAD_REQUEST
