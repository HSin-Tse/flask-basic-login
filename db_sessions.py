from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from settings import DB_ROLES_URI_AJ

session_roles_aj = scoped_session(sessionmaker(autocommit=False,
                                               autoflush=False,
                                               bind=create_engine(DB_ROLES_URI_AJ)))
