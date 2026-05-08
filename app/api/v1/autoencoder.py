from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies.auth import require_admin
from app.schemas.autoencoder import AutoencoderResponse
from app.schemas.network_event import NetworkEventRequest

from ml.inference.network.autoencoder_model import (
    CICIDSAutoencoderModel,
)

from ml.inference.network.feature_builder import (
    NetworkFeatureBuilder,
)

router = APIRouter(
    prefix="/autoencoder",
    tags=["autoencoder"],
)

model = CICIDSAutoencoderModel()

builder = NetworkFeatureBuilder()

@router.post(
    "/check",
    response_model=AutoencoderResponse,
)
def check_autoencoder(
    payload: NetworkEventRequest,
    _=Depends(require_admin),
):
    
    try:
        features = builder.build(payload)

        return model.predict(features)
    
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )