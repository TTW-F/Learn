from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from Student_Management_System.app.database import Base

class Clazz(Base):
    __tablename__ = "clazz"

    id = Column(Integer, primary_key=True, comment="班级ID")
    class_name = Column(
        String(50),
        unique=True,  # 班级名称不能重复
        nullable=False,
        comment="班级名称（比如：2023级计算机1班）"
    )
    grade = Column(String(20), nullable=False, comment="年级（比如：2023级）")
    major = Column(String(50), nullable=False, comment="专业（比如：计算机科学与技术）")
    teacher_id = Column(
        Integer,
        ForeignKey("user.id", ondelete="SET NULL"),  # 关联用户表的ID（班主任）
        comment="班主任ID"
    )
    create_time = Column(DateTime, default=datetime.utcnow, comment="创建时间")

    # 关系映射：班级和班主任、学生的关联
    teacher = relationship("User", back_populates="clazzes")  # 班级对应1个班主任
    students = relationship("Student", back_populates="clazz", cascade="all, delete-orphan")  # 班级对应多个学生