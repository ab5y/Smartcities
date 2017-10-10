from sqlalchemy import (
	Column,
	Index,
	Integer,
	Text,
)
from .meta import Base


class Party(Base):
	__tablename__ = 'parties'
	id = Column(Integer, primary_key=True)
	name = Column(Text)
	