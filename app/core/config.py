"""
File with environment variables and general configuration logic.
`SECRET_KEY`, `ENVIRONMENT` etc. map to env variables with the same names.
"""

from typing import Union, List
from environs import Env
from pydantic import BaseModel

class ProjectSettings(BaseModel):
    NAME: str
    VERSION: str
    DESCRIPTION: str

class APISettings(BaseModel):
    CORS_ALLOWED_ORIGINS: List[str]
    ALLOWED_HOSTS: List[str]    
    GEMINI_API_TOKEN: str

class Config(BaseModel):
    project: ProjectSettings
    backend: APISettings

def load_config() -> Config:
    "Load configuration from dotenv file."
    
    env = Env()
    env.read_env()
    
    return Config(
        project=ProjectSettings(
            NAME=env.str("PROJECT_NAME"),
            VERSION=env.str("PROJECT_VERSION"),
            DESCRIPTION=env.str("PROJECT_DESCRIPTION")
        ),
        backend=APISettings(
            CORS_ALLOWED_ORIGINS=env.list("BACKEND_CORS_ORIGINS"),
            ALLOWED_HOSTS=env.list("ALLOWED_HOSTS"),
            GEMINI_API_TOKEN=env.str("GEMINI_API")
        ),
    )

config = load_config()