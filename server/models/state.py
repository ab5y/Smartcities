from sqlalchemy import (
	Column,
	Index,
	Integer,
	Text)
from sqlalchemy.orm import relationship
from .meta import Base



class State(Base):
	__tablename__ = 'states'
	id = Column(Integer, primary_key=True)
	name = Column(Text)

	cities = relationship('City', order_by='City.id', back_populates='state')

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}