import unittest
import json
import os
from app import create_app, db
from models import User, Role, Report, ExpenseReport
from datetime import datetime


class ExpenseAPITestCase(unittest.TestCase):
    """Test cases for Expense Management API"""
    
    def setUp(self):
        """Set up test client and database"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            self._create_test_data()
    
    def tearDown(self):
        """Clean up after tests"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def _create_test_data(self):
        """Create test users and roles"""
        # Create roles
        admin_role = Role(name='Admin', description='Administrator')
        employee_role = Role(name='Employee', description='Regular employee')
        manager_role = Role(name='Manager', description='Manager')
        
        db.session.add_all([admin_role, employee_role, manager_role])
        db.session.flush()
        
        # Create users
        self.admin_user = User(
            name='Admin User',
            email='admin@test.com',
            role_id=admin_role.id,
            status='active'
        )
        
        self.employee_user = User(
            name='John Doe',
            email='john@test.com',
            role_id=employee_role.id,
            status='active'
        )
        
        self.manager_user = User(
            name='Jane Manager',
            email='jane@test.com',
            role_id=manager_role.id,
            status='active'
        )
        
        db.session.add_all([self.admin_user, self.employee_user, self.manager_user])
        db.session.commit()
    
    def test_submit_expense_success(self):
        """Test successful expense submission"""
        with self.app.app_context():
            data = {
                'user_id': self.employee_user.id,
                'category': 'Food',
                'amount': '50.00',
                'description': 'Team lunch meeting',
                'trip_id': 'Q4-2024'
            }
            
            response = self.client.post('/api/expenses/submit', data=data)
            self.assertEqual(response.status_code, 201)
            
            response_data = json.loads(response.data)
            self.assertTrue(response_data['success'])
            self.assertIn('expense_id', response_data['data'])
            self.assertEqual(response_data['data']['status'], 'pending')
    
    def test_submit_expense_missing_fields(self):
        """Test expense submission with missing required fields"""
        with self.app.app_context():
            data = {
                'user_id': self.employee_user.id,
                'category': 'Food',
                # Missing amount and description
            }
            
            response = self.client.post('/api/expenses/submit', data=data)
            self.assertEqual(response.status_code, 400)
            
            response_data = json.loads(response.data)
            self.assertIn('error', response_data)
    
    def test_submit_expense_invalid_amount(self):
        """Test expense submission with invalid amount"""
        with self.app.app_context():
            data = {
                'user_id': self.employee_user.id,
                'category': 'Food',
                'amount': '-50.00',  # Negative amount
                'description': 'Test'
            }
            
            response = self.client.post('/api/expenses/submit', data=data)
            self.assertEqual(response.status_code, 400)
    
    def test_submit_expense_user_not_found(self):
        """Test expense submission with non-existent user"""
        data = {
            'user_id': 'non-existent-uuid',
            'category': 'Food',
            'amount': '50.00',
            'description': 'Test'
        }
        
        response = self.client.post('/api/expenses/submit', data=data)
        self.assertEqual(response.status_code, 404)
    
    def test_get_all_expenses(self):
        """Test retrieving all expenses"""
        with self.app.app_context():
            # Create test expenses
            self._create_test_expenses()
            
            response = self.client.get('/api/expenses/')
            self.assertEqual(response.status_code, 200)
            
            response_data = json.loads(response.data)
            self.assertIn('data', response_data)
            self.assertIn('pagination', response_data)
            self.assertGreater(len(response_data['data']), 0)
    
    def test_get_expenses_with_filters(self):
        """Test retrieving expenses with filters"""
        with self.app.app_context():
            self._create_test_expenses()
            
            # Filter by status
            response = self.client.get('/api/expenses/?status=pending')
            self.assertEqual(response.status_code, 200)
            
            response_data = json.loads(response.data)
            for expense in response_data['data']:
                self.assertEqual(expense['status'], 'pending')
    
    def test_get_expenses_pagination(self):
        """Test expense pagination"""
        with self.app.app_context():
            # Create multiple expenses
            for i in range(15):
                self._create_single_expense(amount=10.0 + i)
            
            # Get first page
            response = self.client.get('/api/expenses/?page=1&limit=5')
            self.assertEqual(response.status_code, 200)
            
            response_data = json.loads(response.data)
            self.assertEqual(len(response_data['data']), 5)
            self.assertEqual(response_data['pagination']['current_page'], 1)
            self.assertGreaterEqual(response_data['pagination']['total_pages'], 3)
    
    def test_get_single_expense(self):
        """Test retrieving a single expense"""
        with self.app.app_context():
            expense_id = self._create_single_expense()
            
            response = self.client.get(f'/api/expenses/{expense_id}')
            self.assertEqual(response.status_code, 200)
            
            response_data = json.loads(response.data)
            self.assertEqual(response_data['id'], expense_id)
    
    def test_get_single_expense_not_found(self):
        """Test retrieving non-existent expense"""
        response = self.client.get('/api/expenses/non-existent-id')
        self.assertEqual(response.status_code, 404)
    
    def test_approve_expense_success(self):
        """Test successful expense approval"""
        with self.app.app_context():
            expense_id = self._create_single_expense()
            
            data = {
                'approver_id': self.manager_user.id,
                'comments': 'Approved - Valid expense'
            }
            
            response = self.client.put(
                f'/api/expenses/{expense_id}/approve',
                data=json.dumps(data),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.data)
            self.assertTrue(response_data['success'])
            self.assertEqual(response_data['data']['status'], 'approved')
    
    def test_approve_expense_missing_approver(self):
        """Test approval without approver_id"""
        with self.app.app_context():
            expense_id = self._create_single_expense()
            
            data = {
                'comments': 'Approved'
            }
            
            response = self.client.put(
                f'/api/expenses/{expense_id}/approve',
                data=json.dumps(data),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 400)
    
    def test_approve_already_approved_expense(self):
        """Test approving an already approved expense"""
        with self.app.app_context():
            expense_id = self._create_single_expense(status='approved')
            
            data = {
                'approver_id': self.manager_user.id,
                'comments': 'Approved'
            }
            
            response = self.client.put(
                f'/api/expenses/{expense_id}/approve',
                data=json.dumps(data),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 400)
    
    def test_reject_expense_success(self):
        """Test successful expense rejection"""
        with self.app.app_context():
            expense_id = self._create_single_expense()
            
            data = {
                'approver_id': self.manager_user.id,
                'reason': 'Invalid receipt'
            }
            
            response = self.client.put(
                f'/api/expenses/{expense_id}/reject',
                data=json.dumps(data),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.data)
            self.assertTrue(response_data['success'])
            self.assertEqual(response_data['data']['status'], 'rejected')
    
    def test_reject_expense_missing_reason(self):
        """Test rejection without reason"""
        with self.app.app_context():
            expense_id = self._create_single_expense()
            
            data = {
                'approver_id': self.manager_user.id
            }
            
            response = self.client.put(
                f'/api/expenses/{expense_id}/reject',
                data=json.dumps(data),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 400)
    
    def test_get_pending_expenses(self):
        """Test retrieving pending expenses"""
        with self.app.app_context():
            # Create mix of pending and approved expenses
            self._create_single_expense(status='pending')
            self._create_single_expense(status='pending')
            self._create_single_expense(status='approved')
            
            response = self.client.get('/api/expenses/pending')
            self.assertEqual(response.status_code, 200)
            
            response_data = json.loads(response.data)
            self.assertEqual(len(response_data['data']), 2)
            for expense in response_data['data']:
                self.assertEqual(expense['status'], 'pending')
    
    def test_get_expense_reports_summary(self):
        """Test expense reports and analytics"""
        with self.app.app_context():
            # Create expenses with different categories
            self._create_single_expense(amount=100.0, category='Food')
            self._create_single_expense(amount=200.0, category='Travel')
            self._create_single_expense(amount=50.0, category='Food')
            
            response = self.client.get('/api/expenses/reports')
            self.assertEqual(response.status_code, 200)
            
            response_data = json.loads(response.data)
            self.assertIn('summary', response_data)
            self.assertIn('category_breakdown', response_data)
            self.assertEqual(response_data['summary']['total_expenses'], 350.0)
    
    def test_policy_check_compliant(self):
        """Test policy check for compliant expense"""
        with self.app.app_context():
            expense_id = self._create_single_expense(amount=30.0, category='Food')
            
            response = self.client.get(f'/api/expenses/policy-check/{expense_id}')
            self.assertEqual(response.status_code, 200)
            
            response_data = json.loads(response.data)
            self.assertTrue(response_data['is_compliant'])
            self.assertEqual(len(response_data['violations']), 0)
    
    def test_policy_check_violation(self):
        """Test policy check for non-compliant expense"""
        with self.app.app_context():
            # Create expense exceeding per-meal limit
            expense_id = self._create_single_expense(amount=80.0, category='Food')
            
            response = self.client.get(f'/api/expenses/policy-check/{expense_id}')
            self.assertEqual(response.status_code, 200)
            
            response_data = json.loads(response.data)
            self.assertFalse(response_data['is_compliant'])
            self.assertGreater(len(response_data['violations']), 0)
    
    def test_update_expense_success(self):
        """Test updating a pending expense"""
        with self.app.app_context():
            expense_id = self._create_single_expense(amount=50.0)
            
            data = {
                'items': [{
                    'category': 'Food',
                    'amount': 60.0,
                    'description': 'Updated description',
                    'expense_date': '2024-07-28'
                }],
                'total': 60.0
            }
            
            response = self.client.put(
                f'/api/expenses/{expense_id}',
                data=json.dumps(data),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.data)
            self.assertEqual(response_data['data']['total'], 60.0)
    
    def test_update_approved_expense_fails(self):
        """Test that approved expenses cannot be updated"""
        with self.app.app_context():
            expense_id = self._create_single_expense(status='approved')
            
            data = {
                'items': [{
                    'category': 'Food',
                    'amount': 60.0,
                    'description': 'Updated',
                    'expense_date': '2024-07-28'
                }],
                'total': 60.0
            }
            
            response = self.client.put(
                f'/api/expenses/{expense_id}',
                data=json.dumps(data),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 400)
    
    def test_delete_expense_success(self):
        """Test deleting a pending expense"""
        with self.app.app_context():
            expense_id = self._create_single_expense()
            
            response = self.client.delete(f'/api/expenses/{expense_id}')
            self.assertEqual(response.status_code, 200)
            
            # Verify deletion
            response = self.client.get(f'/api/expenses/{expense_id}')
            self.assertEqual(response.status_code, 404)
    
    def test_delete_approved_expense_fails(self):
        """Test that approved expenses cannot be deleted"""
        with self.app.app_context():
            expense_id = self._create_single_expense(status='approved')
            
            response = self.client.delete(f'/api/expenses/{expense_id}')
            self.assertEqual(response.status_code, 400)
    
    # Helper methods
    
    def _create_test_expenses(self):
        """Create multiple test expenses"""
        self._create_single_expense(amount=50.0, status='pending')
        self._create_single_expense(amount=100.0, status='approved')
        self._create_single_expense(amount=75.0, status='rejected')
    
    def _create_single_expense(self, amount=50.0, status='pending', category='Food'):
        """Create a single test expense and return its ID"""
        report = Report(
            user_id=self.employee_user.id,
            type='expense'
        )
        db.session.add(report)
        db.session.flush()
        
        items = [{
            'category': category,
            'amount': amount,
            'description': 'Test expense',
            'expense_date': '2024-07-28'
        }]
        
        expense = ExpenseReport(
            report_id=report.id,
            total=amount,
            status=status
        )
        expense.set_items(items)
        
        db.session.add(expense)
        db.session.commit()
        
        return expense.id


if __name__ == '__main__':
    unittest.main()