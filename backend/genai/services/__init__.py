#!/usr/bin/env python3

"""
Database Initialization Script
This script initializes the database with tables and basic seed data.
"""

import os
from app import create_app, db
from models import (
    Role, User, JobPost, Resume, Application, Interview,
    Training, Course, Enrollment, Report, EODReport, ExpenseReport,
    PerformanceReview, Notification, AuditLog
)

def init_database():
    """Initialize the database with tables and seed data"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("HR MANAGEMENT SYSTEM - DATABASE INITIALIZATION")
        print("=" * 60)
        
        # Drop existing tables
        print("\n[1/4] Dropping existing tables...")
        db.drop_all()
        print("✓ Tables dropped successfully")
        
        # Create all tables
        print("\n[2/4] Creating tables...")
        db.create_all()
        print("✓ Tables created successfully")
        
        # Create basic roles
        print("\n[3/4] Creating basic roles...")
        roles_data = [
            {
                'name': 'Admin',
                'description': 'System administrator with full access to all features'
            },
            {
                'name': 'Manager',
                'description': 'Manager with team oversight and approval responsibilities'
            },
            {
                'name': 'HR',
                'description': 'Human Resources personnel managing recruitment and employee data'
            },
            {
                'name': 'Employee',
                'description': 'Regular employee with access to personal features'
            },
            {
                'name': 'Candidate',
                'description': 'Job candidate with limited access during recruitment process'
            }
        ]
        
        created_roles = {}
        for role_data in roles_data:
            role = Role(**role_data)
            db.session.add(role)
            db.session.flush()  # Get the ID before commit
            created_roles[role.name] = role
            print(f"  ✓ Created role: {role.name}")
        
        db.session.commit()
        
        # Create test users (optional)
        print("\n[4/4] Creating test users...")
        test_users = [
            {
                'name': 'Admin User',
                'email': 'admin@company.com',
                'role_id': created_roles['Admin'].id,
                'status': 'active'
            },
            {
                'name': 'John Manager',
                'email': 'john.manager@company.com',
                'role_id': created_roles['Manager'].id,
                'status': 'active'
            },
            {
                'name': 'Sarah HR',
                'email': 'sarah.hr@company.com',
                'role_id': created_roles['HR'].id,
                'status': 'active'
            },
            {
                'name': 'Bob Employee',
                'email': 'bob.employee@company.com',
                'role_id': created_roles['Employee'].id,
                'status': 'active'
            },
            {
                'name': 'Alice Candidate',
                'email': 'alice@email.com',
                'role_id': created_roles['Candidate'].id,
                'status': 'active'
            }
        ]
        
        for user_data in test_users:
            user = User(**user_data)
            db.session.add(user)
            print(f"  ✓ Created user: {user.name} ({user.email})")
        
        db.session.commit()
        
        # Create uploads directory
        print("\n[BONUS] Setting up file storage...")
        upload_dirs = [
            './uploads/receipts',
            './uploads/resumes',
            './uploads/documents'
        ]
        
        for directory in upload_dirs:
            os.makedirs(directory, exist_ok=True)
            # Create .gitkeep file
            gitkeep_path = os.path.join(directory, '.gitkeep')
            if not os.path.exists(gitkeep_path):
                open(gitkeep_path, 'w').close()
            print(f"  ✓ Created directory: {directory}")
        
        # Summary
        print("\n" + "=" * 60)
        print("DATABASE INITIALIZATION COMPLETE!")
        print("=" * 60)
        print("\n📊 Summary:")
        print(f"  • Roles created: {len(roles_data)}")
        print(f"  • Test users created: {len(test_users)}")
        print(f"  • Upload directories: {len(upload_dirs)}")
        
        print("\n📋 Available Roles:")
        roles = Role.query.all()
        for role in roles:
            user_count = User.query.filter_by(role_id=role.id).count()
            print(f"  • {role.name}: {role.description} ({user_count} users)")
        
        print("\n👥 Test Users:")
        users = User.query.all()
        for user in users:
            print(f"  • {user.name} ({user.email}) - Role: {user.role.name}")
        
        print("\n🚀 Next Steps:")
        print("  1. Start the server: python run.py")
        print("  2. Test health endpoint: curl http://localhost:5001/health")
        print("  3. View API docs: See EXPENSE_API_DOCUMENTATION.md")
        print("  4. Test expense API: curl http://localhost:5001/api/expenses/")
        
        print("\n" + "=" * 60)

def reset_database():
    """Reset database - drops and recreates all tables"""
    app = create_app()
    
    with app.app_context():
        print("\n⚠️  WARNING: This will delete all existing data!")
        response = input("Are you sure you want to reset the database? (yes/no): ")
        
        if response.lower() == 'yes':
            init_database()
        else:
            print("Database reset cancelled.")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--reset':
        reset_database()
    else:
        init_database()