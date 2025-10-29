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
    
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    from models import (
        Role, User, JobPost, Resume, Application, Interview,
        Training, Course, Enrollment, Report, EODReport, ExpenseReport,
        PerformanceReview, Notification, AuditLog
    )
    
    from routes.user_routes import user_bp
    from routes.role_routes import role_bp
    
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(role_bp, url_prefix='/api/roles')
    
    @app.route('/')
    def hello():
        return {'message': 'HR Management System API', 'version': '1.0'}
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
