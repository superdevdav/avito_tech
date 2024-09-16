from typing import List, Dict, Any

from schemas.db.config_db import new_session
from schemas.db.models import TenderORM
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

class TenderRepository:
      @staticmethod
      async def create_tender(data: Dict[str, Any]):
            try:
                  async with new_session() as session:
                        tender = TenderORM(
                              name=data['name'],
                              description=data['description'],
                              serviceType=data['serviceType'],
                              status='Created',
                              version=1,
                              organizationId=str(data['organizationId']),
                              creatorUsername=data['creatorUsername']
                        )

                        session.add(tender)
                        await session.commit()

                        return tender.id
            except SQLAlchemyError as e:
                  raise ValueError(f"Database error: {str(e)}")
            except KeyError as e:
                  raise ValueError(f"Missing field: {str(e)}")
            except Exception as e:
                  raise ValueError(f"Unexpected error: {str(e)}")
      
      @staticmethod
      async def get_all_tenders(limit, offset, service_type) -> List[TenderORM]:
            try:
                  async with new_session() as session:
                        base_query = 'SELECT * FROM tenders '
                        
                        params = {
                              'limit': limit,
                              'offset': offset
                        }

                        service_type_sql = None
                        if service_type and isinstance(service_type, list):
                              service_type_sql = '('
                              for i in range(len(service_type)):
                                    if i != len(service_type) - 1:
                                          service_type_sql += f"'{str(service_type[i])}', "
                                    else:
                                          service_type_sql += f"'{str(service_type[i])}')"
                              base_query += f'WHERE "serviceType" IN {service_type_sql} '

                        base_query += 'ORDER BY name LIMIT :limit OFFSET :offset;'
                        
                        query = text(base_query)

                        result = await session.execute(query, params)
                        
                        tenders_list = [TenderORM(
                              id = i[0],
                              name = i[1],
                              description = i[2],
                              serviceType = i[3],
                              status = i[4],
                              organizationId = str(i[6]),
                              creatorUsername = i[7],
                              created_at = i[8],
                              updated_at = i[9]
                        ) for i in result.fetchall()]

                        return tenders_list
            except SQLAlchemyError as e:
                  raise ValueError(f"Database error: {str(e)}")
            except Exception as e:
                  raise ValueError(f"Unexpected error: {str(e)}")

      @staticmethod
      async def get_tender_status(id: str):
            try:
                  async with new_session() as session:
                        query = text('SELECT status FROM tenders WHERE id = :id;')

                        result = await session.execute(query, {'id': id})
                        status = result.scalar()

                        return status
            except SQLAlchemyError as e:
                  raise ValueError(f"Database error: {str(e)}")
            except KeyError as e:
                  raise ValueError(f"Missing field: {str(e)}")
            except Exception as e:
                  raise ValueError(f"Unexpected error: {str(e)}")

      @staticmethod
      async def get_user_tenders(username, limit, offset) -> List[TenderORM]:
            try:
                  async with new_session() as session:
                        query = text('SELECT * FROM tenders JOIN employee ON employee.username = tenders."creatorUsername" WHERE employee.username = :username ORDER BY name LIMIT :limit OFFSET :offset;')
                        
                        result = await session.execute(query, {'username': username, 'limit': limit, 'offset': offset})
                        
                        tenders_list = [TenderORM(
                              id = i[0],
                              name = i[1],
                              description = i[2],
                              serviceType = i[3],
                              status = i[4],
                              organizationId = str(i[6]),
                              creatorUsername = i[7],
                              created_at = i[8],
                              updated_at = i[9]
                        ) for i in result.fetchall()]
                        
                        return tenders_list
            except SQLAlchemyError as e:
                  raise ValueError(f"Database error: {str(e)}")
            except Exception as e:
                  raise ValueError(f"Unexpected error: {str(e)}")
      
      @staticmethod
      async def edit_tender(tenderId: str, data: Dict[str, Any]):
            try:
                  async with new_session() as session:
                        query = text('UPDATE tenders SET name = :name, description = :description, "serviceType" = :serviceType, version = version + 1, updated_at = CURRENT_TIMESTAMP WHERE id = :id;')
                        
                        await session.execute(query, {'id': tenderId, 'name': data['name'], 'description': data['description'], 'serviceType': data['serviceType']})
                        await session.commit()
                        print('ok')
                        query = text('SELECT * FROM tenders WHERE id = :id;')
                        result = await session.execute(query, {'id': tenderId})
                        
                        tenders_list = [TenderORM(
                              id = tenderId,
                              name = i[1],
                              description = i[2],
                              serviceType = i[3],
                              status = i[4],
                              version = i[5],
                              organizationId = str(i[6]),
                              creatorUsername = i[7],
                              created_at = i[8],
                              updated_at = i[9]
                        ) for i in result.fetchall()]

                        return tenders_list[0]
            except SQLAlchemyError as e:
                  raise ValueError(f"Database error: {str(e)}")
            except KeyError as e:
                  raise ValueError(f"Missing field: {str(e)}")
            except Exception as e:
                  raise ValueError(f"Unexpected error: {str(e)}")
      
      @staticmethod
      async def user_exists(username: str):
            try:
                  async with new_session() as session:

                        check_query = text('SELECT id FROM employee WHERE username = :username;')
                        result = await session.execute(check_query, {'username': username})
                        user_id = result.scalar()

                        return user_id

            except Exception as e:
                  raise ValueError(f"Unexpected error: {str(e)}")