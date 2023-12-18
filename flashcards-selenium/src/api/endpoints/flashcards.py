"""API endpoints related to flashcards."""

import dependency_injector.wiring
import fastapi
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ... import domain, views
from ...containers.message_bus import MessageBusContainer
from ...domain import exceptions
from ...services.message_bus import MessageBus

router = fastapi.APIRouter()


@router.get("/{word}", status_code=200, response_model=domain.schemata.Flashcard)
@dependency_injector.wiring.inject
async def fetch_flashcard_by_word(
    word: str,
    bus: MessageBus = fastapi.Depends(
        dependency_injector.wiring.Provide[MessageBusContainer.message_bus],
    ),
) -> JSONResponse:
    if result := await views.flashcards.fetch_flashcard_by_word(word, bus):
        return JSONResponse(content=jsonable_encoder(result, exclude={"details", "events"}))
    return JSONResponse(
        content=f"Flashcard for {word=} has not been found.",
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
    )


@router.get("", status_code=200, response_model=list[domain.schemata.Flashcard])
@dependency_injector.wiring.inject
async def fetch_all_flashcards(  # noqa: PLR0913
    regular_expression: str = ".",
    with_definitions: bool = False,
    with_synonyms: bool = False,
    with_translations: bool = False,
    with_examples: bool = False,
    last_retrieved_word: str = "",
    limit: int = 4,
    bus: MessageBus = fastapi.Depends(
        dependency_injector.wiring.Provide[MessageBusContainer.message_bus],
    ),
) -> JSONResponse:
    if result := await views.flashcards.fetch_all_flashcards(
        regular_expression,
        with_definitions,
        with_synonyms,
        with_translations,
        with_examples,
        last_retrieved_word,
        limit,
        bus.uow,
    ):
        return JSONResponse(content=jsonable_encoder(result, exclude={"events"}))
    return JSONResponse(
        content="There are no flashcards at all.",
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
    )


@router.delete("/{word}", status_code=204, response_model=None)
@dependency_injector.wiring.inject
async def delete_flashcard(
    word: str,
    bus: MessageBus = fastapi.Depends(
        dependency_injector.wiring.Provide[MessageBusContainer.message_bus],
    ),
) -> None:
    try:
        cmd = domain.commands.DeleteFlashcard(word)
        await bus.handle(cmd)
    except exceptions.FlashcardDeletionError as ex:
        raise fastapi.HTTPException(
            detail=str(ex),
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        ) from ex
