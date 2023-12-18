"""Liveness, readindess and startup probes."""

import fastapi
from fastapi.responses import JSONResponse


probes_router = fastapi.APIRouter()


@probes_router.get("/startup", status_code=200, tags=["probes"], include_in_schema=False)
def check_startup() -> JSONResponse:
    return JSONResponse(content="OK", status_code=fastapi.status.HTTP_200_OK)


@probes_router.get("/liveness", status_code=200, tags=["probes"], include_in_schema=False)
def check_liveness() -> JSONResponse:
    return JSONResponse(content="OK", status_code=fastapi.status.HTTP_200_OK)


@probes_router.get("/readiness", status_code=200, tags=["probes"], include_in_schema=False)
def check_readiness() -> JSONResponse:
    """Check if application is ready and connected to db.

    Select shoud be here.
    """
    return JSONResponse(content="OK", status_code=fastapi.status.HTTP_200_OK)
