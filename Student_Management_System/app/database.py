from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

#创建数据库引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # 开发时可以改成True，会打印执行的SQL语句（方便调试）
    pool_pre_ping=True  # 自动检查连接是否有效
)

#创建会话工厂
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    # 创建一个会话
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()  #提交数据
        except Exception as e:
            await session.rollback()  #回滚数据
            raise e  # 抛出错误
        finally:
            await session.close()  # 关闭会话