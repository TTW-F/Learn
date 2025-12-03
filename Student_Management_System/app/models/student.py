from Student_Management_System.app.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, comment="学生ID")
    user_id = Column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),  # 关联用户表（删除用户时一起删除学生）
        unique=True,
        nullable=False,
        comment="关联的登录账号ID"
    )

    student_name = Column(String(50), nullable=False, comment="学生姓名")
    gender = Column(
        Enum("男", "女", "其他"),  # 性别只能选这三个
        nullable=False,
        comment="性别"
    )

    age = Column(Integer, nullable=False, comment="年龄")
    phone = Column(String(20), comment="手机号（可选）")
    email = Column(String(100), comment="邮箱（可选）")
    clazz_id = Column(
        Integer,
        ForeignKey("clazz.id", ondelete="RESTRICT"),  # 关联班级表（删除班级前必须先转移学生）
        nullable=False,
        comment="所属班级ID"
    )
    create_time = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    update_time = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="更新时间"
    )

    # 关系映射：学生和用户、班级、成绩的关联
    user = relationship("User", back_populates="student")  # 学生对应1个登录账号
    clazz = relationship("Clazz", back_populates="students")  # 学生对应1个班级