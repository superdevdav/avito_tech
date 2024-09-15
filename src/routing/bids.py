from fastapi import APIRouter, HTTPException, Request, status, Query
from fastapi.responses import JSONResponse

from typing import Optional, Literal

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repositories.Bid import BidRepository
from schemas.bidModels.BidCreateModel import BidCreateModel
from schemas.bidModels.BidEditModel import BidEditModel

bids_router = APIRouter()

@bids_router.post('/bids/new',
            responses={
            200: {
                  "description": "Предложение успешно создано. Сервер присваивает уникальный идентификатор и время создания.",
                  "content": {
                  "application/json": {
                        'example': {
                              "id": "550e8400-e29b-41d4-a716-446655440000",
                              "name": "Доставка товаров Алексей",
                              "status": "Created",
                              "authorType": "User",
                              "authorId": "61a485f0-e29b-41d4-a716-446655440000",
                              "version": 1,
                              "createdAt": "2006-01-02T15:04:05Z07:00"
                              }
                        }
                  },
            400: {
                  'description': 'Решение не может быть отправлено.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            },
            401: {
                  'description': 'Пользователь не существует или некорректен.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            },
            403: {
                  'description': 'Недостаточно прав для выполнения действия.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            },
            404: {
                  'description': 'Предложение не найдено.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            }
      }
      }                   
)
async def createBid(
      request_body: BidCreateModel
      ):
      try:
            params = {
                  'name': request_body.name,
                  'description': request_body.description,
                  'tenderId': request_body.tenderId,
                  'authorType': request_body.authorType,
                  'authorId': request_body.authorId
            }

            bid = await BidRepository.create_bid(params)
            if bid:
                  return {
                        "id": str(bid.id),
                        "name": bid.name,
                        "status": bid.status,
                        "authorType": bid.authorType,
                        "authorId": str(bid.authorId),
                        "version": bid.version,
                        "created_at": bid.created_at
                  }
            else:
                  raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create bid")
      except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
      except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
      
@bids_router.get('/bids/my',
            responses={
            200: {
                  "description": "Список предложений пользователя, отсортированный по алфавиту.",
                  "content": {
                  "application/json": {
                        'example': [
                              {
                                    "id": "550e8400-e29b-41d4-a716-446655440000",
                                    "name": "Доставка товаров Алексей",
                                    "status": "Created",
                                    "authorType": "User",
                                    "authorId": "61a485f0-e29b-41d4-a716-446655440000",
                                    "version": 1,
                                    "createdAt": "2006-01-02T15:04:05Z07:00"
                              }
                              ]
                        }
                  }
            },
            400: {
                  'description': 'Решение не может быть отправлено.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            },
            401: {
                  'description': 'Пользователь не существует или некорректен.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            },
            403: {
                  'description': 'Недостаточно прав для выполнения действия.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            },
            404: {
                  'description': 'Предложение не найдено.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            }
      } 
)
async def getUserBids(
      limit: Optional[int] = Query(5, alias="paginationLimit"),
      offset: Optional[int] = Query(0, alias="paginationOffset"),
      username: Optional[str] = None,
      ):
      try:
            if limit < 0 or offset < 0:
                  raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect limit or offset')
            
            bids = await BidRepository.get_user_bids(username, limit=limit, offset=offset)
            bids = sorted(bids, key=lambda b: b.name)
            return bids
      except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@bids_router.get('/bids/{tenderId}/list',
            responses={
            200: {
                  "description": "Список предложений, отсортированный по алфавиту.",
                  "content": {
                  "application/json": {
                        'example': [
                              {
                                    "id": "550e8400-e29b-41d4-a716-446655440000",
                                    "name": "Доставка товаров Алексей",
                                    "status": "Created",
                                    "authorType": "User",
                                    "authorId": "61a485f0-e29b-41d4-a716-446655440000",
                                    "version": 1,
                                    "createdAt": "2006-01-02T15:04:05Z07:00"
                              }
                              ]
                        }
                  }
            },
            400: {
                  'description': 'Решение не может быть отправлено.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            },
            401: {
                  'description': 'Пользователь не существует или некорректен.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            },
            403: {
                  'description': 'Недостаточно прав для выполнения действия.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            },
            404: {
                  'description': 'Предложение не найдено.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            }
      }  
)
async def getBidsForTender(
      tenderId: str,
      username: str,
      limit: Optional[int] = Query(5, alias="paginationLimit"),
      offset: Optional[int] = Query(0, alias="paginationOffset"),
      ):
      try:
            result = await BidRepository.user_exists(username)
            if result == 401:
                  raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User with this username does not exist')

            bids = await BidRepository.get_bids_for_tender(tenderId, limit, offset)
            
            if bids:
                  bids = sorted(bids, key=lambda b: b.name)
                  return bids
            else:
                  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Tender or bids not found')
      except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
      except PermissionError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
      except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@bids_router.get('/bids/{bidId}/status',
            responses={
            200: {
                  "description": "Текущий статус предложения.",
                  "content": {
                  "application/json": {
                        'example': 'Created'
                        }
                  }
            },
            400: {
                  'description': 'Решение не может быть отправлено.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            },
            401: {
                  'description': 'Пользователь не существует или некорректен.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            },
            403: {
                  'description': 'Недостаточно прав для выполнения действия.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            },
            404: {
                  'description': 'Предложение не найдено.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            }
      }
)
async def getBidStatus(
      bidId: str,
      username: str
      ):
      try:
            result = await BidRepository.user_exists(username)
            if result == 401:
                  raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User with this username does not exist')

            bid_status = await BidRepository.get_bid_status(bidId)
            return JSONResponse(content=bid_status, status_code=status.HTTP_200_OK)
      except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
      except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@bids_router.patch('/bids/{bidId}/edit',
            responses={
            200: {
                  "description": "Предложение успешно изменено и возвращает обновленную информацию.",
                  "content": {
                  "application/json": {
                        'example': {
                                    "id": "550e8400-e29b-41d4-a716-446655440000",
                                    "name": "Доставка товаров Алексей",
                                    "status": "Created",
                                    "authorType": "User",
                                    "authorId": "61a485f0-e29b-41d4-a716-446655440000",
                                    "version": 1,
                                    "createdAt": "2006-01-02T15:04:05Z07:00"
                              }
                        }
                  }
            },
            400: {
                  'description': 'Решение не может быть отправлено.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            },
            401: {
                  'description': 'Пользователь не существует или некорректен.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            },
            403: {
                  'description': 'Недостаточно прав для выполнения действия.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            },
            404: {
                  'description': 'Предложение не найдено.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            }
      }
)
async def editBid(
      bidId: str,
      username: str,
      request_body: BidEditModel
      ):
      try:
            result = await BidRepository.user_exists(username)
            if result == 401:
                  raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User with this username does not exist')
            
            params = {
                  'name': request_body.name,
                  'description': request_body.description
            }

            edited_bid = await BidRepository.edit_bid(bidId, params)
            return edited_bid
      except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@bids_router.put('/bids/{bidId}/submit_decision',
      responses={
            200: {
                  "description": "Решение по предложению успешно отправлено.",
                  "content": {
                  "application/json": {
                        'example': {
                                    "id": "550e8400-e29b-41d4-a716-446655440000",
                                    "name": "Доставка товаров Алексей",
                                    "status": "Created",
                                    "authorType": "User",
                                    "authorId": "61a485f0-e29b-41d4-a716-446655440000",
                                    "version": 1,
                                    "createdAt": "2006-01-02T15:04:05Z07:00"
                              }
                        }
                  }
            },
            400: {
                  'description': 'Решение не может быть отправлено.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            },
            401: {
                  'description': 'Пользователь не существует или некорректен.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            },
            403: {
                  'description': 'Недостаточно прав для выполнения действия.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            },
            404: {
                  'description': 'Предложение не найдено.',
                  "content": {
                  "application/json": {
                        'example': {
                                    "reason": "<объяснение, почему запрос пользователя не может быть обработан>"
                              }
                        }
                  }
            }
      }
)
async def submitBidDecision(
      bidId: str,
      bidDecision: Literal['Approved', 'Rejected'],
      username: str
      ):
      try:
            result = await BidRepository.user_exists(username)
            if result == 401:
                  raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User with this username does not exist')

            result = await BidRepository.submit_decision(bidId, bidDecision)
            if result:
                  return JSONResponse(content='Decision submitted', status_code=status.HTTP_200_OK)
      except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
      except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@bids_router.put('/bids/{bidId}/feedback')
async def submitBidFeedback(
      bidId: str,
      bidFeedback: str,
      username: str
      ):
      try:
            result = await BidRepository.user_exists(username)
            if result == 401:
                  raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User with this username does not exist')

            result = await BidRepository.submit_bid_feedback(bidId, username, bidFeedback)
            if result:
                  return JSONResponse(content='Feedback submitted', status_code=status.HTTP_200_OK)
      except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))