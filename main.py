from fastapi import FastAPI
from app.db.db_session import engine, Base, SessionLocal
from app.models.admin_model import Admin
from app.auth.auth_utils import hash_password
from app.routers.auth_router import auth_router
from app.routers.post_router import post_router

# Crear tablas
Base.metadata.create_all(bind=engine)

# Crear admin por defecto si no existe
def crear_admin_por_defecto():
    db = SessionLocal()
    admin = db.query(Admin).filter(Admin.username == "admin").first()
    if not admin:
        nuevo_admin = Admin(
            username="admin",
            hashed_password=hash_password("admin123")
        )
        db.add(nuevo_admin)
        db.commit()
    db.close()

crear_admin_por_defecto()

app = FastAPI(title="App Simple con Login Admin")

app.include_router(auth_router, prefix="/auth")
app.include_router(post_router, prefix="/post")

@app.get("/")
def root():
    return {"msg": "Bienvenido a la app pública. Visita /post/publico para ver el texto publicado."}
