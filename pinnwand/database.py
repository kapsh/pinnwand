import datetime
import logging
import os
import base64
import contextlib

import pygments.lexers
import pygments.formatters

from sqlalchemy import Integer, Column, String, DateTime, Text, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from pinnwand.settings import DATABASE_URI


log = logging.getLogger(__name__)

_engine = create_engine(DATABASE_URI)
_session = sessionmaker(bind=_engine)


@contextlib.contextmanager
def session() -> Session:
    a_session = _session()

    try:
        yield a_session
    except:
        a_session.rollback()
        raise
    finally:
        a_session.close()


class _Base(object):
    """Base class which provides automated table names
    and a primary key column."""

    @declared_attr
    def __tablename__(cls) -> str:  # pylint: disable=no-self-argument
        return str(cls.__class__.__name__.lower())

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=_Base)


class Paste(Base):  # type: ignore
    """The Paste model represents a single Paste."""

    pub_date = Column(DateTime)
    chg_date = Column(DateTime)

    paste_id = Column(String(250), unique=True)
    removal_id = Column(String(250), unique=True)

    lexer = Column(String(250))

    raw = Column(Text)
    fmt = Column(Text)
    src = Column(String(250))

    exp_date = Column(DateTime)

    def create_hash(self) -> str:
        # This should organically grow as more is used, probably depending
        # on how often collissions occur.
        # Aside from that we should never repeat hashes which have been used before
        # without keeping the pastes in the database.
        # this does expose urandom directly ..., is that bad?
        return (
            base64.urlsafe_b64encode(os.urandom(3))
            .decode("ascii")
            .replace("=", "")
        )

    def __init__(
        self,
        raw: str,
        lexer: str = "text",
        expiry: datetime.timedelta = datetime.timedelta(days=7),
        src: str = "web",
    ) -> None:
        self.pub_date = datetime.datetime.utcnow()
        self.chg_date = datetime.datetime.utcnow()

        # Generate a paste_id and a removal_id
        # Unless someone proves me wrong that I need to check for collisions
        # my famous last words will be that the odds are astronomically small
        self.paste_id = self.create_hash()
        self.removal_id = self.create_hash()

        self.raw = raw

        self.src = src

        self.lexer = lexer

        lexer = pygments.lexers.get_lexer_by_name(lexer)
        formatter = pygments.formatters.HtmlFormatter(  # pylint: disable=no-member
            linenos=True, cssclass="source"
        )

        self.fmt = pygments.highlight(self.raw, lexer, formatter)

        # The expires date is the pub_date with the delta of the expiry
        if expiry:
            self.exp_date = self.pub_date + expiry
        else:
            self.exp_date = None

    def __repr__(self) -> str:
        return f"<Paste(paste_id={self.paste.id})>"
