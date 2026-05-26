from pydantic import BaseModel


class OfferApply(BaseModel):

    coupon_code: str

