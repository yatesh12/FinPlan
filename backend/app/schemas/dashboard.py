from pydantic import BaseModel
from typing import Optional, Dict, Any

class DashboardResponse(BaseModel):
    """Response schema for dashboard data"""
    user_id: int
    data: Dict[str, Any]
    
    class Config:
        extra = "allow"  # Allow additional fields

class DashboardData(BaseModel):
    """Schema for dashboard data"""
    
    class Config:
        extra = "allow"  # Allow additional fields to accommodate flexible profile data