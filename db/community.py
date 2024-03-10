from datetime import datetime

from sqlalchemy import Column, BigInteger, String, DateTime

from base import BaseModel


class Community(BaseModel):
    __tablename__ = 'communities'

    id = Column(autoincrement=True)
    tg_id = Column(BigInteger, nullable=False)
    name = Column(String, nullable=False)
    desc = Column(String, nullable=False)
    owner_id = Column(BigInteger, nullable=False)
    limit = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())

