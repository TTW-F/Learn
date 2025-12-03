from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

# 性别枚举（和数据库对应）
class GenderEnum(str, Enum):
    male = "男"
    female = "女"
    other = "其他"

# 添加学生的请求模型
class StudentCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="登录用户名（学生学号）")
    password: str = Field(..., min_length=6, max_length=20, description="登录密码")
    student_name: str = Field(..., min_length=1, max_length=50, description="学生姓名")
    gender: GenderEnum = Field(..., description="性别")
    age: int = Field(..., ge=6, le=50, description="年龄（6-50岁）")
    phone: Optional[str] = Field(None, pattern=r"^1[3-9]\d{9}$", description="手机号（可选，必须是11位正确格式）")
    email: Optional[EmailStr] = Field(None, description="邮箱（可选，格式要正确，比如xxx@qq.com）")
    clazz_id: int = Field(..., description="所属班级ID（必须存在）")

# 更新学生的请求模型
class StudentUpdate(BaseModel):
    student_name: Optional[str] = Field(None, min_length=1, max_length=50, description="学生姓名（可选）")
    gender: Optional[GenderEnum] = None
    age: Optional[int] = Field(None, ge=6, le=50, description="年龄（可选）")
    phone: Optional[str] = Field(None, pattern=r"^1[3-9]\d{9}$", description="手机号（可选）")
    email: Optional[EmailStr] = Field(None, description="邮箱（可选）")
    clazz_id: Optional[int] = Field(None, description="所属班级ID（可选）")

# 学生响应模型
class StudentBase(BaseModel):
    id: int
    student_name: str
    gender: GenderEnum
    age: int
    phone: Optional[str]
    email: Optional[EmailStr]
    clazz_id: int
    clazz_name: Optional[str] = Field(None, description="班级名称")
    username: str = Field(..., description="登录用户名")
    create_time: datetime

    class Config:
        from_attributes = True

# 分页响应模型
class StudentPagination(BaseModel):
    items: list[StudentBase] = Field(..., description="当前页的学生列表")
    total: int = Field(..., description="学生总人数")
    page: int = Field(..., description="当前页码")
    size: int = Field(..., description="每页显示多少人")
    pages: int = Field(..., description="总页数")