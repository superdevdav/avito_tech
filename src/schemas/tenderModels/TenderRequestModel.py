from pydantic import BaseModel
from typing import Literal

class TenderRequestModel(BaseModel):
    name: str
    description: str
    serviceType: Literal['Construction', 'Delivery', 'Manufacture']