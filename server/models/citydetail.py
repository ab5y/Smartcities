from sqlalchemy import (
	Column,
	ForeignKey,
	Integer,
	Text,
)
from sqlalchemy.orm import relationship
from .meta import Base


class CityDetail(Base):
	__tablename__ = 'city_details'
	id = Column(Integer, primary_key=True)
	detail_type_id = Column(Integer, ForeignKey('city_detail_types.id'), nullable=True)

	detail_types = relationship('CityDetailType', order_by='CityDetailType.id', back_populates='city_details')
	