from pydantic import BaseModel

class TenderCreateModel(BaseModel):
      name: str
      description: str
      serviceType: str
      status: str
      organizationId: str
      creatorUsername: str