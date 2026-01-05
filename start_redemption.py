#!/usr/bin/env python3
"""
快速启动脚本
自动检查配置、初始化数据库、启动Web服务
"""

import os
import sys
from pathlib import Path
from logger import log


def check_requirements():
    """检查必需的文件"""
    required_files = {
        "config.toml": "配置文件 (请复制 config.toml.example 并修改)",
        "team.json": "Team凭证文件 (请从 https://chatgpt.com/api/auth/session 获取)",
    }

    missing_files = []
    for file, desc in required_files.items():
        if not Path(file).exists():
            missing_files.append(f"  [X] {file} - {desc}")

    if missing_files:
        log.error("缺少必需的配置文件:")
        for msg in missing_files:
            print(msg)
        print("\n请先完成配置后再启动服务。")
        print("详细说明请查看: REDEMPTION_GUIDE.md")
        return False

    log.info("配置文件检查通过", icon="success")
    return True


def init_database():
    """初始化数据库"""
    try:
        from database import db

        log.info("数据库初始化完成", icon="success")
        return True
    except Exception as e:
        log.error(f"数据库初始化失败: {e}")
        return False


def check_codes():
    """检查是否有兑换码"""
    try:
        from database import db

        stats = db.get_dashboard_stats()
        total_codes = stats["total_codes"]

        if total_codes == 0:
            log.warning("当前没有兑换码,请先生成兑换码:")
            print(
                "\n  python code_generator.py generate --team TeamA --count 10\n"
            )
            return False

        log.info(f"当前有 {total_codes} 个兑换码", icon="success")
        return True
    except Exception as e:
        log.error(f"检查兑换码失败: {e}")
        return False


def start_server():
    """启动Web服务"""
    try:
        import config
        from web_server import run_server

        host = config.get("web.host", "0.0.0.0")
        port = config.get("web.port", 5000)
        debug = config.get("web.debug", False)

        print("\n" + "=" * 60)
        log.info("启动 ChatGPT Team 兑换码系统", icon="start")
        print("=" * 60)
        print(f"\n[Page] 用户兑换页面: http://{host}:{port}/")
        print(f"[Admin] 管理后台: http://{host}:{port}/admin")
        print(f"[Key] 管理密码: {config.get('web.admin_password', 'admin123')}")
        print("\n按 Ctrl+C 停止服务\n")
        print("=" * 60 + "\n")

        run_server(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n\n[Bye] 服务已停止")
        sys.exit(0)
    except Exception as e:
        log.error(f"启动服务失败: {e}")
        sys.exit(1)


def main():
    """主函数"""
    print("\n[Check] 检查系统环境...\n")

    # 1. 检查配置文件
    if not check_requirements():
        sys.exit(1)

    # 2. 初始化数据库
    if not init_database():
        sys.exit(1)

    # 3. 检查兑换码(仅提醒,不阻止启动)
    check_codes()

    # 4. 启动服务
    start_server()


if __name__ == "__main__":
    main()
