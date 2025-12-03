from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine, Base
from app.api import auth_router, students_router


# 生命周期管理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - 服务器启动时执行
    print(" 学生管理系统启动中...")

    # 创建数据库表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("数据库表创建完成")

    yield  # 这里服务器正常运行

    # Shutdown - 服务器关闭时执行
    print("学生管理系统关闭中...")
    await engine.dispose()
    print("数据库连接已关闭")


# 创建FastAPI应用实例（相当于启动Web服务器）
app = FastAPI(
    title="学生管理系统API",  # 接口文档标题
    description="小白友好版：FastAPI + SQLAlchemy 学生管理系统",  # 文档描述
    version="1.0.0",  # 版本号
    lifespan=lifespan  # 添加生命周期管理
)

# 注册接口路由（把我们写的接口添加到服务器）
app.include_router(auth_router)  # 认证接口（登录/注销）
app.include_router(students_router)  # 学生管理接口（增删改查）


# 根路由（测试服务器是否启动成功）
@app.get("/", summary="健康检查")
async def root():
    return {"message": "学生管理系统启动成功！访问 /docs 查看接口文档"}


# 运行服务器（直接运行这个文件时执行）
if __name__ == "__main__":
    import uvicorn

    # 启动服务器：host=0.0.0.0表示允许其他电脑访问，port=8000是端口号
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)