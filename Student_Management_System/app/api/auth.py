from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from jwt  import PyJWTError
import jwt
from sqlalchemy.ext.asyncio import AsyncSession



from Student_Management_System.app.config import settings
from Student_Management_System.app.database import get_db
from Student_Management_System.app.models import User
from Student_Management_System.app.schemas.user import TokenData, Token

# 创建路由对象
router = APIRouter(
    prefix="/api/auth",
    tags=["认证管理"]
)

# 工具函数：生成JWT Token（登录成功后调用）
def create_access_token(data: dict):
    to_encode = data.copy()
    # 设置Token过期时间（当前时间+配置里的有效期）
    expire = datetime.now() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # 加密生成Token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm="HS256"
    )
    return encoded_jwt

# 登录接口
@router.post("/login", response_model=Token, summary="用户登录")
async def login(
    db: AsyncSession = Depends(get_db),  # 依赖：获取数据库会话
    form_data: OAuth2PasswordRequestForm = Depends()  # 接收用户名密码（支持表单提交，测试方便）
):
    """
    登录接口：
    - 输入：username（用户名）、password（密码）
    - 输出：access_token（令牌）、token_type（bearer）
    - 支持管理员、教师、学生登录
    """
    # 1. 从数据库查询用户名对应的用户
    user = await db.scalar(db.query(User).filter(User.username == form_data.username))
    # 2. 验证用户是否存在，密码是否正确
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 3. 生成Token（存用户ID和角色）
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role}
    )
    # 4. 返回Token
    return {"access_token": access_token, "token_type": "bearer"}

# 注销接口（实际JWT是无状态的，客户端删除Token即可）
@router.post("/logout", summary="用户注销")
async def logout():
    """注销接口：客户端直接删除Token即可，服务器无需额外处理"""
    return {"code": 200, "msg": "注销成功"}