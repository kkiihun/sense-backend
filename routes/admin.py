from fastapi import APIRouter, Depends
from dependencies.security import get_current_admin
from schemas.user import UserOut

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/dashboard", response_model=UserOut)
def admin_dashboard(current_admin = Depends(get_current_admin)):
    return current_admin
