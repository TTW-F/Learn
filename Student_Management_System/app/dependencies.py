from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt  import PyJWTError
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List


from Student_Management_System.app.config import settings
from Student_Management_System.app.database import get_db
from Student_Management_System.app.models import User
from Student_Management_System.app.schemas.user import TokenData

# 从请求头获取Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# 依赖1：验证Token，获取当前登录的用户
async def get_current_user(
    db: AsyncSession = Depends(get_db),  # 获取数据库会话
    token: str = Depends(oauth2_scheme)  # 从请求头获取Token
) -> User:
    # Token无效时返回
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="登录失效或未登录，请重新登录",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 解码Token，获取用户信息
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=["HS256"],  # 加密算法（和生成Token时一致）
            options={"verify_exp": True}  # 验证Token是否过期
        )
        # 从Token里提取用户ID和角色
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None or role is None:
            raise credentials_exception
        token_data = TokenData(user_id=int(user_id), role=role)
    except PyJWTError:
        raise credentials_exception

    # 用户是否存在
    user = await db.get(User, token_data.user_id)
    if user is None:
        raise credentials_exception
    # 检查用户是否被禁用
    if user.status != 1:
        raise HTTPException(status_code=403, detail="账号已被禁用")
    return user

# 3. 依赖2：角色权限控制（比如只允许管理员访问）
def role_required(allowed_roles: List[str]):
    # 内部函数，接收当前登录用户
    def decorator(current_user: User = Depends(get_current_user)):
        # 检查用户角色是否在允许的列表里
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"权限不足！仅允许{allowed_roles}角色访问"
            )
        return current_user
    return decorator