from pydantic import BaseModel

class BidCreateModel(BaseModel):
      name: str
      description: str
      tenderId: str
      authorType: str
      authorId: str