from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.admin_model import Admin
from app.auth.auth_utils import verify_password, create_access_token

def login_admin(db: Session, username: str, password: str):
    admin = db.query(Admin).filter(Admin.username == username).first()
    if not admin or not verify_password(password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    token = create_access_token({"sub": username, "rol": "admin"})
    return token
