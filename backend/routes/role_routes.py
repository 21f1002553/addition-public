from flask import Blueprint, request, jsonify
from app import db
from models import Role

role_bp = Blueprint('roles', __name__)

@role_bp.route('/', methods=['GET'])
def get_roles():
    try:
        roles = Role.query.all()
        return jsonify([role.to_dict() for role in roles]), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@role_bp.route('/', methods=['POST'])
def create_role():
    try:
        data = request.get_json()
        
        existing_role = Role.query.filter_by(name=data['name']).first()
        if existing_role:
            return jsonify({'error': 'Role name already exists'}), 400
        
        role = Role(
            name=data['name'],
            description=data.get('description', '')
        )
        
        db.session.add(role)
        db.session.commit()
        
        return jsonify({'message': 'Role created successfully', 'role': role.to_dict()}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@role_bp.route('/<role_id>', methods=['GET'])
def get_role(role_id):
    try:
        role = Role.query.get_or_404(role_id)
        return jsonify(role.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
