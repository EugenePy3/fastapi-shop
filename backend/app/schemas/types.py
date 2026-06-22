from decimal import Decimal
from typing import Annotated
from pydantic import Field

PriceType = Annotated[
    Decimal,
    Field(
        gt=0,
        max_digits=10,
        decimal_places=2,
        examples=[999.99],
    )
]
