from pydantic import BaseModel, Field, NonNegativeInt


class Pagination(BaseModel):
    limit: int = Field(
        default=10, le=30, ge=10, description="Could be any number between 10 and 20"
    )
    offset: NonNegativeInt = Field(default=0, description="could be any positive value")
