from fastapi import FastAPI
import uvicorn
from public import router as public_router
from secure import router as secure_router

app = FastAPI()

app.include_router(public_router, tags=["public"])
app.include_router(secure_router, tags=["secure"])

@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to the API"}