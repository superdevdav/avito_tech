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
                              authorType=data['AuthorType'],
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
                        query = text('SELECT * FROM bids JOIN employee ON employee.username = bids."creatorUsername" WHERE employee.username = :username ORDER BY name LIMIT :limit OFFSET :offset;')
                        result = await session.execute(query, {'username': username, 'limit': limit, 'offset': offset})
                        bids_list = [BidORM(
                              id = i[0],
                              name = i[1],
                              description = i[2],
                              status = i[4],
                              tenderId = i[5],
                              organizationId = i[5],
                              creatorUsername = i[6],
                              created_at = i[7],
                              updated_at = i[8]
                        ) for i in result.fetchall()]
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
                        bids_list = [BidORM(
                              id = i[0],
                              name = i[1],
                              description = i[2],
                              status = i[4],
                              tenderId = i[5],
                              organizationId = i[5],
                              creatorUsername = i[6],
                              created_at = i[7],
                              updated_at = i[8]
                        ) for i in result.fetchall()]
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
                        bids_list = [BidORM(
                              id = bidId,
                              name = i[1],
                              description = i[2],
                              status = i[3],
                              version = i[4],
                              tenderId = i[5],
                              organizationId = i[6],
                              creatorUsername = i[7],
                              created_at = i[8],
                              updated_at = i[9]
                        ) for i in result.fetchall()]

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
                        await session.commit()

                        return True
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
      async def submit_bid_feedback(id: str, username: str, feedback: str):
            try:
                  async with new_session() as session:
                        query = text('INSERT INTO bids_reviews (username, description, bidId) VALUES (:username, :description, :id);')

                        result = await session.execute(query, {'id': id, 'username': username, 'description': feedback})

                        return result.scalar()
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

                        check_query = text('SELECT id FROM bids WHERE "creatorUsername" = :username;')
                        result = await session.execute(check_query, {'username': username})
                        bid_id = result.scalar()

                        if bid_id is None:
                              return 401

            except Exception as e:
                  raise ValueError(f"Unexpected error: {str(e)}")