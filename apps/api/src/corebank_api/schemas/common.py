from decimal import Decimal
from enum import StrEnum
from typing import Annotated

from pydantic import Field, PlainSerializer

Money = Annotated[
    Decimal,
    Field(max_digits=18, decimal_places=2),
    PlainSerializer(lambda value: float(value), return_type=float, when_used="json"),
]


class Currency(StrEnum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"
