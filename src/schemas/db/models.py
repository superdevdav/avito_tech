from config import *

import uuid

from sqlalchemy import CheckConstraint
from sqlalchemy import Enum, Column, String, Integer, Text, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from enum import Enum as PyEnum

Base = declarative_base()

class EmployeeORM(Base):
      __tablename__ = 'employee'

      id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
      username = Column(String(50), unique=True, nullable=False)
      first_name = Column(String(50))
      last_name = Column(String(50))
      
      created_at = Column(TIMESTAMP, server_default=func.now())
      updated_at = Column(TIMESTAMP, onupdate=func.now(), server_default=func.now())

organization_types = Enum(
     'IE',
     'LLC',
     'JSC', 
     name="organization_type")

class OrganizationORM(Base):
      __tablename__ = 'organization'
      
      id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
      name = Column(String(100), nullable=False)
      description = Column(Text)
      type = Column(organization_types)
      
      created_at = Column(TIMESTAMP, server_default=func.now())
      updated_at = Column(TIMESTAMP, onupdate=func.now(), server_default=func.now())

class OrganizationResponsibleORM(Base):
      __tablename__ = 'organization_responsible'

      id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
      
      organization_id = Column(UUID(as_uuid=True), ForeignKey('organization.id'))
      organization = relationship('OrganizationORM', backref='responsibles')
      
      user_id = Column(UUID(as_uuid=True), ForeignKey('employee.id'))
      employee = relationship('EmployeeORM', backref='responsibilities')

class StatusTenderEnum(PyEnum):
    CREATED = 'Created'
    PUBLISHED = 'Published'
    CLOSED = 'Closed'

class ServiceTypeEnum(PyEnum):
    CONSTRUCTION = 'Construction'
    DELIVERY = 'Delivery'
    MANUFACTURE = 'Manufacture'

class TenderORM(Base):
     __tablename__ = 'tenders'

     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
     name = Column(String(100), unique=True)
     description = Column(String(500))
     serviceType = Column(Enum(ServiceTypeEnum), nullable=False)
     status = Column(Enum(StatusTenderEnum), nullable=False)
     version = Column(Integer, default=1)
     
     organizationId = Column(UUID(as_uuid=True), ForeignKey('organization.id'))
     organization = relationship('OrganizationORM', backref='tenders')

     creatorUsername = Column(String, ForeignKey('employee.username'))
     employee = relationship('EmployeeORM', backref='tenders')

     created_at = Column(TIMESTAMP, server_default=func.now())
     updated_at = Column(TIMESTAMP, onupdate=func.now(), server_default=func.now())

     __table_args__ = (
          CheckConstraint('version >= 1', name='version_value_check'),
     )

class StatusBidEnum(PyEnum):
    CREATED = 'Created'
    PUBLISHED = 'Published'
    CANCELED = 'Canceled'

class BidDecisionEnum(PyEnum):
    APPROVED = 'Approved'
    REJECTED = 'Rejected'

class BidAuthorTypeEnum(PyEnum):
     ORGANIZATION = 'Organization'
     USER = 'User'

class BidORM(Base):
     __tablename__ = 'bids'

     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
     name = Column(String(100), unique=True)
     description = Column(String(500))
     status = Column(Enum(StatusBidEnum))
     authorType = Column(Enum(BidAuthorTypeEnum))
     authorId = Column(UUID(as_uuid=True), default=uuid.uuid4)
     version = Column(Integer, default=1)
     decision = Column(String(50), nullable=True)

     tenderId = Column(UUID(as_uuid=True), ForeignKey('tenders.id'))

     created_at = Column(TIMESTAMP, server_default=func.now())
     updated_at = Column(TIMESTAMP, onupdate=func.now(), server_default=func.now())

     __table_args__ = (
          CheckConstraint('version >= 1', name='version_value_check'),
     )

class BidReviewsORM(Base):
     __tablename__ = 'bids_reviews'
     
     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
     userName = Column(String(100), unique=True)
     description = Column(Text)
     
     bidId = Column(UUID(as_uuid=True), ForeignKey('bids.id'))

     created_at = Column(TIMESTAMP, server_default=func.now())
     updated_at = Column(TIMESTAMP, onupdate=func.now(), server_default=func.now())