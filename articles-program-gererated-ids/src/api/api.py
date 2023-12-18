"""API endpoints group."""

from fastapi import APIRouter

from . import endpoints


api_router = APIRouter()

api_router.include_router(endpoints.articles.router, prefix="/articles", tags=["articles"])
