from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.events import router as events_router
from app.api.v1.anomaly import router as anomaly_router
from app.api.v1.alerts import router as alerts_router
from app.api.v1.fraud import router as fraud_router
from app.api.v1.intrusion import router as intrusion_router
from app.api.v1.autoencoder import router as autoencoder_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(events_router)
app.include_router(anomaly_router)
app.include_router(alerts_router)
app.include_router(fraud_router)
app.include_router(intrusion_router)
app.include_router(autoencoder_router)


@app.get("/")
def root():
    return {"message": f"{settings.app_name} is running"}


@app.get("/health")
def health():
    return {"status": "ok"}

