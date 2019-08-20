from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
# from DiscordBotTest import pass_discord_id

BASE = declarative_base()
SQL_LITE_DB_NAME = 'Dischord' + '.db'
SQL_LITE_ENGINE_URL = 'sqlite:///' + SQL_LITE_DB_NAME


def get_engine():
    """Returns SQL engine depending on OS"""
    engine_url = SQL_LITE_ENGINE_URL
    engine = create_engine(engine_url)
    return engine


def get_session():
    engine = get_engine()
    BASE.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()


class User(BASE):
    __tablename__ = "user"
    id = Column('id', Integer, primary_key=True)
    discord_id = Column('discord_id', String, unique=True)
    user_balance = Column('user_balance', Integer)


def find_discord_id_balance(discord_id_in):
    # active_discord_user = pass_discord_id()
    session = get_session()
    users = session.query(User).all()
    for i in users:
        if i.discord_id == discord_id_in:
            return i.user_balance
            break


def find_user_exists(discord_id_in):
    session = get_session()
    users = session.query(User).all()
    for i in users:
        if i.discord_id == discord_id_in:
            print("true")
            return True
            break


    session.close()
    # active_discord_user = "Matt#2929"


def adduser(discord_id_in):
    session = get_session()
    discorduser = User()
    discorduser.discord_id = discord_id_in
    discorduser.user_balance = 100
    session.add(discorduser)
    session.commit()
    session.close()
