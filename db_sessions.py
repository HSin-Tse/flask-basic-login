from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from settings import DB_URI, DB_ROLES_URI, DB_ROLES_URI_AJ

session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=create_engine(DB_URI)))

# session_roles = scoped_session(sessionmaker(autocommit=False,
#                                             autoflush=False,
#                                             bind=create_engine(DB_ROLES_URI)))

session_roles_aj = scoped_session(sessionmaker(autocommit=False,
                                               autoflush=False,
                                               bind=create_engine(DB_ROLES_URI_AJ)))
