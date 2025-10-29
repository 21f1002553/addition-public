from flask import Blueprint, request, jsonify
from app import db
from models import Role, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'User already exists'}), 400
        
        # Create new user
        user = User(
            name=data['name'],
            email=data['email'],
            role_id=data['role_id'],
            status=data.get('status', 'active')
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'User registered successfully', 'user': user.to_dict()}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if user.status != 'active':
            return jsonify({'error': 'User account is not active'}), 403
        
        return jsonify({'message': 'Login successful', 'user': user.to_dict()}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/roles', methods=['GET'])
def get_roles():
    try:
        roles = Role.query.all()
        return jsonify([role.to_dict() for role in roles]), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/roles', methods=['POST'])
def create_role():
    try:
        data = request.get_json()
        
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
