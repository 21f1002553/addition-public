import uuid
from datetime import datetime, date
from app import db
import json

class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    users = db.relationship('User', backref='role', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    role_id = db.Column(db.String(36), db.ForeignKey('roles.id'), nullable=False)
    status = db.Column(db.String(50), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    job_posts = db.relationship('JobPost', backref='posted_by', lazy=True)
    resumes = db.relationship('Resume', backref='owner', lazy=True)
    applications = db.relationship('Application', backref='candidate', lazy=True)
    interviews_as_interviewer = db.relationship('Interview', backref='interviewer', lazy=True)
    enrollments = db.relationship('Enrollment', backref='user', lazy=True)
    reports = db.relationship('Report', foreign_keys='Report.user_id', backref='user', lazy=True)
    approved_reports = db.relationship('Report', foreign_keys='Report.approved_by', backref='approver', lazy=True)
    employee_reviews = db.relationship('PerformanceReview', foreign_keys='PerformanceReview.employee_id', backref='employee', lazy=True)
    reviewer_reviews = db.relationship('PerformanceReview', foreign_keys='PerformanceReview.reviewer_id', backref='reviewer', lazy=True)
    notifications = db.relationship('Notification', backref='recipient', lazy=True)
    audit_logs = db.relationship('AuditLog', backref='actor', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role_id': self.role_id,
            'role_name': self.role.name if self.role else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class JobPost(db.Model):
    __tablename__ = 'job_posts'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    requirements = db.Column(db.Text)
    posted_by_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='active')
    
    applications = db.relationship('Application', backref='job', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'requirements': self.requirements,
            'posted_by_id': self.posted_by_id,
            'posted_by_name': self.posted_by.name if self.posted_by else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'status': self.status
        }

class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    file_url = db.Column(db.String(500))
    parsed_data = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    applications = db.relationship('Application', backref='resume', lazy=True)
    
    def get_parsed_data(self):
        return json.loads(self.parsed_data) if self.parsed_data else {}
    
    def set_parsed_data(self, data):
        self.parsed_data = json.dumps(data)
    
    def to_dict(self):
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'owner_name': self.owner.name if self.owner else None,
            'file_url': self.file_url,
            'parsed_data': self.get_parsed_data(),
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }

class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    candidate_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.String(36), db.ForeignKey('job_posts.id'), nullable=False)
    resume_id = db.Column(db.String(36), db.ForeignKey('resumes.id'), nullable=False)
    status = db.Column(db.String(50), default='applied')
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Float)
    
    interviews = db.relationship('Interview', backref='application', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'candidate_name': self.candidate.name if self.candidate else None,
            'job_id': self.job_id,
            'job_title': self.job.title if self.job else None,
            'resume_id': self.resume_id,
            'status': self.status,
            'applied_at': self.applied_at.isoformat() if self.applied_at else None,
            'score': self.score
        }

class Interview(db.Model):
    __tablename__ = 'interviews'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    application_id = db.Column(db.String(36), db.ForeignKey('applications.id'), nullable=False)
    scheduled_at = db.Column(db.DateTime, nullable=False)
    interviewer_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), default='scheduled')
    feedback = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'application_id': self.application_id,
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'interviewer_id': self.interviewer_id,
            'interviewer_name': self.interviewer.name if self.interviewer else None,
            'status': self.status,
            'feedback': self.feedback
        }

class Training(db.Model):
    __tablename__ = 'trainings'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
    courses = db.relationship('Course', backref='training', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None
        }

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    training_id = db.Column(db.String(36), db.ForeignKey('trainings.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content_url = db.Column(db.String(500))
    duration_mins = db.Column(db.Integer)
    
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'training_id': self.training_id,
            'training_title': self.training.title if self.training else None,
            'title': self.title,
            'content_url': self.content_url,
            'duration_mins': self.duration_mins
        }

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.String(36), db.ForeignKey('courses.id'), nullable=False)
    progress = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(50), default='enrolled')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'course_id': self.course_id,
            'course_title': self.course.title if self.course else None,
            'progress': self.progress,
            'status': self.status
        }

class Report(db.Model):
    __tablename__ = 'reports'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    
    eod_report = db.relationship('EODReport', backref='report', uselist=False, lazy=True)
    expense_report = db.relationship('ExpenseReport', backref='report', uselist=False, lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'type': self.type,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'approved_by': self.approved_by,
            'approved_by_name': self.approver.name if self.approver else None
        }

class EODReport(db.Model):
    __tablename__ = 'eod_reports'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    report_id = db.Column(db.String(36), db.ForeignKey('reports.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    tasks = db.Column(db.Text)
    ai_summary = db.Column(db.Text)
    
    def get_tasks(self):
        return json.loads(self.tasks) if self.tasks else []
    
    def set_tasks(self, tasks):
        self.tasks = json.dumps(tasks)
    
    def to_dict(self):
        return {
            'id': self.id,
            'report_id': self.report_id,
            'date': self.date.isoformat() if self.date else None,
            'tasks': self.get_tasks(),
            'ai_summary': self.ai_summary
        }

class ExpenseReport(db.Model):
    __tablename__ = 'expense_reports'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    report_id = db.Column(db.String(36), db.ForeignKey('reports.id'), nullable=False)
    items = db.Column(db.Text)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')
    
    def get_items(self):
        return json.loads(self.items) if self.items else []
    
    def set_items(self, items):
        self.items = json.dumps(items)
    
    def to_dict(self):
        return {
            'id': self.id,
            'report_id': self.report_id,
            'items': self.get_items(),
            'total': self.total,
            'status': self.status
        }

class PerformanceReview(db.Model):
    __tablename__ = 'performance_reviews'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    reviewer_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text)
    rating = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': self.employee.name if self.employee else None,
            'reviewer_id': self.reviewer_id,
            'reviewer_name': self.reviewer.name if self.reviewer else None,
            'type': self.type,
            'text': self.text,
            'rating': self.rating,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    recipient_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'recipient_id': self.recipient_id,
            'recipient_name': self.recipient.name if self.recipient else None,
            'message': self.message,
            'read': self.read,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    actor_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    target_type = db.Column(db.String(50), nullable=False)
    target_id = db.Column(db.String(36), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'actor_id': self.actor_id,
            'actor_name': self.actor.name if self.actor else None,
            'action': self.action,
            'target_type': self.target_type,
            'target_id': self.target_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
