from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, get_db
from models import Base
from routers import pages, components, deployment, auth, subscription
from subscription_manager import setup_subscription_manager
import uvicorn

Base.metadata.create_all(bind=engine)

# Inicializar el sistema de gestión de suscripciones
try:
    db = next(get_db())
    setup_subscription_manager(db)
    print("✅ Sistema de gestión de suscripciones inicializado")
except Exception as e:
    print(f"❌ Error inicializando sistema de gestión de suscripciones: {e}")
    # No detener el servidor, solo logear el error

app = FastAPI(title="Landing Builder API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(pages.router)
app.include_router(components.router)
app.include_router(deployment.router)
app.include_router(subscription.router)

@app.get("/")
async def root():
    return {"message": "Landing Builder API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)