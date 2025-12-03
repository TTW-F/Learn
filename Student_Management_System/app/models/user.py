from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Enum, SmallInteger, DateTime
from sqlalchemy.orm import relationship
from Student_Management_System.app.database import Base
import bcrypt

class User(Base):
    __tablename__ = "user"  # 数据库表名
    id = Column(Integer, primary_key=True, comment="用户ID（自动增长）")
    username = Column(
        String(50),
        unique=True,  # 用户名不能重复
        nullable=False,  # 不能为空
        comment="登录用户名（管理员用admin，学生用学号）"
    )
    password = Column(
        String(100),
        nullable=False,
        comment="加密后的密码（不存明文，安全）"
    )
    role = Column(
        Enum("admin", "teacher", "student"),
        nullable=False,
        comment="角色：管理员/教师/学生"
    )
    status = Column(
        SmallInteger,
        default=1,  # 默认是1（正常）
        comment="状态：1-正常，0-禁用（禁用后不能登录）"
    )
    create_time = Column(
        DateTime,
        default=datetime.now(timezone.utc),  # 自动填充当前时间
        comment="创建时间"
    )
    update_time = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),  # 更新时自动刷新时间
        comment="更新时间"
    )

    # 关系映射（告诉程序：用户和学生、班级的关联）
    # 1个用户对应1个学生（学生专属）
    student = relationship("Student", back_populates="user", uselist=False, cascade="all, delete-orphan")
    # 1个教师（用户角色是teacher）对应多个班级
    clazzes = relationship("Clazz", back_populates="teacher", lazy="selectin")

    # 密码加密方法（把明文密码变成加密后的字符串）
    def set_password(self, raw_password: str):
        salt = bcrypt.gensalt()  # 生成“盐”（让密码更难破解）
        # 加密密码（先转成字节，加密后再转成字符串存储）
        self.password = bcrypt.hashpw(raw_password.encode("utf-8"), salt).decode("utf-8")

    # 密码验证方法（登录时验证输入的密码是否正确）
    def verify_password(self, raw_password: str) -> bool:
        # 把输入的明文密码和数据库里的加密密码对比
        return bcrypt.checkpw(raw_password.encode("utf-8"), self.password.encode("utf-8"))