from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRoute
from sqlalchemy import Column, Boolean, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import settings
from sqlalchemy.dialects.postgresql import UUID
import uuid
import re
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator

############################################
#BLOCK FOR COMMON INTERACTION WITH DATABASE#
############################################

engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True)

##################################################
#create session for the interaction with database#
##################################################

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

#######################
# BLOCK WITH DATABASE #
#######################

Base = declarative_base()

class User(base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surfase = Column(String,nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################

class UserDAL:
    """Data Access Layer for operating user info"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

        async def creae_user(
                self, name:str, surname:str, email:str
        ) -> User:
            new_user = User (
                name=name,
                surname=surname,
                email=email,
            )
            self.db_session.add(new_user)
            await self.db_session.flush()
            return new_user 

########################        
# BLOG WITH API MODELS #
########################

LETTER_MATCH_PATTERN =re.compile(r"^[а-яА-Яа-zA-Z\-]+$")

class TunedModel(BaseModel):
    class Config:
        """talls pydantic to convert to even non dict obj to json"""
        orm_mode = True

class UserCreate(BaseModel):
    name = str
    surname = str
    email = EmailStr

    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )