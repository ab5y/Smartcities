from sqlalchemy import (
	Column,
	ForeignKey,
	Index,
	Integer,
	Text,
)
from sqlalchemy.orm import relationship
from .meta import Base


class ProjectSubCategory(Base):
	__tablename__ = 'projectsubcategories'
	id = Column(Integer, primary_key=True)
	name = Column(Text)
	category_id = Column(Integer, ForeignKey('projectcategories.id'), nullable=False)

	category = relationship('ProjectCategory', order_by='ProjectCategory.id', back_populates='subcategories')
	projects = relationship('Project', order_by='Project.id', back_populates='subcategory')