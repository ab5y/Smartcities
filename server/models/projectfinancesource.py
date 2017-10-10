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


class ProjectFinanceSource(Base):
	__tablename__ = 'projectfinancesources'
	id = Column(Integer, primary_key=True)
	source_id = Column(Integer, ForeignKey('financesources.id'), nullable=False)
	amount = Column(Numeric)
	details = Column(Text)

	source = relationship('FinanceSource', order_by='FinanceSource.id', back_populates='projectfinancesources')
	project = relationship('Project', order_by='Project.id', back_populates='projectfinancesources')