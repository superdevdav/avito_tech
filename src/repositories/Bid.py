import uuid

from typing import List, Dict, Any

from schemas.db.config_db import new_session
from schemas.db.models import BidORM
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text      

class BidRepository:
      @staticmethod
      async def create_bid(data: Dict[str, Any]):
            try:
                  async with new_session() as session:
                        bid = BidORM(
                              name=data['name'],
                              description=data['description'],
                              status='Created',
                              tenderId=data['tenderId'],
                              authorType=data['authorType'],
                              authorId=data['authorId']
                        )

                        session.add(bid)
                        await session.commit()
                        await session.refresh(bid)

                        return {
                              "id": str(bid.id),
                              "name": bid.name,
                              "status": bid.status,
                              "authorType": bid.authorType,
                              "authorId": str(bid.authorId),
                              "version": bid.version,
                              "created_at": bid.created_at
                        }
            except SQLAlchemyError as e:
                  raise ValueError(f"Database error: {str(e)}")
            except KeyError as e:
                  raise ValueError(f"Missing field: {str(e)}")
            except Exception as e:
                  raise ValueError(f"Unexpected error: {str(e)}")
      
      @staticmethod
      async def get_user_bids(username, limit, offset) -> List[BidORM]:
            try:
                  async with new_session() as session:

                        base_query = 'SELECT * FROM bids WHERE bids."authorId" = '
                        base_query += '(SELECT id FROM employee WHERE employee.username = ' f"'{username}') "
                        base_query += 'ORDER BY bids.name LIMIT :limit OFFSET :offset;'

                        query = text(base_query)

                        result = await session.execute(query, {'limit': limit, 'offset': offset})
                        bids_list = [{
                                    'id': i[0],
                                    'name': i[1],
                                    'status': i[3],
                                    'authorType': i[4],
                                    'authorId': i[5],
                                    'version': i[6],
                                    'created_at': i[9]
                              } for i in result.fetchall()]
                        return bids_list
            except SQLAlchemyError as e:
                  raise ValueError(f"Database error: {str(e)}")
            except Exception as e:
                  raise ValueError(f"Unexpected error: {str(e)}")
      
      @staticmethod
      async def get_bids_for_tender(id, limit, offset):
            try:
                  async with new_session() as session:
                        query = text('SELECT * FROM bids JOIN tenders ON tenders.id = bids."tenderId" WHERE tenders.id = :id ORDER BY bids.name LIMIT :limit OFFSET :offset;')
                        result = await session.execute(query, {'id': id, 'limit': limit, 'offset': offset})
                        bids_list = [{
                              'id': i[0],
                              'name': i[1],
                              'status': i[3],
                              'authorType': i[4],
                              'authorId': i[5],
                              'version': i[6],
                              'created_at': i[9]
                        } for i in result.fetchall()]
                        return bids_list
            except SQLAlchemyError as e:
                  raise ValueError(f"Database error: {str(e)}")
            except Exception as e:
                  raise ValueError(f"Unexpected error: {str(e)}")

      @staticmethod
      async def edit_bid(bidId: int, data: Dict[str, Any]):
            try:
                  async with new_session() as session:
                        query = text('UPDATE bids SET name = :name, description = :description, version = version + 1, updated_at = CURRENT_TIMESTAMP WHERE id = :id;')
                        await session.execute(query, {'id': bidId, 'name': data['name'], 'description': data['description']})
                        await session.commit()
                        
                        query = text('SELECT * FROM bids WHERE id = :id;')
                        result = await session.execute(query, {'id': bidId})
                        bids_list = [{
                              'id': i[0],
                              'name': i[1],
                              'status': i[3],
                              'authorType': i[4],
                              'authorId': i[5],
                              'version': i[6],
                              'created_at': i[9]
                        } for i in result.fetchall()]

                        return bids_list[0]
            except SQLAlchemyError as e:
                  raise ValueError(f"Database error: {str(e)}")
            except KeyError as e:
                  raise ValueError(f"Missing field: {str(e)}")
            except Exception as e:
                  raise ValueError(f"Unexpected error: {str(e)}")
      
      @staticmethod
      async def submit_decision(id: str, decision: str):
            try:
                  async with new_session() as session:
                        query = text('UPDATE bids SET decision = :decision WHERE id = :id;')

                        await session.execute(query, {'decision': decision, 'id': id})
                        
                        query = text('SELECT * FROM bids WHERE id = :id;')
                        result = await session.execute(query, {'id': id})

                        return result.fetchall()[0]
            except SQLAlchemyError as e:
                  raise ValueError(f"Database error: {str(e)}")
            except KeyError as e:
                  raise ValueError(f"Missing field: {str(e)}")
            except Exception as e:
                  raise ValueError(f"Unexpected error: {str(e)}")
      
      @staticmethod
      async def get_bid_status(id: str):
            try:
                  async with new_session() as session:
                        query = text('SELECT status FROM bids WHERE id = :id;')

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
      async def submit_bid_feedback(bidId: str, username: str, feedback: str):
            try:
                  async with new_session() as session:
                        insert_query = text('INSERT INTO bids_reviews (id, "userName", description, "bidId") VALUES (:reviewId, :username, :description, :bidId);')

                        await session.execute(insert_query, {'reviewId': uuid.uuid4(), 'bidId': bidId, 'username': username, 'description': feedback})
                        await session.commit()
                        
                        select_query = text('SELECT * FROM bids WHERE id = :id;')
                        result = await session.execute(select_query, {'id': bidId})

                        return result.fetchall()[0]
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

      @staticmethod
      async def user_exists_by_id(id: str):
            try:
                  async with new_session() as session:

                        check_query = text('SELECT username FROM employee WHERE id = :id;')
                        result = await session.execute(check_query, {'id': id})
                        username = result.scalar()

                        return username

            except Exception as e:
                  raise ValueError(f"Unexpected error: {str(e)}")    