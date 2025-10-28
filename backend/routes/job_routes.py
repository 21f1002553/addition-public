from flask import Blueprint, request, jsonify
from app import db
from models import JobPost

job_bp = Blueprint('jobs', __name__)

@job_bp.route('/', methods=['GET'])
def get_jobs():
    try:
        jobs = JobPost.query.all()
        return jsonify([job.to_dict() for job in jobs]), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@job_bp.route('/<job_id>', methods=['GET'])
def get_job(job_id):
    try:
        job = JobPost.query.get_or_404(job_id)
        return jsonify(job.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@job_bp.route('/', methods=['POST'])
def create_job():
    try:
        data = request.get_json()
        
        job = JobPost(
            title=data['title'],
            description=data.get('description', ''),
            requirements=data.get('requirements', ''),
            posted_by_id=data['posted_by_id'],
            status=data.get('status', 'active')
        )
        
        db.session.add(job)
        db.session.commit()
        
        return jsonify({'message': 'Job post created successfully', 'job': job.to_dict()}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@job_bp.route('/<job_id>', methods=['PUT'])
def update_job(job_id):
    try:
        job = JobPost.query.get_or_404(job_id)
        data = request.get_json()
        
        job.title = data.get('title', job.title)
        job.description = data.get('description', job.description)
        job.requirements = data.get('requirements', job.requirements)
        job.status = data.get('status', job.status)
        
        db.session.commit()
        
        return jsonify({'message': 'Job post updated successfully', 'job': job.to_dict()}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@job_bp.route('/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    try:
        job = JobPost.query.get_or_404(job_id)
        db.session.delete(job)
        db.session.commit()
        
        return jsonify({'message': 'Job post deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@job_bp.route('/<job_id>/applications', methods=['GET'])
def get_job_applications(job_id):
    try:
        job = JobPost.query.get_or_404(job_id)
        applications = job.applications
        return jsonify([application.to_dict() for application in applications]), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
