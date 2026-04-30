from fastapi import APIRouter, HTTPException

from ml.inference.network.cicids_model import CICIDSModel

router = APIRouter(prefix="/intrusion", tags=["intrusion"])

model = CICIDSModel()

@router.post("/check")
def check_intrusion(features: list[float]):
    try:
        return model.predict(features)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))