from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserSchema(BaseModel):
    id: Optional[str] = None
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    created_at: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "johndoe@example.com",
                "password": "password123"
            }
        }
    
    def hash_password(self):
        self.password = pwd_context.hash(self.password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "johndoe@example.com",
                "password": "password123"
            }
        }


class ProductSchema(BaseModel):
    id: Optional[str] = None
    name: str = Field(...)
    description: str = Field(...)
    price: float = Field(...)
    stock: int = Field(...)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Product 1",
                "description": "This is product 1",
                "price": 99.99,
                "stock": 100
            }
        }

class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None