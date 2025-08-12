from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from app.db.db_session import get_db
from app.auth.auth_utils import verify_token
from app.models.post_model import Post

post_router = APIRouter(tags=["Publicaciones"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Obtener la única publicación pública
@post_router.get("/publico")
def leer_post_publico(db: Session = Depends(get_db)):
    post = db.query(Post).first()
    return {"content": post.content if post else "No hay publicaciones aún."}

# Publicar / actualizar texto (solo admin)
@post_router.post("/publicar")
def publicar_texto(content: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    if payload.get("rol") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")

    post = db.query(Post).first()
    if post:
        post.content = content
    else:
        post = Post(content=content)
        db.add(post)
    db.commit()
    db.refresh(post)
    return {"msg": "Publicación guardada", "content": post.content}
