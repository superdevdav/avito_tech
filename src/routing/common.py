from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import PlainTextResponse

common_router = APIRouter()

@common_router.get('/ping')
def checkServer():
      try:
            return PlainTextResponse(content='ok', status_code=status.HTTP_200_OK)
      except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))