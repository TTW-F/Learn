from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from Student_Management_System.app.database import get_db
from Student_Management_System.app.models import Student, User, Clazz
from Student_Management_System.app.schemas.student import StudentCreate, StudentUpdate, StudentBase, StudentPagination
from Student_Management_System.app.dependencies import get_current_user, role_required

# 创建路由对象
router = APIRouter(
    prefix="/api/students",
    tags=["学生管理"]
)


# 1. 查询学生列表（管理员和教师能看，支持分页、搜索）
@router.get("", response_model=StudentPagination, summary="查询所有学生")
async def get_students(
        db: AsyncSession = Depends(get_db),
        # 权限控制：只允许admin和teacher访问
        current_user: User = Depends(role_required(["admin", "teacher"])),
        page: int = Query(1, ge=1, description="页码，默认第1页"),
        size: int = Query(10, ge=1, le=100, description="每页显示数量，默认10个"),
        name: Optional[str] = Query(None, description="按姓名模糊搜索（可选）"),
        clazz_id: Optional[int] = Query(None, description="按班级ID筛选（可选）")
):
    # 构建查询条件
    stmt = select(Student).join(User).join(Clazz)  # 关联用户表和班级表（要显示用户名和班级名）
    if name:
        # 模糊查询：姓名包含name的学生（比如name=张三，会查到张三、张三丰）
        stmt = stmt.filter(Student.student_name.like(f"%{name}%"))
    if clazz_id:
        # 精确查询：指定班级ID的学生
        stmt = stmt.filter(Student.clazz_id == clazz_id)

    # 分页查询：跳过前面的记录，取当前页的记录（相当于SQL的LIMIT和OFFSET）
    offset = (page - 1) * size
    result = await db.execute(stmt.offset(offset).limit(size))
    students = result.scalars().unique().all()  # 获取查询结果

    # 查询总条数（用于计算总页数）
    total = await db.scalar(select(func.count(Student.id)).where(stmt.whereclause))

    # 格式化结果（把数据库模型转换成响应模型，包含班级名称）
    student_list = []
    for student in students:
        student_list.append(StudentBase(
            id=student.id,
            student_name=student.student_name,
            gender=student.gender,
            age=student.age,
            phone=student.phone,
            email=student.email,
            clazz_id=student.clazz_id,
            clazz_name=student.clazz.class_name,  # 从关联的班级表获取班级名
            username=student.user.username,  # 从关联的用户表获取用户名
            create_time=student.create_time
        ))

    # 返回分页结果
    return {
        "items": student_list,
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size  # 总页数（向上取整）
    }


# 2. 添加学生（只有管理员能操作）
@router.post("", response_model=StudentBase, summary="添加新学生")
async def create_student(
        student_in: StudentCreate,  # 接收添加学生的参数（会自动校验）
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(role_required(["admin"]))  # 仅管理员可添加
):
    # 校验1：用户名是否已存在（不能重复）
    existing_user = await db.scalar(select(User).filter(User.username == student_in.username))
    if existing_user:
        raise HTTPException(status_code=400, detail=f"用户名{student_in.username}已存在")

    # 校验2：班级ID是否存在（不能给不存在的班级添加学生）
    clazz = await db.get(Clazz, student_in.clazz_id)
    if not clazz:
        raise HTTPException(status_code=400, detail=f"班级ID{student_in.clazz_id}不存在")

    # 步骤1：创建用户账号（学生的登录账号，角色是student）
    user = User(
        username=student_in.username,
        role="student"  # 固定为学生角色
    )
    user.set_password(student_in.password)  # 加密密码
    db.add(user)  # 把用户添加到数据库会话
    await db.flush()  # 刷新会话，获取自动生成的user.id（不用提交事务）

    # 步骤2：创建学生信息（关联上面的用户ID）
    student = Student(
        user_id=user.id,
        student_name=student_in.student_name,
        gender=student_in.gender,
        age=student_in.age,
        phone=student_in.phone,
        email=student_in.email,
        clazz_id=student_in.clazz_id
    )
    db.add(student)  # 把学生添加到数据库会话
    await db.commit()  # 提交事务（保存到数据库）
    await db.refresh(student)  # 刷新学生对象，获取最新数据

    # 格式化并返回结果
    return StudentBase(
        id=student.id,
        student_name=student.student_name,
        gender=student.gender,
        age=student.age,
        phone=student.phone,
        email=student.email,
        clazz_id=student.clazz_id,
        clazz_name=clazz.class_name,
        username=user.username,
        create_time=student.create_time
    )


# 3. 查询单个学生（管理员/教师能查所有，学生只能查自己）
@router.get("/{student_id}", response_model=StudentBase, summary="查询单个学生")
async def get_student(
        student_id: int,  # 从URL获取学生ID（比如/api/students/1就是查ID=1的学生）
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(role_required(["admin", "teacher", "student"]))
):
    # 查询学生（关联用户表和班级表）
    student = await db.scalar(select(Student).join(User).join(Clazz).filter(Student.id == student_id))
    if not student:
        raise HTTPException(status_code=404, detail=f"学生ID{student_id}不存在")

    # 权限控制：学生只能查自己的信息
    if current_user.role == "student" and current_user.id != student.user_id:
        raise HTTPException(status_code=403, detail="无权查询他人信息")

    # 返回结果
    return StudentBase(
        id=student.id,
        student_name=student.student_name,
        gender=student.gender,
        age=student.age,
        phone=student.phone,
        email=student.email,
        clazz_id=student.clazz_id,
        clazz_name=student.clazz.class_name,
        username=student.user.username,
        create_time=student.create_time
    )


# 4. 更新学生信息（只有管理员/教师能操作）
@router.put("/{student_id}", response_model=StudentBase, summary="更新学生信息")
async def update_student(
        student_id: int,  # 要更新的学生ID
        student_in: StudentUpdate,  # 要更新的参数（可选字段）
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(role_required(["admin", "teacher"]))
):
    # 查询学生是否存在
    student = await db.scalar(select(Student).join(Clazz).filter(Student.id == student_id))
    if not student:
        raise HTTPException(status_code=404, detail=f"学生ID{student_id}不存在")

    # 校验：如果更新班级ID，要确保班级存在
    if student_in.clazz_id:
        clazz = await db.get(Clazz, student_in.clazz_id)
        if not clazz:
            raise HTTPException(status_code=400, detail=f"班级ID{student_in.clazz_id}不存在")

    # 更新字段：只更新传入的非空字段（比如只传了姓名，就只改姓名）
    update_data = student_in.model_dump(exclude_unset=True)  # 把校验模型转成字典，排除未设置的字段
    for key, value in update_data.items():
        setattr(student, key, value)  # 给学生对象赋值

    db.add(student)  # 添加到会话
    await db.commit()  # 提交事务
    await db.refresh(student)  # 刷新数据

    # 返回更新后的结果
    return StudentBase(
        id=student.id,
        student_name=student.student_name,
        gender=student.gender,
        age=student.age,
        phone=student.phone,
        email=student.email,
        clazz_id=student.clazz_id,
        clazz_name=student.clazz.class_name,
        username=student.user.username,
        create_time=student.create_time
    )


# 5. 删除学生（只有管理员能操作）
@router.delete("/{student_id}", summary="删除学生")
async def delete_student(
        student_id: int,  # 要删除的学生ID
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(role_required(["admin"]))  # 仅管理员可删除
):
    # 查询学生是否存在
    student = await db.scalar(select(Student).filter(Student.id == student_id))
    if not student:
        raise HTTPException(status_code=404, detail=f"学生ID{student_id}不存在")

    # 删除学生（会级联删除关联的用户账号）
    await db.delete(student)
    await db.commit()  # 提交事务

    # 返回成功信息
    return {"code": 200, "msg": f"学生ID{student_id}删除成功"}