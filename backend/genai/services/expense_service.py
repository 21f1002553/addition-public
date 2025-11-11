from ..prompt import PromptManager
from ..llm_factory import LLMModelFactory
from ...utils import TextUtility
import json


class ExpenseService:
    """
    AI-powered expense verification and analysis service
    """
    
    def __init__(self, model_name: str = 'gemini'):
        self.model_name = model_name
    
    def verify_expense_receipt(self, receipt_text: str, claimed_amount: float, category: str):
        """
        Verify expense receipt using AI
        Extracts information from receipt and compares with claimed amount
        """
        prompt = f"""
        You are an expert expense auditor.
        Analyze the following receipt text and verify the expense claim.
        
        Receipt Text:
        {receipt_text}
        
        Claimed Information:
        - Amount: ${claimed_amount}
        - Category: {category}
        
        Extract and verify the following information from the receipt:
        Respond only in valid JSON format with the following structure:
        {{
            "extracted_amount": 0.0,
            "extracted_vendor": "",
            "extracted_date": "",
            "extracted_items": [],
            "matches_claimed_amount": true/false,
            "confidence_score": 0.0-1.0,
            "discrepancy": 0.0,
            "flags": [],
            "recommendation": ""
        }}
        
        Rules:
        - Compare extracted amount with claimed amount
        - Flag if discrepancy > $5 or > 10%
        - Confidence score based on receipt clarity
        - Provide specific recommendations
        - Output only valid JSON
        """
        
        try:
            if self.model_name == "gemini":
                model = LLMModelFactory.get_model_provider('gemini').get_model()
                response = model.generate_content(prompt)
                result = response.text
            elif self.model_name == "chatgpt":
                model = LLMModelFactory.get_model_provider('chatgpt').get_model()
                result = model.generate_content(prompt)
            else:
                raise ValueError(f"Unsupported model: {self.model_name}")
            
            # Clean and parse JSON response
            result = TextUtility.remove_json_marker(result)
            return result
        
        except Exception as e:
            return {
                "error": str(e),
                "extracted_amount": claimed_amount,
                "matches_claimed_amount": True,
                "confidence_score": 0.0,
                "recommendation": "Unable to verify automatically. Manual review required."
            }
    
    def check_policy_compliance(self, expense_data: dict, policy_limits: dict):
        """
        Check if expense complies with company policy using AI
        """
        prompt = f"""
        You are a company policy compliance expert.
        Review the following expense against company policy.
        
        Expense Details:
        {json.dumps(expense_data, indent=2)}
        
        Policy Limits:
        {json.dumps(policy_limits, indent=2)}
        
        Analyze and respond in valid JSON format:
        {{
            "is_compliant": true/false,
            "violations": [
                {{
                    "rule": "",
                    "severity": "high|medium|low",
                    "description": ""
                }}
            ],
            "warnings": [],
            "approval_recommendation": "approve|review|reject",
            "reasoning": ""
        }}
        
        Rules:
        - Check all policy limits
        - Identify any violations
        - Consider context and reasonableness
        - Provide clear reasoning
        - Output only valid JSON
        """
        
        try:
            if self.model_name == "gemini":
                model = LLMModelFactory.get_model_provider('gemini').get_model()
                response = model.generate_content(prompt)
                result = response.text
            elif self.model_name == "chatgpt":
                model = LLMModelFactory.get_model_provider('chatgpt').get_model()
                result = model.generate_content(prompt)
            else:
                raise ValueError(f"Unsupported model: {self.model_name}")
            
            result = TextUtility.remove_json_marker(result)
            return result
        
        except Exception as e:
            return {
                "error": str(e),
                "is_compliant": True,
                "approval_recommendation": "review",
                "reasoning": "Unable to verify automatically. Manual review required."
            }
    
    def categorize_expense(self, description: str, amount: float):
        """
        Automatically categorize expense based on description
        """
        prompt = f"""
        You are an expense categorization expert.
        Categorize the following expense into the most appropriate category.
        
        Description: {description}
        Amount: ${amount}
        
        Available Categories:
        - Travel (flights, trains, taxis, rental cars)
        - Food (meals, snacks, beverages)
        - Supplies (office supplies, equipment)
        - Accommodation (hotels, lodging)
        - Entertainment (client entertainment, team events)
        - Other
        
        Respond in valid JSON format:
        {{
            "category": "",
            "subcategory": "",
            "confidence": 0.0-1.0,
            "reasoning": ""
        }}
        
        Rules:
        - Choose the most specific category
        - Provide confidence score
        - Explain reasoning briefly
        - Output only valid JSON
        """
        
        try:
            if self.model_name == "gemini":
                model = LLMModelFactory.get_model_provider('gemini').get_model()
                response = model.generate_content(prompt)
                result = response.text
            elif self.model_name == "chatgpt":
                model = LLMModelFactory.get_model_provider('chatgpt').get_model()
                result = model.generate_content(prompt)
            else:
                raise ValueError(f"Unsupported model: {self.model_name}")
            
            result = TextUtility.remove_json_marker(result)
            return result
        
        except Exception as e:
            return {
                "error": str(e),
                "category": "Other",
                "confidence": 0.0,
                "reasoning": "Unable to categorize automatically."
            }
    
    def detect_duplicate_expenses(self, new_expense: dict, existing_expenses: list):
        """
        Detect potential duplicate expense submissions using AI
        """
        prompt = f"""
        You are a fraud detection expert specializing in duplicate expense detection.
        
        New Expense:
        {json.dumps(new_expense, indent=2)}
        
        Recent Expenses (last 30 days):
        {json.dumps(existing_expenses, indent=2)}
        
        Analyze if the new expense is a potential duplicate of any existing expense.
        Consider:
        - Similar amounts (within 10%)
        - Same date or nearby dates
        - Same vendor/merchant
        - Similar descriptions
        
        Respond in valid JSON format:
        {{
            "is_duplicate": true/false,
            "duplicate_probability": 0.0-1.0,
            "matching_expenses": [
                {{
                    "expense_id": "",
                    "similarity_score": 0.0-1.0,
                    "matching_factors": []
                }}
            ],
            "recommendation": "",
            "action": "approve|flag|reject"
        }}
        
        Rules:
        - High similarity (>0.8) = likely duplicate
        - Medium similarity (0.5-0.8) = flag for review
        - Low similarity (<0.5) = probably not duplicate
        - Output only valid JSON
        """
        
        try:
            if self.model_name == "gemini":
                model = LLMModelFactory.get_model_provider('gemini').get_model()
                response = model.generate_content(prompt)
                result = response.text
            elif self.model_name == "chatgpt":
                model = LLMModelFactory.get_model_provider('chatgpt').get_model()
                result = model.generate_content(prompt)
            else:
                raise ValueError(f"Unsupported model: {self.model_name}")
            
            result = TextUtility.remove_json_marker(result)
            return result
        
        except Exception as e:
            return {
                "error": str(e),
                "is_duplicate": False,
                "duplicate_probability": 0.0,
                "recommendation": "Unable to check for duplicates automatically."
            }
    
    def generate_expense_summary(self, expenses: list, period: str):
        """
        Generate AI-powered summary of expenses for a period
        """
        prompt = f"""
        You are a financial analyst.
        Generate a comprehensive summary of the following expenses for {period}.
        
        Expenses:
        {json.dumps(expenses, indent=2)}
        
        Provide insights on:
        - Total spending by category
        - Spending patterns and trends
        - Unusual or outlier expenses
        - Cost-saving opportunities
        - Policy compliance issues
        
        Respond in valid JSON format:
        {{
            "total_amount": 0.0,
            "expense_count": 0,
            "category_breakdown": {{}},
            "key_insights": [],
            "trends": [],
            "outliers": [],
            "recommendations": [],
            "executive_summary": ""
        }}
        
        Rules:
        - Provide actionable insights
        - Highlight important patterns
        - Keep summary concise but informative
        - Output only valid JSON
        """
        
        try:
            if self.model_name == "gemini":
                model = LLMModelFactory.get_model_provider('gemini').get_model()
                response = model.generate_content(prompt)
                result = response.text
            elif self.model_name == "chatgpt":
                model = LLMModelFactory.get_model_provider('chatgpt').get_model()
                result = model.generate_content(prompt)
            else:
                raise ValueError(f"Unsupported model: {self.model_name}")
            
            result = TextUtility.remove_json_marker(result)
            return result
        
        except Exception as e:
            return {
                "error": str(e),
                "executive_summary": "Unable to generate summary automatically."
            }
    
    def suggest_expense_optimization(self, user_expense_history: list):
        """
        Suggest ways to optimize expenses based on historical data
        """
        prompt = f"""
        You are a cost optimization consultant.
        Analyze the employee's expense history and suggest optimization strategies.
        
        Expense History:
        {json.dumps(user_expense_history, indent=2)}
        
        Provide recommendations on:
        - Recurring expenses that could be reduced
        - Better alternatives or vendors
        - Travel and accommodation optimization
        - Meal and entertainment efficiency
        
        Respond in valid JSON format:
        {{
            "total_potential_savings": 0.0,
            "optimization_opportunities": [
                {{
                    "category": "",
                    "current_average": 0.0,
                    "suggested_target": 0.0,
                    "potential_savings": 0.0,
                    "recommendations": []
                }}
            ],
            "best_practices": [],
            "priority_actions": []
        }}
        
        Rules:
        - Be realistic and practical
        - Consider business needs
        - Prioritize high-impact opportunities
        - Output only valid JSON
        """
        
        try:
            if self.model_name == "gemini":
                model = LLMModelFactory.get_model_provider('gemini').get_model()
                response = model.generate_content(prompt)
                result = response.text
            elif self.model_name == "chatgpt":
                model = LLMModelFactory.get_model_provider('chatgpt').get_model()
                result = model.generate_content(prompt)
            else:
                raise ValueError(f"Unsupported model: {self.model_name}")
            
            result = TextUtility.remove_json_marker(result)
            return result
        
        except Exception as e:
            return {
                "error": str(e),
                "optimization_opportunities": [],
                "best_practices": []
            }


# Create singleton instance
expense_service = ExpenseService()