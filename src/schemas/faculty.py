from pydantic import BaseModel, Field, PositiveInt, ConfigDict


class Faculty(BaseModel):
    name: str = Field(description="It is unique")
    max_class: PositiveInt = Field(le=6)
