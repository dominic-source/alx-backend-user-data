#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import Mapping, Union
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """add user to database"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs: Mapping[str, Union[int, str]]) -> User:
        """returns the first row foun in the users table"""
        for key in kwargs.keys():
            if key not in ['id', 'email', 'hashed_password',
                           'session_id', 'reset_token']:
                raise InvalidRequestError
        data = self._session.query(User).filter_by(**kwargs).first()
        if not data:
            raise NoResultFound
        return data

    def update_user(self, user_id: int,
                    **kwargs: Mapping[str, Union[int, str]]) -> None:
        """update users info"""
        id_d = {"id": user_id}
        user = self.find_user_by(id_d)
        for key, value in kwargs.items():
            if key not in ['id', 'email', 'hashed_password',
                           'session_id', 'reset_token']:
                raise ValueError
            setattr(user, key, value)
        self._session.commit()
        return None
