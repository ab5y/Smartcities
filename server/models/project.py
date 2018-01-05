from sqlalchemy import (
	Boolean,
	Column,
	ForeignKey,
	Index,
	Integer,
	Numeric,
	Text,
)
from sqlalchemy.orm import relationship
from .meta import Base


class Project(Base):
	__tablename__ = 'project'
	id = Column(Integer, primary_key=True)
	name = Column(Text)
	rank = Column(Integer)
	round = Column(Text)
	city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
	category_id = Column(Integer, ForeignKey('projectcategories.id'), nullable=False)
	subcategory_id = Column(Integer, ForeignKey('projectsubcategories.id'), nullable=False)
	potential_displacements = Column(Boolean)
	IT_ITES = Column(Boolean)
	comment = Column(Text)
	amount_total = Column(Numeric)


	city = relationship('City', order_by='City.id', back_populates='projects')
	category = relationship('ProjectCategory', order_by='ProjectCategory.id', back_populates='projects')
	subcategory = relationship('ProjectSubCategory', order_by='ProjectSubCategory.id', back_populates='projects')
