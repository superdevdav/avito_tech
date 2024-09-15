from pydantic import BaseModel

class BidEditModel(BaseModel):
      name: str
      description: str