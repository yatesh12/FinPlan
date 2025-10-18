import torch
import torch.nn as nn
import numpy as np
from pathlib import Path
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

# Define the neural network architecture that matches your model
class PortfolioModel(nn.Module):
    def __init__(self, input_size=11, hidden_size=64, output_size=10):
        super(PortfolioModel, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size)
            # Removed Softmax - will apply manually during inference
        )
    
    def forward(self, x):
        return self.network(x)

class MLService:
    def __init__(self):
        self.model = None
        self.model_loaded = False
        self.feature_names = [
            "Risk_Appetite",
            "Age", 
            "Financial_Knowledge_Level",
            "Investment_Goal_Wealth_Growth",
            "Investment_Goal_Retirement",
            "Investment_Goal_Short_term_Gains", 
            "Investment_Goal_Tax_Saving",
            "Investment_Goal_Children_Education",
            "Investment_Horizon_Years",
            "Avg_Investment_Size_INR",
            "Cluster_ID"
        ]
        self.output_features = [
            "Alloc_Stocks",
            "Alloc_Bonds", 
            "Alloc_Mutual_Funds",
            "Alloc_ETFs",
            "Alloc_Real_Estate",
            "Alloc_Crypto",
            "Alloc_Commodities_Gold",
            "Alloc_Savings_Accounts", 
            "Alloc_Retirement_Plans",
            "Alloc_International_Equities"
        ]
    
    def load_model(self, model_path: str = "full_portfolio_model.pth"):
        """Load the PyTorch model"""
        try:
            model_file = Path(model_path)
            if not model_file.exists():
                logger.error(f"Model file not found: {model_path}")
                return False
            
            # Initialize model with correct architecture
            self.model = PortfolioModel()
            
            # Load the state dict (with weights_only=False for compatibility)
            state_dict = torch.load(model_file, map_location=torch.device('cpu'), weights_only=False)
            self.model.load_state_dict(state_dict)
            self.model.eval()
            
            self.model_loaded = True
            logger.info(f"Model loaded successfully from {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
    
    def map_profile_to_features(self, profile_data: Dict[str, Any]) -> Dict[str, float]:
        """Map profile data to ML model features"""
        features = {}
        
        # Risk Appetite - MORE EXTREME differentiation for better model sensitivity
        risk_mapping = {"low": 1, "medium": 3, "moderate": 3, "high": 5}
        risk_appetite = risk_mapping.get(profile_data.get("risk_tolerance", "medium"), 3)
        features["Risk_Appetite"] = risk_appetite
        
        # Age - use directly 
        age = float(profile_data.get("age", 30))
        features["Age"] = age
        
        # Financial Knowledge Level (0 or 1 as per your requirement)
        experience_mapping = {"beginner": 0, "intermediate": 1, "advanced": 1}
        features["Financial_Knowledge_Level"] = experience_mapping.get(
            profile_data.get("investment_experience", "beginner"), 0
        )
        
        # Investment Goals - binary features (0 or 1) with better parsing
        goals_text = profile_data.get("financial_goals", "").lower()
        
        # Try to parse JSON goals first
        try:
            import json
            goals_list = json.loads(profile_data.get("financial_goals", "[]"))
            if isinstance(goals_list, list) and goals_list:
                goal_names = " ".join([goal.get("name", "").lower() for goal in goals_list])
                goals_text += " " + goal_names
        except (json.JSONDecodeError, TypeError):
            pass
        
        # Enhanced keyword matching for goals
        features["Investment_Goal_Wealth_Growth"] = 1 if any(keyword in goals_text for keyword in 
            ["wealth", "growth", "portfolio", "investment", "money", "financial"]) else 0
        features["Investment_Goal_Retirement"] = 1 if any(keyword in goals_text for keyword in 
            ["retirement", "retire", "pension", "old age"]) else 0
        features["Investment_Goal_Short_term_Gains"] = 1 if any(keyword in goals_text for keyword in 
            ["short", "quick", "immediate", "emergency", "urgent"]) else 0
        features["Investment_Goal_Tax_Saving"] = 1 if any(keyword in goals_text for keyword in 
            ["tax", "saving", "elss", "80c", "deduction"]) else 0
        features["Investment_Goal_Children_Education"] = 1 if any(keyword in goals_text for keyword in 
            ["education", "child", "kids", "school", "college", "study"]) else 0
        
        # Investment Horizon - age and goal based
        if age < 30:
            base_horizon = 20
        elif age < 45:
            base_horizon = 15
        elif age < 55:
            base_horizon = 10
        else:
            base_horizon = 5
            
        # Adjust based on goals
        if features["Investment_Goal_Short_term_Gains"]:
            features["Investment_Horizon_Years"] = min(base_horizon, 3)
        elif features["Investment_Goal_Retirement"] and age < 50:
            features["Investment_Horizon_Years"] = max(base_horizon, 15)
        else:
            features["Investment_Horizon_Years"] = base_horizon
        
        # Average Investment Size - more realistic calculation
        monthly_income = float(profile_data.get("income", 50000))
        monthly_expenses = float(profile_data.get("expenses", 30000) or 30000)
        current_savings = float(profile_data.get("savings", 0) or 0)
        
        # Use actual savings if available, otherwise calculate potential
        if current_savings > 0:
            features["Avg_Investment_Size_INR"] = max(current_savings, 25000)
        else:
            monthly_surplus = max(monthly_income - monthly_expenses, monthly_income * 0.1)
            features["Avg_Investment_Size_INR"] = max(monthly_surplus * 6, 25000)
        
        # Cluster ID - ENHANCED risk-based clustering for maximum differentiation
        risk_score = risk_appetite
        age_factor = 2 if age < 35 else 1 if age < 50 else 0
        knowledge_factor = features["Financial_Knowledge_Level"] * 2
        horizon_factor = 1 if features["Investment_Horizon_Years"] > 10 else 0
        
        combined_score = risk_score + age_factor + knowledge_factor + horizon_factor
        
        # More aggressive clustering to force different outputs
        if risk_appetite == 5:  # High risk always gets aggressive cluster
            features["Cluster_ID"] = 1  # Aggressive
        elif risk_appetite == 1:  # Low risk always gets conservative cluster
            features["Cluster_ID"] = 3  # Conservative
        elif combined_score >= 6:
            features["Cluster_ID"] = 1  # Aggressive
        elif combined_score <= 4:
            features["Cluster_ID"] = 3  # Conservative  
        else:
            features["Cluster_ID"] = 2  # Moderate
        
        return features
    
    def normalize_features(self, features: Dict[str, float]) -> np.ndarray:
        """Normalize features for model input"""
        # Simple normalization - you may want to use the same scaler used during training
        normalized = []
        
        for feature_name in self.feature_names:
            value = features.get(feature_name, 0)
            
            # Apply basic normalization based on expected ranges
            if feature_name == "Age":
                normalized_value = (value - 25) / 40  # Age range 25-65
            elif feature_name == "Avg_Investment_Size_INR":
                normalized_value = np.log(value + 1) / 15  # Log scale for money
            elif feature_name == "Risk_Appetite":
                # Enhanced risk normalization - preserve extreme differences
                normalized_value = (value - 1) / 4  # Scale 1-5 to 0-1
            elif feature_name == "Financial_Knowledge_Level":
                normalized_value = value  # Keep binary 0/1
            else:
                normalized_value = value  # Binary features and others
            
            normalized.append(normalized_value)
        
        return np.array(normalized, dtype=np.float32)
    
    def apply_risk_adjustments(self, base_allocations: np.ndarray, features: Dict[str, float]) -> np.ndarray:
        """Apply risk-based adjustments to ensure meaningful portfolio differences"""
        risk_level = features.get("Risk_Appetite", 3)
        allocations = base_allocations.copy()
        
        # Asset indices based on self.output_features order
        indices = {
            "stocks": 0,      # Alloc_Stocks
            "bonds": 1,       # Alloc_Bonds  
            "mutual_funds": 2, # Alloc_Mutual_Funds
            "etfs": 3,        # Alloc_ETFs
            "real_estate": 4, # Alloc_Real_Estate
            "crypto": 5,      # Alloc_Crypto
            "gold": 6,        # Alloc_Commodities_Gold
            "savings": 7,     # Alloc_Savings_Accounts
            "retirement": 8,  # Alloc_Retirement_Plans
            "intl_equity": 9  # Alloc_International_Equities
        }
        
        if risk_level == 1:  # LOW RISK - Conservative approach
            # Increase safe assets significantly
            allocations[indices["bonds"]] *= 1.8      # Boost bonds
            allocations[indices["savings"]] *= 1.6    # Boost savings
            allocations[indices["retirement"]] *= 1.4 # Boost retirement
            
            # Decrease risky assets significantly  
            allocations[indices["stocks"]] *= 0.3     # Reduce stocks
            allocations[indices["crypto"]] *= 0.2     # Minimize crypto
            allocations[indices["etfs"]] *= 0.5       # Reduce ETFs
            
        elif risk_level == 5:  # HIGH RISK - Aggressive approach
            # Increase risky assets significantly
            allocations[indices["stocks"]] *= 2.5     # Boost stocks significantly
            allocations[indices["crypto"]] *= 3.0     # Boost crypto significantly
            allocations[indices["etfs"]] *= 2.0       # Boost ETFs
            allocations[indices["intl_equity"]] *= 1.8 # Boost international
            
            # Decrease safe assets
            allocations[indices["bonds"]] *= 0.4      # Reduce bonds
            allocations[indices["savings"]] *= 0.5    # Reduce savings
            
        else:  # MEDIUM RISK - Moderate adjustments
            # Slight adjustments for balanced approach
            allocations[indices["stocks"]] *= 1.2     # Slight stock increase
            allocations[indices["bonds"]] *= 1.1      # Slight bond increase
            allocations[indices["crypto"]] *= 0.8     # Slight crypto reduction
        
        # Re-normalize to ensure they sum to 1.0 after adjustments
        allocations = allocations / allocations.sum()
        
        return allocations
    
    def predict_portfolio(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict portfolio allocation based on profile data"""
        if not self.model_loaded:
            if not self.load_model():
                return {"error": "Model not available"}
        
        try:
            # Map profile to features
            features = self.map_profile_to_features(profile_data)
            
            # Debug: Log extracted features for different users
            logger.info(f"Extracted features for user: {features}")
            
            # Normalize features
            normalized_features = self.normalize_features(features)
            
            # Debug: Log normalized features
            logger.info(f"Normalized features: {normalized_features.tolist()}")
            
            # Convert to tensor
            input_tensor = torch.FloatTensor(normalized_features).unsqueeze(0)
            
            # Make prediction
            with torch.no_grad():
                logits = self.model(input_tensor)
                # Apply softmax normalization to logits
                probabilities = torch.softmax(logits, dim=1)
                base_allocations = probabilities.squeeze().numpy()
                
                # ENHANCED: Apply risk-based adjustments to ensure meaningful differences
                allocations = self.apply_risk_adjustments(base_allocations, features)
                
                # Debug: Log softmax normalization 
                logger.info(f"Applied softmax normalization - probabilities sum: {allocations.sum():.6f}")
                logger.info(f"Risk level: {features['Risk_Appetite']}, Cluster: {features['Cluster_ID']}")
            
            # Convert to percentages and create result
            result = {
                "allocations": {},
                "features_used": features,
                "total_allocation": 0
            }
            
            # Convert to percentages first
            percentages = [float(allocation * 100) for allocation in allocations]
            
            # Ensure they sum to exactly 100% by normalizing
            total_before_norm = sum(percentages)
            if total_before_norm > 0:
                percentages = [p * 100.0 / total_before_norm for p in percentages]
            
            for i, percentage in enumerate(percentages):
                asset_name = self.output_features[i]
                result["allocations"][asset_name] = round(percentage, 2)
            
            # Calculate total from rounded values
            result["total_allocation"] = sum(result["allocations"].values())
            
            return result
            
        except Exception as e:
            logger.error(f"Error predicting portfolio: {e}")
            return {"error": str(e)}

# Global instance
ml_service = MLService()