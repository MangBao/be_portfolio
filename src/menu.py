from flask import Blueprint, request, jsonify
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from src.database import Menu, db
from flask_jwt_extended import jwt_required
from flasgger import swag_from

menu = Blueprint("menu", __name__, url_prefix="/api/v1/menu")

@menu.get('/')
@swag_from('./docs/menu/get_menus.yaml')
def get_menus():
    menus = Menu.query.order_by(Menu.menu_order.asc()).all()
    data = []
    for menu in menus:
        data.append({
            'id': menu.id,
            'title': menu.title.split(';') if menu.title else [],
            'menu_name': menu.menu_name,
            'menu_url': menu.menu_url,
            'menu_order': menu.menu_order,
            'is_active': menu.is_active,
            'created_at': menu.created_at,
            'updated_at': menu.updated_at
        })
    
    return jsonify({'menus': data}), HTTP_200_OK

@menu.get('/<int:id>')
@swag_from('./docs/menu/get_menu.yaml')
def get_menu(id):
    menu = Menu.query.get(id)
    if not menu:
        return jsonify({'error': 'Menu not found'}), HTTP_404_NOT_FOUND

    return jsonify({
        'id': menu.id,
        'title': menu.title,
        'menu_name': menu.menu_name,
        'menu_url': menu.menu_url,
        'menu_order': menu.menu_order,
        'is_active': menu.is_active,
        'created_at': menu.created_at,
        'updated_at': menu.updated_at
    }), HTTP_200_OK

@menu.post('/')
@jwt_required()
@swag_from('./docs/menu/create_menu.yaml')
def create_menu():
    title = request.json.get('title', [])
    menu_name = request.json.get('menu_name')
    menu_url = request.json.get('menu_url')
    menu_order = request.json.get('menu_order', 0)
    is_active = request.json.get('is_active', True)

    # Kiểm tra required fields
    if not menu_name or not menu_url:
        return jsonify({'error': 'Menu name and URL are required'}), HTTP_400_BAD_REQUEST

    # Kiểm tra nếu menu_name đã tồn tại
    existing_menu = Menu.query.filter_by(menu_name=menu_name).first()
    if existing_menu:
        return jsonify({'error': f'Menu name "{menu_name}" already exists'}), HTTP_400_BAD_REQUEST

    # Đảm bảo title luôn là list trước khi xử lý
    if not isinstance(title, list):
        return jsonify({'error': 'Title must be an array of strings'}), HTTP_400_BAD_REQUEST

    # Kiểm tra số lượng phần tử title
    if len(title) > 2:
        return jsonify({'error': 'Title can only have a maximum of 2 parts'}), HTTP_400_BAD_REQUEST

    # Chuyển list thành string nếu có giá trị
    title_str = ";".join(title) if title else ""

    # Tạo đối tượng menu
    menu = Menu(
        title=title_str,
        menu_name=menu_name,
        menu_url=menu_url,
        menu_order=menu_order,
        is_active=is_active
    )

    db.session.add(menu)
    db.session.commit()

    return jsonify({
        'id': menu.id,
        'title': menu.title.split(';') if menu.title else [],
        'menu_name': menu.menu_name,
        'menu_url': menu.menu_url,
        'menu_order': menu.menu_order,
        'is_active': menu.is_active,
        'created_at': menu.created_at,
        'updated_at': menu.updated_at
    }), HTTP_201_CREATED


@menu.put('/<int:id>')
@jwt_required()
@swag_from('./docs/menu/update_menu.yaml')
def update_menu(id):
    menu = Menu.query.get(id)
    if not menu:
        return jsonify({'error': 'Menu not found'}), HTTP_404_NOT_FOUND

    title = request.json.get('title', menu.title)
    menu_name = request.json.get('menu_name', menu.menu_name)
    menu_url = request.json.get('menu_url', menu.menu_url)
    menu_order = request.json.get('menu_order', menu.menu_order)
    is_active = request.json.get('is_active', menu.is_active)

    # Kiểm tra title không quá 2 phần
    if title and len(title.split(',')) > 2:
        return jsonify({'error': 'Title can only have maximum 2 parts separated by comma'}), HTTP_400_BAD_REQUEST

    menu.title = title
    menu.menu_name = menu_name
    menu.menu_url = menu_url
    menu.menu_order = menu_order
    menu.is_active = is_active

    db.session.commit()

    return jsonify({
        'id': menu.id,
        'title': menu.title,
        'menu_name': menu.menu_name,
        'menu_url': menu.menu_url,
        'menu_order': menu.menu_order,
        'is_active': menu.is_active,
        'created_at': menu.created_at,
        'updated_at': menu.updated_at
    }), HTTP_200_OK

@menu.delete('/<int:id>')
@jwt_required()
@swag_from('./docs/menu/delete_menu.yaml')
def delete_menu(id):
    menu = Menu.query.get(id)
    if not menu:
        return jsonify({'error': 'Menu not found'}), HTTP_404_NOT_FOUND

    db.session.delete(menu)
    db.session.commit()

    return jsonify({'message': 'Menu deleted successfully'}), HTTP_200_OK

@menu.patch('/<int:id>/toggle-active')
@jwt_required()
@swag_from('./docs/menu/toggle_menu_active.yaml')
def toggle_menu_active(id):
    menu = Menu.query.get(id)
    if not menu:
        return jsonify({'error': 'Menu not found'}), HTTP_404_NOT_FOUND

    menu.is_active = not menu.is_active
    db.session.commit()

    return jsonify({
        'id': menu.id,
        'is_active': menu.is_active,
        'message': f'Menu is now {"active" if menu.is_active else "inactive"}'
    }), HTTP_200_OK
