import pymysql
from ai_promana_backend.config import settings

USERS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS `users` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增主键ID',
    `username` VARCHAR(50) NOT NULL COMMENT '用户名',
    `email` VARCHAR(255) DEFAULT NULL COMMENT '邮箱地址',
    `phone` VARCHAR(20) DEFAULT NULL COMMENT '手机号码',
    `password` VARCHAR(255) NOT NULL COMMENT '密码哈希',
    `full_name` VARCHAR(100) DEFAULT NULL COMMENT '真实姓名',
    `role` VARCHAR(20) NOT NULL DEFAULT 'user' COMMENT '用户角色',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uniq_username` (`username`),
    UNIQUE KEY `uniq_email` (`email`),
    UNIQUE KEY `uniq_phone` (`phone`),
    KEY `idx_role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户信息表';
"""

def setup_database():
    """初始化数据库表结构"""
    try:
        conn = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            charset="utf8mb4"
        )
        
        cursor = conn.cursor()
        
        # 创建数据库（如果不存在）
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.MYSQL_DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.execute(f"USE {settings.MYSQL_DATABASE}")
        
        # 创建用户表
        cursor.execute(USERS_TABLE_SQL)
        
        conn.commit()
        print("数据库表结构初始化成功")
        
    except pymysql.MySQLError as e:
        print(f"数据库初始化失败：{str(e)}")
        raise
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    setup_database()
