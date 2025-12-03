from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional

# 角色枚举
class RoleEnum(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

# 登录请求模型
class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="登录用户名")
    password: str = Field(..., min_length=6, max_length=20, description="登录密码（6-20位）")

# Token响应模型
class Token(BaseModel):
    access_token: str = Field(..., description="登录成功后的令牌，后续接口要用")
    token_type: str = Field("bearer", description="令牌类型，固定为bearer")

# Token信息
class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[RoleEnum] = None

# 用户信息响应模型
class UserBase(BaseModel):
    id: int
    username: str
    role: RoleEnum
    create_time: datetime


    class Config:
        from_attributes = True