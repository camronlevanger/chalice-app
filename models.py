# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Table, Boolean, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from dataclasses import dataclass
from base import Session, engine, Base

class UserTeams(Base):
    __tablename__ = 'user_teams'
    id=Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('users.id'))
    user_id = Column(Integer, ForeignKey('teams.id'))
    position = Column(String(50))
    active = Column(Boolean, default=True)
    teams = relationship("Team", backref="teams")
    users = relationship("User", backref="users")
    __table_args__ = (Index('idxteamposuser', team_id, user_id, position , unique=True ,), )
    

@dataclass
class Team(Base):
    __tablename__ = 'teams'
    id=Column(Integer, primary_key=True)
    name=Column('name', String(32))
    users = relationship(
        "UserTeams",
        back_populates="teams")


class User(Base):
    __tablename__ = 'users'
    id=Column(Integer, primary_key=True)
    email=Column('email', String(120), unique=True)
    teams = relationship(
        "UserTeams",
        back_populates="users")
