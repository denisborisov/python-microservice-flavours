"""App entrypoint."""

import fastapi

from . import api, routines
from .containers.wiring import attach_containers_to_app


app = fastapi.FastAPI(
    title="Articles Microservice",
    summary="Provides with ability to manipulate articles.",
    description=(
        "Articles Microservice is one of the **core** microservices.\n"
        "It provides with ability to perform CRUD operations."
    ),
    version="0.1.0",
    contact={
        "name": "Denis Borisov",
        "email": "denis.borisov@hotmail.com",
        "url": "https://www.linkedin.com/in/borisovdenis/",
    },
    docs_url="/api/docs",
    redoc_url="/api/redoc",
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
