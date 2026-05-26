from pydantic import BaseModel


class ReviewCreate(BaseModel):

    rating: int

    comment: str
class ReviewResponse(BaseModel):

    rating: int

    comment: str

    class Config:
        orm_mode = True

        