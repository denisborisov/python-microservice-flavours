"""API endpoints related to articles."""

import uuid

import dependency_injector.wiring
import fastapi
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ... import domain, views
from ...containers.message_bus import MessageBusContainer
from ...domain import exceptions
from ...services.message_bus import MessageBus


router = fastapi.APIRouter()


@router.post("", status_code=201, response_model=dict)
@dependency_injector.wiring.inject
async def create_article(
    article: domain.schemata.ArticlePost,
    bus: MessageBus = fastapi.Depends(
        dependency_injector.wiring.Provide[MessageBusContainer.message_bus],
    ),
) -> JSONResponse:
    try:
        cmd = domain.commands.CreateArticle(
            article.title,
            article.preview,
            article.body,
            article.created_by,
        )
    except exceptions.ArticleCreationError as ex:
        raise fastapi.HTTPException(
            detail="Failed to create article.",
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        ) from ex
    result = await bus.handle(cmd)
    return JSONResponse(
        content={"article_id": jsonable_encoder(result)},
        status_code=fastapi.status.HTTP_201_CREATED,
    )


@router.get("/{article_id}", status_code=200, response_model=domain.schemata.Article)
@dependency_injector.wiring.inject
async def fetch_article_by_id(
    article_id: uuid.UUID,
    bus: MessageBus = fastapi.Depends(
        dependency_injector.wiring.Provide[MessageBusContainer.message_bus],
    ),
) -> JSONResponse:
    if result := await views.articles.fetch_article_by_id(article_id, bus.uow):
        return JSONResponse(content=jsonable_encoder(result))
    return JSONResponse(
        content=f"Article with {article_id=} has not been found.",
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
    )


@router.get("", status_code=200, response_model=list[domain.schemata.Article])
@dependency_injector.wiring.inject
async def fetch_all_articles(
    created_by: int | None = None,
    bus: MessageBus = fastapi.Depends(
        dependency_injector.wiring.Provide[MessageBusContainer.message_bus],
    ),
) -> JSONResponse:
    if result := await views.articles.fetch_all_articles(bus.uow, created_by):
        return JSONResponse(content=jsonable_encoder(result))
    return JSONResponse(
        content="There are no articles at all.",
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
    )


@router.patch("/{article_id}", status_code=200, response_model=None)
@dependency_injector.wiring.inject
async def update_article(
    article_id: uuid.UUID,
    article: domain.schemata.ArticlePatch,
    bus: MessageBus = fastapi.Depends(
        dependency_injector.wiring.Provide[MessageBusContainer.message_bus],
    ),
) -> None:
    try:
        cmd = domain.commands.UpdateArticle(
            article_id,
            article.title,
            article.preview,
            article.body,
        )
    except exceptions.ArticleModificationError as ex:
        raise fastapi.HTTPException(
            detail="Failed to update article.",
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        ) from ex

    try:
        await bus.handle(cmd)
    except exceptions.ArticleModificationError as ex:
        raise fastapi.HTTPException(
            detail=str(ex),
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        ) from ex


@router.delete("/{article_id}", status_code=204, response_model=None)
@dependency_injector.wiring.inject
async def delete_article(
    article_id: uuid.UUID,
    bus: MessageBus = fastapi.Depends(
        dependency_injector.wiring.Provide[MessageBusContainer.message_bus],
    ),
) -> None:
    try:
        cmd = domain.commands.DeleteArticle(article_id)
        await bus.handle(cmd)
    except exceptions.ArticleDeletionError as ex:
        raise fastapi.HTTPException(
            detail=str(ex),
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        ) from ex
