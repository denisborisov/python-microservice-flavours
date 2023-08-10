"""App entrypoint."""

import fastapi

from . import api
from . import routines
from .containers.wiring import attach_containers_to_app


app = fastapi.FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    title="Articles Microservice",
    description="This is an article microservice.",
    version="0.1.0",
    contact={
        "name": "Denis Borisov",
        "email": "denis.borisov@hotmail.com",
    },
)

attach_containers_to_app(app)

app.include_router(api.api.api_router, prefix="/api")
app.include_router(api.probes.probes_router, prefix="/api/status")


@app.on_event("startup")
def on_startup() -> None:
    routines.mappers.start_mappers()
    routines.message_bus.start_process_events_in_bus()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await routines.message_bus.stop_process_events_in_bus()
    routines.mappers.stop_mappers()
    await routines.database_engine.dispose_database_engine()
