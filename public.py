from fastapi import APIRouter, Body, HTTPException, status
from models import UserSchema, UserLoginSchema
from auth.jwt_handler import signJWT
from database import db
from typing import List

router = APIRouter()

@router.post("/user/signup", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserSchema = Body(...)):
    existing_user = db.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    user.hash_password()
    
    user_data = user.dict()
    created_user = db.create_user(user_data)
    created_user.pop('password', None)
    return {
        "message": "User created successfully",
        "user": created_user,
        "token": signJWT(created_user['email'])
    }

@router.post("/user/login")
async def user_login(user: UserLoginSchema = Body(...)):
    stored_user = db.get_user_by_email(user.email)
    if not stored_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not UserSchema.verify_password(user.password, stored_user['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    return {
        "message": "Login successful",
        "token": signJWT(user.email)
    }

@router.get("/users", response_model=List[UserSchema])
async def get_all_users():
    users = db.get_all_users()
    for user in users:
        user.pop('password', None)
    return users