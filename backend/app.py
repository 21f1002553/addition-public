import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///hr_system.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # File upload configuration
    app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', './uploads/receipts')
    app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_UPLOAD_SIZE', 5 * 1024 * 1024))  # 5MB default
    
    # Create upload directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Import models
    from models import (
        Role, User, JobPost, Resume, Application, Interview,
        Training, Course, Enrollment, Report, EODReport, ExpenseReport,
        PerformanceReview, Notification, AuditLog
    )
    
    # Import and register blueprints
    from routes.user_routes import user_bp
    from routes.role_routes import role_bp
    from routes.expense_routes import expense_bp
    
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(role_bp, url_prefix='/api/roles')
    app.register_blueprint(expense_bp, url_prefix='/api/expenses')
    
    # Root routes
    @app.route('/')
    def hello():
        return {
            'message': 'HR Management System API',
            'version': '1.0',
            'endpoints': {
                'health': '/health',
                'users': '/api/users',
                'roles': '/api/roles',
                'expenses': '/api/expenses'
            }
        }
    
    @app.route('/health')
    def health():
        return {
            'status': 'healthy',
            'database': 'connected',
            'upload_folder': app.config['UPLOAD_FOLDER']
        }
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5001)