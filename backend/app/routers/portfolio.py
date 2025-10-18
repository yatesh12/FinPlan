from fastapi import APIRouter, Depends, HTTPException, status
from ..middleware.auth import get_current_user, CurrentUser
from ..models.profile import ProfileModel
from ..services.ml_service import ml_service
from typing import Dict, Any

router = APIRouter()

@router.get("/predict")
async def predict_portfolio(
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Predict optimal portfolio allocation based on user profile
    """
    try:
        # Get user profile data
        profile_data = await ProfileModel.get_profile_by_user_id(current_user.userId)
        
        if not profile_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No profile found. Please complete your profile first."
            )
        
        # Get portfolio prediction from ML service
        prediction = ml_service.predict_portfolio(profile_data)
        
        if "error" in prediction:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Prediction failed: {prediction['error']}"
            )
        
        return {
            "user_id": current_user.userId,
            "portfolio_prediction": prediction,
            "message": "Portfolio prediction generated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Portfolio prediction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate portfolio prediction"
        )

@router.get("/allocations")
async def get_portfolio_allocations(
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Get simplified portfolio allocations for dashboard display
    """
    try:
        # Get user profile data
        profile_data = await ProfileModel.get_profile_by_user_id(current_user.userId)
        
        if not profile_data:
            # Return default allocations if no profile
            return {
                "allocations": {
                    "Stocks": 30,
                    "Bonds": 20,
                    "Mutual Funds": 25,
                    "ETFs": 15,
                    "Real Estate": 10
                },
                "message": "Default allocation shown. Complete your profile for personalized recommendations."
            }
        
        # Get prediction
        prediction = ml_service.predict_portfolio(profile_data)
        
        if "error" in prediction:
            # Return conservative default on error
            return {
                "allocations": {
                    "Stocks": 20,
                    "Bonds": 40,
                    "Mutual Funds": 25,
                    "Savings": 15
                },
                "message": "Default conservative allocation shown due to prediction error."
            }
        
        # Simplify allocations for frontend display
        allocations = prediction["allocations"]
        simplified = {}
        
        # Group related assets
        simplified["Stocks"] = (
            allocations.get("Alloc_Stocks", 0) + 
            allocations.get("Alloc_International_Equities", 0)
        )
        simplified["Bonds"] = allocations.get("Alloc_Bonds", 0)
        simplified["Mutual Funds"] = allocations.get("Alloc_Mutual_Funds", 0)
        simplified["ETFs"] = allocations.get("Alloc_ETFs", 0)
        simplified["Real Estate"] = allocations.get("Alloc_Real_Estate", 0)
        simplified["Crypto"] = allocations.get("Alloc_Crypto", 0)
        simplified["Gold"] = allocations.get("Alloc_Commodities_Gold", 0)
        simplified["Savings"] = allocations.get("Alloc_Savings_Accounts", 0)
        simplified["Retirement"] = allocations.get("Alloc_Retirement_Plans", 0)
        
        # Filter out zero allocations
        filtered_allocations = {k: round(v, 1) for k, v in simplified.items() if v > 0.5}
        
        return {
            "allocations": filtered_allocations,
            "total_allocation": sum(filtered_allocations.values()),
            "risk_level": profile_data.get("risk_tolerance", "medium"),
            "message": "Personalized portfolio allocation based on your profile"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Portfolio allocations error: {e}")
        # Return default allocation on any error
        return {
            "allocations": {
                "Stocks": 25,
                "Bonds": 30,
                "Mutual Funds": 30,
                "Savings": 15
            },
            "message": "Default allocation shown due to system error."
        }

@router.post("/feedback")
async def portfolio_feedback(
    feedback_data: Dict[str, Any],
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Collect user feedback on portfolio recommendations
    """
    try:
        # Log feedback for model improvement
        print(f"Portfolio feedback from user {current_user.userId}: {feedback_data}")
        
        # Here you could store feedback in database for model retraining
        # await FeedbackModel.create_feedback(current_user.userId, feedback_data)
        
        return {
            "message": "Thank you for your feedback!",
            "feedback_received": True
        }
        
    except Exception as e:
        print(f"Portfolio feedback error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to record feedback"
        )