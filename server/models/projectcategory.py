from sqlalchemy import (
	Column,
	Index,
	Integer,
	Text,
)
from sqlalchemy.orm import relationship
from .meta import Base


class ProjectCategory(Base):
	__tablename__ = 'projectcategories'
	id = Column(Integer, primary_key=True)
	name = Column(Text)

	subcategories = relationship('ProjectSubCategory', order_by='ProjectSubCategory.id', back_populates='category')
	projects = relationship('Project', order_by='Project.id', back_populates='category')

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}