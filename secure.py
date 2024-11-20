from fastapi import APIRouter, Depends, HTTPException, Body
from auth.jwt_bearer import JWTBearer
from models import ProductSchema, ProductUpdateSchema
from database import db
from typing import List

router = APIRouter()

@router.post("/products", response_model=ProductSchema, dependencies=[Depends(JWTBearer())])
async def create_product(product: ProductSchema = Body(...)):
    product_data = product.dict(exclude_unset=True)
    return db.create_product(product_data)

@router.get("/products", response_model=List[ProductSchema], dependencies=[Depends(JWTBearer())])
async def get_all_products():
    return db.get_all_products()

@router.get("/products/{product_id}", response_model=ProductSchema, dependencies=[Depends(JWTBearer())])
async def get_product(product_id: str):
    product = db.get_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    return product

@router.put("/products/{product_id}", response_model=ProductSchema, dependencies=[Depends(JWTBearer())])
async def update_product(product_id: str, product_update: ProductUpdateSchema = Body(...)):
    update_data = product_update.dict(exclude_unset=True)
    updated_product = db.update_product(product_id, update_data)
    if not updated_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    return updated_product

@router.delete("/products/{product_id}", dependencies=[Depends(JWTBearer())])
async def delete_product(product_id: str):
    if not db.delete_product(product_id):
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    return {"message": "Product deleted successfully"}