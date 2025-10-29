#!/usr/bin/env python3

from app import create_app, db
from models import (
    Role, User, JobPost, Resume, Application, Interview,
    Training, Course, Enrollment, Report, EODReport, ExpenseReport,
    PerformanceReview, Notification, AuditLog
)

def init_database():
    app = create_app()
    
    with app.app_context():
        print("Dropping existing tables...")
        db.drop_all()
        
        print("Creating tables...")
        db.create_all()
        
        print("Creating basic roles...")
        roles_data = [
            {'name': 'Admin', 'description': 'System administrator with full access'},
            {'name': 'Manager', 'description': 'Manager with team oversight responsibilities'},
            {'name': 'HR', 'description': 'Human Resources personnel'},
            {'name': 'Candidate', 'description': 'Job candidate with limited access'}
        ]
        
        for role_data in roles_data:
            role = Role(**role_data)
            db.session.add(role)
        
        db.session.commit()
        
        print("Database initialized successfully!")
        print("Available roles:")
        roles = Role.query.all()
        for role in roles:
            print(f"  - {role.name}: {role.description}")

if __name__ == '__main__':
    init_database()
