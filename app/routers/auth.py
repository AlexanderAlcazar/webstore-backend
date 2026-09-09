from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
def register_user():
    pass


@router.post("/login")
def login_user():
    pass
