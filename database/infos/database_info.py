from pydantic import BaseModel, Field


class DatabaseInfo(BaseModel):
    host: str
    port: int
    user: str = Field(default="")
    password: str = Field(default="")
    db: str = Field(default="")
