#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简化版数据库初始化脚本（无emoji，兼容Windows）
"""

import sqlite3
from pathlib import Path

# 数据库文件路径
DB_FILE = Path(__file__).parent / "redemption.db"

def init_database():
    """初始化数据库"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        # 创建兑换码表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS redemption_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code VARCHAR(32) UNIQUE NOT NULL,
                team_name VARCHAR(100) NOT NULL,
                max_uses INTEGER DEFAULT 1,
                used_count INTEGER DEFAULT 0,
                expires_at DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(20) DEFAULT 'active',
                notes TEXT,
                locked_by TEXT,
                locked_until DATETIME
            )
        """)

        # 创建兑换记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS redemptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code_id INTEGER NOT NULL,
                email VARCHAR(255) NOT NULL,
                team_name VARCHAR(100) NOT NULL,
                redeemed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                invite_status VARCHAR(20) DEFAULT 'pending',
                error_message TEXT,
                ip_address VARCHAR(45),
                FOREIGN KEY (code_id) REFERENCES redemption_codes(id)
            )
        """)

        # 创建Team统计表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teams_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_name VARCHAR(100) UNIQUE NOT NULL,
                total_seats INTEGER DEFAULT 0,
                used_seats INTEGER DEFAULT 0,
                pending_invites INTEGER DEFAULT 0,
                available_seats INTEGER DEFAULT 0,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 创建索引
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_code ON redemption_codes(code)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_email ON redemptions(email)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_team ON redemption_codes(team_name)
        """)

        conn.commit()
        print("[SUCCESS] Database initialized successfully!")
        print(f"[INFO] Database file: {DB_FILE}")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to initialize database: {e}")
        conn.rollback()
        return False

    finally:
        conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("Initializing Redemption System Database...")
    print("=" * 60)

    success = init_database()

    print("=" * 60)
    if success:
        print("Database initialization completed!")
    else:
        print("Database initialization failed!")
    print("=" * 60)
