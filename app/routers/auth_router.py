from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.db_session import get_db
from app.auth.auth_service import login_admin

auth_router = APIRouter(tags=["Autenticación"])

@auth_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    token = login_admin(db, form_data.username, form_data.password)
    return {"access_token": token, "token_type": "bearer"}
