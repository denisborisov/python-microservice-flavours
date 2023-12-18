"""Create flashcards table.

Revision ID: fd0b55b207fb
Revises:
Create Date: 2023-11-28 13:14:29.733520
"""
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.ext.asyncio import AsyncAttrs

from alembic import op


# revision identifiers, used by Alembic.
revision = "fd0b55b207fb"
down_revision = None
branch_labels = None
depends_on = None


class Base(AsyncAttrs, sqlalchemy.orm.DeclarativeBase):
    pass


class Flashcard(Base):
    __tablename__ = "flashcards"

    word: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(primary_key=True)
    details: sqlalchemy.orm.Mapped[dict[str, list[str]]] = sqlalchemy.orm.mapped_column(
        type_=sqlalchemy.JSON
    )


def upgrade() -> None:
    database_engine = op.get_bind()
    Base.metadata.create_all(database_engine)

    session: sqlalchemy.orm.Session = sqlalchemy.orm.Session(bind=database_engine)

    session.execute(
        sqlalchemy.insert(Flashcard),
        [
            {
                "word": "challenge",
                "details": {
                    "definitions": [
                        "a call to take part in a contest or competition, especially a duel.",
                        "an objection or query as to the truth of something, often with "
                        "an implicit demand for proof.",
                    ],
                    "synonyms": ["dare", "provocation", "confrontation with", "dispute with"],
                    "translations": ["испытание", "вызов"],
                    "examples": ["recently vaccinated calves should be protected from challenge"],
                },
            },
            {
                "word": "cuckoo",
                "details": {
                    "definitions": [
                        "a medium-sized long-tailed bird, typically with a gray or brown back and barred or pale "
                        "underparts. Many cuckoos lay their eggs in the nests of small songbirds.",
                        "a mad person.",
                    ],
                    "synonyms": [],
                    "translations": ["кукушка", "разиня"],
                    "examples": ["people think you're cuckoo"],
                },
            },
            {
                "word": "cup",
                "details": {
                    "definitions": [
                        "a small bowl-shaped container for drinking from, typically having a handle.",
                        "an ornamental trophy in the form of a cup, usually made of gold or silver and having a stem "
                        "and two handles, awarded as a prize in a contest.",
                    ],
                    "synonyms": ["trophy", "chalice"],
                    "translations": ["чашка", "кубок"],
                    "examples": [
                        "the ball bounced out of the cup",
                        "the bars offered large glasses of white wine cup",
                    ],
                },
            },
            {
                "word": "cucumber",
                "details": {
                    "definitions": [
                        "a long, green-skinned fruit with watery flesh, usually eaten raw in salads or pickled.",
                        "the climbing plant of the gourd family that yields cucumbers, native to the Chinese Himalayan "
                        "region. It is widely cultivated but very rare in the wild.",
                    ],
                    "synonyms": [],
                    "translations": ["огурец"],
                    "examples": [],
                },
            },
            {
                "word": "fork",
                "details": {
                    "definitions": [
                        "an implement with two or more prongs used for lifting food to the mouth or holding it when cutting.",
                        "the point where something, especially a road or river, divides into two parts.",
                    ],
                    "synonyms": ["branch", "split"],
                    "translations": ["вилка", "вилы"],
                    "examples": ["fork in some compost", "turn right at the next fork"],
                },
            },
            {
                "word": "hat",
                "details": {
                    "definitions": [
                        "a shaped covering for the head worn for warmth, as a fashion item, or as part of a uniform."
                    ],
                    "synonyms": ["titfer"],
                    "translations": ["шляпа", "шапка"],
                    "examples": ["a black straw hat"],
                },
            },
            {
                "word": "hatch",
                "details": {
                    "definitions": [
                        "an opening of restricted size allowing for passage from one area to another.",
                        "a newly hatched brood.",
                    ],
                    "synonyms": [],
                    "translations": ["люк", "штриховка"],
                    "examples": ["a hatch of mayflies", "a service hatch"],
                },
            },
            {
                "word": "knife",
                "details": {
                    "definitions": [
                        "an instrument composed of a blade fixed into a handle, used for cutting or as a weapon.",
                        "stab (someone) with a knife.",
                    ],
                    "synonyms": ["cutting tool", "blade"],
                    "translations": ["нож", "скальпель"],
                    "examples": [],
                },
            },
            {
                "word": "knight",
                "details": {
                    "definitions": [
                        "(in the Middle Ages) a man who served his sovereign or lord as a mounted soldier in armor.",
                        "(in the UK) a man awarded a nonhereditary title by the sovereign in recognition of merit or "
                        "service and entitled to use the honorific “Sir” in front of his name.",
                    ],
                    "synonyms": ["chevalier", "cavalier"],
                    "translations": ["рыцарь", "конь"],
                    "examples": ["in all your quarrels I will be your knight"],
                },
            },
            {
                "word": "night",
                "details": {
                    "definitions": [
                        "the period of darkness in each twenty-four hours; the time from sunset to sunrise.",
                        "the period of time between afternoon and bedtime; an evening.",
                    ],
                    "synonyms": ["darkness", "dark"],
                    "translations": ["ночь", "вечер"],
                    "examples": [
                        "a line of watchfires stretched away into the night",
                        "a two-bedroom cabin costs $90 per night",
                    ],
                },
            },
            {
                "word": "ping",
                "details": {
                    "definitions": [
                        "a short, high-pitched ringing sound.",
                        "make or cause to make a short, high-pitched ringing sound.",
                    ],
                    "synonyms": [],
                    "translations": ["свистеть", "гудеть"],
                    "examples": ["the ping of the oven timer"],
                },
            },
            {
                "word": "pinky",
                "details": {
                    "definitions": [
                        "partly pink or with a pink tinge.",
                        "variant spelling of pinkie (sense 1).",
                    ],
                    "synonyms": [],
                    "translations": ["мизинец", "розоватый"],
                    "examples": [],
                },
            },
            {
                "word": "spoon",
                "details": {
                    "definitions": [
                        "an implement consisting of a small, shallow oval or round bowl on a long handle, used for "
                        "eating, stirring, and serving food.",
                        "a thing resembling a spoon in shape.",
                    ],
                    "synonyms": [],
                    "translations": ["ложка", "блесна"],
                    "examples": [],
                },
            },
            {
                "word": "table",
                "details": {
                    "definitions": [
                        "a piece of furniture with a flat top and one or more legs, providing a level surface on which "
                        "objects may be placed, and that can be used for such purposes as eating, writing, working, or "
                        "playing games.",
                        "a set of facts or figures systematically displayed, especially in columns.",
                    ],
                    "synonyms": ["bench", "board"],
                    "translations": ["стол", "таблица"],
                    "examples": [
                        "a table of contents",
                        "they made the hand easily with the aid of a club ruff on the table",
                    ],
                },
            },
            {
                "word": "taste",
                "details": {
                    "definitions": [
                        "the sensation of flavor perceived in the mouth and throat on contact with a substance.",
                        "a person's liking for particular flavors.",
                    ],
                    "synonyms": ["flavor", "savor"],
                    "translations": ["вкус", "пристрастие"],
                    "examples": [
                        "the waiter poured some wine for him to taste",
                        "the wine had a fruity taste",
                    ],
                },
            },
        ],
    )


def downgrade() -> None:
    database_engine = op.get_bind()
    Base.metadata.drop_all(database_engine)
