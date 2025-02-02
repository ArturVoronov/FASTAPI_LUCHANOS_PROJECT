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