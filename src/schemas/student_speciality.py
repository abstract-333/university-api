import uuid
from pydantic import BaseModel, Field, PositiveInt


class StudentSpecialityInDB(BaseModel):
    user_id: uuid.UUID = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"], description="uuid7"
    )
    university_id: PositiveInt = Field(
        examples=["4444"],
        description="""Your university id number that are written in student card, note that you can only have one 
        record in faculty""",
    )
    class_id: PositiveInt = Field(
        examples=[1, 2, 3, 4, 5, 6], description="Enter your class", le=6
    )
    name: str
    faculty_name: str
