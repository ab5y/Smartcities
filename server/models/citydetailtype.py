from sqlalchemy import (
	Column,
	Integer,
	Text,
)
from sqlalchemy.orm import relationship
from .meta import Base


class CityDetailType(Base):
	__tablename__ = 'city_detail_types'
	id = Column(Integer, primary_key=True)
	name = Column(Text)

	city_details = relationship('CityDetail', order_by='CityDetail.id', back_populates='detail_types')