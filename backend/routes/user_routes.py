from flask import Blueprint, request, jsonify
from app import db
from models import User, Role, Notification, PerformanceReview

user_bp = Blueprint('users', __name__)

@user_bp.route('/', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'Email already exists'}), 400
        
        user = User(
            name=data['name'],
            email=data['email'],
            role_id=data['role_id'],
            status=data.get('status', 'active')
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'User created successfully', 'user': user.to_dict()}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.role_id = data.get('role_id', user.role_id)
        user.status = data.get('status', user.status)
        
        db.session.commit()
        
        return jsonify({'message': 'User updated successfully', 'user': user.to_dict()}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'User deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<user_id>/notifications', methods=['GET'])
def get_user_notifications(user_id):
    try:
        notifications = Notification.query.filter_by(recipient_id=user_id).order_by(Notification.created_at.desc()).all()
        return jsonify([notification.to_dict() for notification in notifications]), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<user_id>/notifications', methods=['POST'])
def create_notification(user_id):
    try:
        data = request.get_json()
        
        notification = Notification(
            recipient_id=user_id,
            message=data['message'],
            read=data.get('read', False)
        )
        
        db.session.add(notification)
        db.session.commit()
        
        return jsonify({'message': 'Notification created successfully', 'notification': notification.to_dict()}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<user_id>/notifications/<notification_id>/read', methods=['PUT'])
def mark_notification_read(user_id, notification_id):
    try:
        notification = Notification.query.filter_by(id=notification_id, recipient_id=user_id).first_or_404()
        notification.read = True
        
        db.session.commit()
        
        return jsonify({'message': 'Notification marked as read'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<user_id>/performance-reviews', methods=['GET'])
def get_user_performance_reviews(user_id):
    try:
        reviews = PerformanceReview.query.filter_by(employee_id=user_id).order_by(PerformanceReview.created_at.desc()).all()
        return jsonify([review.to_dict() for review in reviews]), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<user_id>/performance-reviews', methods=['POST'])
def create_performance_review(user_id):
    try:
        data = request.get_json()
        
        review = PerformanceReview(
            employee_id=user_id,
            reviewer_id=data['reviewer_id'],
            type=data['type'],
            text=data.get('text', ''),
            rating=data.get('rating')
        )
        
        db.session.add(review)
        db.session.commit()
        
        return jsonify({'message': 'Performance review created successfully', 'review': review.to_dict()}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
