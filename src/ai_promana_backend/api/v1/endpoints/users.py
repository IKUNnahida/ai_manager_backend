from fastapi import APIRouter, Depends, HTTPException
import pymysql
from datetime import datetime
from ai_promana_backend.database import get_db
from ai_promana_backend.core.security import verify_password, get_password_hash, create_access_token
from ai_promana_backend.schemas.user import UserCreate, UserLogin, UserOut, LoginResponse

router = APIRouter()

@router.post("/register", response_model=UserOut, summary="用户注册", description="创建新用户账户")
def register_user(
    payload: UserCreate,
    db: pymysql.connections.Connection = Depends(get_db)
):
    cursor = None
    try:
        cursor = db.cursor()
        
        # 检查用户名是否已存在
        cursor.execute("SELECT id FROM users WHERE username = %s", (payload.username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="用户名已存在")
        
        # 检查邮箱是否已存在
        if payload.email:
            cursor.execute("SELECT id FROM users WHERE email = %s", (payload.email,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="邮箱已被注册")
        
        # 检查手机号是否已存在
        if payload.phone:
            cursor.execute("SELECT id FROM users WHERE phone = %s", (payload.phone,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="手机号已被注册")
        
        # 哈希密码
        hashed_password = get_password_hash(payload.password)
        
        # 插入用户记录
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_sql = """
        INSERT INTO users (username, email, phone, password, full_name, role, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            insert_sql,
            (
                payload.username,
                payload.email,
                payload.phone,
                hashed_password,
                payload.full_name or payload.username,
                "user",
                now,
                now
            )
        )
        user_id = cursor.lastrowid
        db.commit()
        
        # 查询新创建的用户
        cursor.execute(
            "SELECT id, username, email, phone, full_name, role, created_at, updated_at FROM users WHERE id = %s",
            (user_id,)
        )
        user = cursor.fetchone()
        
        return UserOut(
            id=user["id"],
            username=user["username"],
            email=user["email"],
            phone=user["phone"],
            full_name=user["full_name"],
            role=user["role"],
            created_at=user["created_at"].strftime("%Y-%m-%d %H:%M:%S") if hasattr(user["created_at"], "strftime") else user["created_at"],
            updated_at=user["updated_at"].strftime("%Y-%m-%d %H:%M:%S") if hasattr(user["updated_at"], "strftime") else user["updated_at"]
        )
    
    except pymysql.MySQLError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"数据库操作失败：{str(e)}")
    finally:
        if cursor:
            cursor.close()

@router.post("/login", response_model=LoginResponse, summary="用户登录", description="用户登录获取访问令牌")
def login_user(
    payload: UserLogin,
    db: pymysql.connections.Connection = Depends(get_db)
):
    cursor = None
    try:
        cursor = db.cursor()
        
        # 查询用户
        cursor.execute(
            "SELECT id, username, email, phone, full_name, role, password, created_at, updated_at FROM users WHERE username = %s",
            (payload.username,)
        )
        user = cursor.fetchone()
        
        # 验证用户是否存在且密码正确
        if not user or not verify_password(payload.password, user["password"]):
            raise HTTPException(status_code=401, detail="用户名或密码错误")
        
        # 创建访问令牌
        access_token = create_access_token(data={"sub": user["id"], "username": user["username"], "role": user["role"]})
        
        return LoginResponse(
            access_token=access_token,
            user=UserOut(
                id=user["id"],
                username=user["username"],
                email=user["email"],
                phone=user["phone"],
                full_name=user["full_name"],
                role=user["role"],
                created_at=user["created_at"].strftime("%Y-%m-%d %H:%M:%S") if hasattr(user["created_at"], "strftime") else user["created_at"],
                updated_at=user["updated_at"].strftime("%Y-%m-%d %H:%M:%S") if hasattr(user["updated_at"], "strftime") else user["updated_at"]
            )
        )
    
    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"数据库操作失败：{str(e)}")
    finally:
        if cursor:
            cursor.close()
