from sqlalchemy import (
	Column,
	ForeignKey,
	Index,
	Integer,
	Text,
)
from sqlalchemy.orm import relationship
from .meta import Base


class City(Base):
	__tablename__ = 'cities'
	id = Column(Integer, primary_key=True)
	name = Column(Text)
	state_id = Column(Integer, ForeignKey('states.id'), nullable=False)

	state = relationship('State', order_by='State.id', back_populates='cities')
	projects = relationship('Project', order_by='Project.id', back_populates='city')

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}