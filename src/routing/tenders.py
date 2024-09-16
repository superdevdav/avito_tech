from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import JSONResponse
from typing import List, Optional, Literal

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repositories.Tender import TenderRepository
from schemas.tenderModels.TenderRequestModel import TenderRequestModel
from schemas.tenderModels.TenderCreateModel import TenderCreateModel

tenders_router = APIRouter()

@tenders_router.post('/tenders/new',
            responses={
            200: {
                  "description": "Тендер успешно создан. Сервер присваивает уникальный идентификатор и время создания.",
                  "content": {
                  "application/json": {
                        'example': [
                              {
                                    "id": "550e8400-e29b-41d4-a716-446655440000",
                                    "name": "Доставка товары Казань - Москва",
                                    "description": "Нужно доставить оборудовоние для олимпиады по робототехники",
                                    "status": "Created",
                                    "serviceType": "Delivery",
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
            }
      } 
)
async def createTender(
      request_body: TenderCreateModel
      ):
      
      try:
            params = {
                  "name": request_body.name,
                  "description": request_body.description,
                  "serviceType": request_body.serviceType,
                  "status": request_body.status,
                  "organizationId": request_body.organizationId,
                  "creatorUsername": request_body.creatorUsername
            }
            
            creator_id = await TenderRepository.user_exists(request_body.creatorUsername)
            if creator_id:
                  raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User does not exist or invalid')

            id = await TenderRepository.create_tender(params)
            if id:
                  return JSONResponse(content={'id': str(id),
                                            'name': params['name'], 
                                            'description': params['description'], 
                                            'serviceType': params['serviceType'],
                                            'status': params['status'],
                                            'organizationId': params['organizationId'],
                                            'creatorUsername': params['creatorUsername']
                                            }, status_code=status.HTTP_200_OK)
      except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
      except PermissionError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
      except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@tenders_router.get('/tenders',
            responses={
            200: {
                  "description": "Список тендеров, отсортированных по алфавиту по названию.",
                  "content": {
                  "application/json": {
                        'example': [
                              {
                                    "id": "550e8400-e29b-41d4-a716-446655440000",
                                    "name": "Доставка товары Казань - Москва",
                                    "description": "Нужно доставить оборудовоние для олимпиады по робототехники",
                                    "status": "Created",
                                    "serviceType": "Delivery",
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
async def getTenders(
      service_type: Optional[List[Literal['Construction', 'Delivery', 'Manufacture']]] = Query(None),
      limit: Optional[int] = Query(5, max_length=50, alias="limit"),
      offset: Optional[int] = Query(0, alias="offset"),
      ):
      try:
            tenders = await TenderRepository.get_all_tenders(limit=limit, offset=offset, service_type=service_type)
            tenders = sorted(tenders, key=lambda t: t.name)
            
            if tenders:
                  return tenders
            else:
                  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Tenders not found')
      except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
      except PermissionError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
      except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@tenders_router.get('/tenders/my',
            responses={
            200: {
                  "description": "Список тендеров пользователя, отсортированный по алфавиту.",
                  "content": {
                  "application/json": {
                        'example': [
                              {
                                    "id": "550e8400-e29b-41d4-a716-446655440000",
                                    "name": "Доставка товары Казань - Москва",
                                    "description": "Нужно доставить оборудовоние для олимпиады по робототехники",
                                    "status": "Created",
                                    "serviceType": "Delivery",
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
async def getUserTenders(
      username: Optional[str] = None,
      limit: Optional[int] = Query(5, max_length=50, alias="limit"),
      offset: Optional[int] = Query(0, alias="offset")
      ):
      try:
            user_id = await TenderRepository.user_exists(username)
            if not user_id:
                  raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User does not exist or invalid')

            tenders = await TenderRepository.get_user_tenders(username, limit=limit, offset=offset)
            tenders = sorted(tenders, key=lambda t: t.name)
            
            if tenders:
                  return tenders
            else:
                  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Tenders not found')
      except HTTPException as e:
            raise e
      except PermissionError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
      except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
      except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@tenders_router.patch('/tenders/{tenderId}/edit',
            responses={
            200: {
                  "description": "ендер успешно изменен и возвращает обновленную информацию.",
                  "content": {
                  "application/json": {
                        'example': {
                              "id": "550e8400-e29b-41d4-a716-446655440000",
                              "name": "Доставка товары Казань - Москва",
                              "description": "Нужно доставить оборудовоние для олимпиады по робототехники",
                              "status": "Created",
                              "serviceType": "Delivery",
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
async def editTender(
      tenderId: str,
      username: str,
      request_body: TenderRequestModel
      ):
      try:
            user_id = await TenderRepository.user_exists(username)
            if not user_id:
                  raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User does not exist or invalid')

            params = {'name': request_body.name, 'description': request_body.description, 'serviceType': request_body.serviceType}
            data = await TenderRepository.edit_tender(tenderId, params)
            if data:
                  return JSONResponse(content={'id': str(data.id),
                                               'name': data.name,
                                               'description': data.description,
                                               'serviceType': data.serviceType,
                                               'status': data.status,
                                               'version': data.version,
                                               'organizationId': data.organizationId,
                                               'creatorUsername': data.creatorUsername,
                                               'created_at': str(data.created_at),
                                               'updated_at': str(data.updated_at)
                                               }, status_code=status.HTTP_200_OK)
            else:
                  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
      except HTTPException as e:
            raise e
      except PermissionError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
      except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
      except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@tenders_router.get('/tenders/{tenderId}/status',
            responses={
            200: {
                  "description": "Текущий статус тендера.",
                  "content": {
                  "application/json": {
                        "example": "Created"
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
async def getTenderStatus(
      tenderId: str,
      username: Optional[str] = None
      ):
      try:
            user_id = await TenderRepository.user_exists(username)
            if not user_id:
                  raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User does not exist or invalid')

            tender_status = await TenderRepository.get_tender_status(tenderId)
            if tender_status:
                  return JSONResponse(content=tender_status, status_code=status.HTTP_200_OK)
            else:
                  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Tender not found')
      except HTTPException as e:
            raise e
      except PermissionError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
      except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
      except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
