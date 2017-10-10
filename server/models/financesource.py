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


class FinanceSource(Base):
	__tablename__ = 'financesources'
	id = Column(Integer, primary_key=True)
	name = Column(Text)