"""API endpoints related to articles."""

import dependency_injector.wiring
import fastapi
from fastapi.responses import JSONResponse

from ... import domain
from ... import views
from ...containers.message_bus import MessageBusContainer
from ...services.message_bus import MessageBus

router = fastapi.APIRouter()


@router.post("", status_code=201, response_model=dict)
@dependency_injector.wiring.inject
async def create_article(
    article: domain.schemata.ArticleCreate,
    bus: MessageBus = fastapi.Depends(
        dependency_injector.wiring.Provide[MessageBusContainer.message_bus]
    ),
) -> JSONResponse:
    try:
        cmd = domain.commands.CreateArticle(article.title,
                                            article.preview,
                                            article.body,
                                            article.created_by)
        await bus.handle(cmd)
    except Exception as ex:
        return JSONResponse(
            content=f"Failed to create article. {ex}",
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        )
    else:
        return JSONResponse(content="Article has been created.",
                            status_code=fastapi.status.HTTP_201_CREATED)


@router.get("/{article_id}", status_code=200, response_model=domain.schemata.Article)
@dependency_injector.wiring.inject
async def fetch_article_by_id(
    article_id: int,
    bus: MessageBus = fastapi.Depends(
        dependency_injector.wiring.Provide[MessageBusContainer.message_bus]
    ),
) -> domain.model.Article | JSONResponse:
    if result := await views.articles.fetch_article_by_id(article_id, bus.uow):
        return result
    return JSONResponse(
        content=f"Article with {article_id=} has not been found.",
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
    )


@router.get("", status_code=200, response_model=list[domain.schemata.Article])
@dependency_injector.wiring.inject
async def fetch_all_articles(
    bus: MessageBus = fastapi.Depends(
        dependency_injector.wiring.Provide[MessageBusContainer.message_bus]
    ),
) -> list[domain.model.Article] | JSONResponse:
    if result := await views.articles.fetch_all_articles(bus.uow):
        return result
    return JSONResponse(content="There are no articles at all.",
                        status_code=fastapi.status.HTTP_404_NOT_FOUND)
