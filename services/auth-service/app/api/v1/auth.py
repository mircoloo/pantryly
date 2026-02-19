from fastapi import APIRouter, Depends, HTTPException


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/login")
def login():
    return {"data": "login"}


@router.post("/signup")
def login():
    return {"data": "signed up"}