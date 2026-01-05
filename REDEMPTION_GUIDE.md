# ChatGPT Team 兑换码系统 - 使用指南

## 📋 目录

1. [系统简介](#系统简介)
2. [快速开始](#快速开始)
3. [配置说明](#配置说明)
4. [生成兑换码](#生成兑换码)
5. [启动Web服务](#启动web服务)
6. [用户兑换流程](#用户兑换流程)
7. [管理后台使用](#管理后台使用)
8. [API接口文档](#api接口文档)
9. [常见问题](#常见问题)

---

## 系统简介

这是一个基于Web的ChatGPT Team席位兑换系统，允许用户通过输入邮箱和兑换码来兑换Team席位。

### 主要功能

- ✅ **兑换码管理**: 批量生成、启用/禁用兑换码
- ✅ **用户兑换**: 简洁的Web界面,输入邮箱+兑换码即可兑换
- ✅ **自动邀请**: 兑换成功后自动邀请用户到ChatGPT Team
- ✅ **管理后台**: 实时查看兑换记录、统计数据、Team席位状态
- ✅ **防刷机制**: IP限流、邮箱唯一性检查
- ✅ **灵活配置**: 支持多Team、自定义有效期、使用次数限制

### 系统架构

```
用户浏览器 → Flask Web服务 → SQLite数据库 → Team Service (邀请API)
```

---

## 快速开始

### 1. 环境要求

- Python 3.12+
- pip (Python包管理器)

### 2. 安装依赖

```bash
pip install flask
```

### 3. 配置Team凭证

1. 复制配置文件模板:
```bash
cp config.toml.example config.toml
```

2. 获取Team凭证:
   - 登录ChatGPT Team管理员账号
   - 访问 `https://chatgpt.com/api/auth/session`
   - 复制整个JSON响应

3. 创建 `team.json` 文件:
```json
[{
    "user": {
        "id": "user-xxx",
        "email": "your-team-admin@example.com"
    },
    "account": {
        "id": "account-id",
        "organizationId": "org-xxx"
    },
    "accessToken": "eyJhbGciOiJSUzI1NiIs..."
}]
```

4. 编辑 `config.toml`,修改以下配置:
```toml
[web]
admin_password = "your-secure-password"  # 管理后台密码
```

### 4. 初始化数据库

```bash
python database.py
```

### 5. 生成兑换码

```bash
# 生成10个兑换码,绑定到 TeamA
python code_generator.py generate --team TeamA --count 10

# 生成100个兑换码,每个码可用5次,有效期30天
python code_generator.py generate --team TeamA --count 100 --max-uses 5 --valid-days 30
```

### 6. 启动Web服务

```bash
python web_server.py
```

访问:
- 用户兑换页面: http://localhost:5000/
- 管理后台: http://localhost:5000/admin

---

## 配置说明

### config.toml 配置项

```toml
# 兑换系统配置
[redemption]
database_file = "redemption.db"        # 数据库文件路径
rate_limit_per_hour = 10               # IP限流: 每小时最多兑换次数
enable_ip_check = true                 # 是否启用IP检查

# Web服务配置
[web]
host = "0.0.0.0"                       # 监听地址
port = 5000                            # 监听端口
debug = false                          # 调试模式(生产环境设为false)
admin_password = "change-me"           # 管理后台密码
enable_admin = true                    # 是否启用管理后台
```

### team.json 格式

可以配置多个Team:

```json
[
  {
    "user": {"id": "user-1", "email": "admin1@example.com"},
    "account": {"id": "account-1", "organizationId": "org-1"},
    "accessToken": "token-1"
  },
  {
    "user": {"id": "user-2", "email": "admin2@example.com"},
    "account": {"id": "account-2", "organizationId": "org-2"},
    "accessToken": "token-2"
  }
]
```

---

## 生成兑换码

### 命令行工具: code_generator.py

#### 生成兑换码

```bash
# 基础用法: 生成10个兑换码
python code_generator.py generate --team TeamA --count 10

# 完整参数示例
python code_generator.py generate \
  --team TeamA \              # Team名称(必需)
  --count 100 \               # 生成数量(默认:10)
  --max-uses 5 \              # 每个码最大使用次数(默认:1)
  --valid-days 30 \           # 有效天数(不指定则永久有效)
  --prefix PROMO \            # 兑换码前缀(默认:TEAM)
  --notes "春节活动" \        # 备注信息
  --export codes.csv          # 导出到CSV文件
```

**生成的兑换码格式**: `TEAM-ABCD-1234-EFGH`

#### 查看兑换码列表

```bash
# 查看所有兑换码
python code_generator.py list

# 按Team筛选
python code_generator.py list --team TeamA

# 按状态筛选
python code_generator.py list --status active
```

#### 启用/禁用兑换码

```bash
# 禁用兑换码
python code_generator.py disable TEAM-ABCD-1234-EFGH

# 启用兑换码
python code_generator.py enable TEAM-ABCD-1234-EFGH
```

#### 查看统计信息

```bash
python code_generator.py stats
```

---

## 启动Web服务

### 开发环境

```bash
python web_server.py
```

### 生产环境

使用 Gunicorn (推荐):

```bash
# 安装 Gunicorn
pip install gunicorn

# 启动服务 (4个工作进程)
gunicorn -w 4 -b 0.0.0.0:5000 web_server:app

# 后台运行
nohup gunicorn -w 4 -b 0.0.0.0:5000 web_server:app > web.log 2>&1 &
```

### 使用 Nginx 反向代理

Nginx 配置示例:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## 用户兑换流程

### 1. 访问兑换页面

用户访问: `http://your-domain.com/`

### 2. 输入信息

- **邮箱地址**: 用户的真实邮箱
- **兑换码**: 管理员提供的兑换码

### 3. 验证兑换码

输入兑换码后,系统会自动验证:
- ✅ 有效: 显示Team名称、剩余可用次数
- ❌ 无效: 显示错误原因(过期、已用尽等)

### 4. 提交兑换

点击"立即兑换",系统执行:
1. 验证邮箱格式
2. 检查IP限流
3. 检查邮箱是否已兑换
4. 验证兑换码有效性
5. 检查Team席位
6. 邀请用户到Team
7. 发送邀请邮件

### 5. 查收邮件

用户会收到来自ChatGPT的邀请邮件,点击链接完成注册。

---

## 管理后台使用

### 访问方式

1. 访问: `http://your-domain.com/admin`
2. 输入管理密码 (在 config.toml 中配置)

### 功能模块

#### 1. 仪表盘统计

实时显示:
- 总兑换码数
- 激活的兑换码数
- 总兑换次数
- 成功兑换次数
- 今日兑换次数

#### 2. 兑换码管理

- 查看所有兑换码
- 按Team/状态筛选
- 启用/禁用兑换码
- 查看使用情况

#### 3. 兑换记录

- 查看所有兑换记录
- 显示邮箱、兑换码、Team、状态、时间、IP
- 实时更新

#### 4. Team统计

- 查看所有Team的席位使用情况
- 总席位、已使用、待接受、可用席位
- 最后更新时间

---

## API接口文档

### 用户API

#### 1. 兑换接口

```
POST /api/redeem
Content-Type: application/json

请求体:
{
    "email": "user@example.com",
    "code": "TEAM-ABCD-1234-EFGH"
}

成功响应 (200):
{
    "success": true,
    "message": "兑换成功！邮件已发送到 user@example.com",
    "data": {
        "email": "user@example.com",
        "team": "TeamA",
        "redeemed_at": "2026-01-05T12:00:00"
    }
}

失败响应 (400/429/500):
{
    "success": false,
    "error": "错误信息",
    "code": "ERROR_CODE"
}
```

错误码:
- `INVALID_EMAIL`: 邮箱格式无效
- `INVALID_CODE`: 兑换码无效
- `RATE_LIMIT`: 操作过于频繁
- `EMAIL_ALREADY_REDEEMED`: 邮箱已兑换
- `NO_SEATS`: Team席位已满
- `INVITE_FAILED`: 邀请失败

#### 2. 验证兑换码

```
GET /api/verify?code=TEAM-ABCD-1234-EFGH

响应 (200):
{
    "valid": true,
    "code": "TEAM-ABCD-1234-EFGH",
    "team": "TeamA",
    "max_uses": 5,
    "used_count": 2,
    "remaining_uses": 3,
    "expires_at": "2026-12-31T23:59:59",
    "status": "active"
}
```

### 管理API (需要登录)

#### 1. 获取统计信息

```
GET /api/admin/stats

响应:
{
    "success": true,
    "data": {
        "dashboard": {
            "total_codes": 100,
            "active_codes": 80,
            "total_redemptions": 50,
            "successful_redemptions": 45,
            "today_redemptions": 5
        },
        "teams": [...]
    }
}
```

#### 2. 获取兑换码列表

```
GET /api/admin/codes?team=TeamA&status=active
```

#### 3. 获取兑换记录

```
GET /api/admin/redemptions?limit=50&offset=0
```

#### 4. 更新兑换码状态

```
PUT /api/admin/codes/{code}/status
Content-Type: application/json

{
    "status": "disabled"  // active/disabled/expired
}
```

---

## 常见问题

### Q1: 如何修改管理后台密码?

编辑 `config.toml`:
```toml
[web]
admin_password = "your-new-password"
```
然后重启Web服务。

### Q2: 如何限制每个邮箱只能兑换一次?

系统默认已实现该限制,无需额外配置。每个邮箱成功兑换后,无法再次兑换。

### Q3: 如何防止恶意刷兑换?

系统内置IP限流机制:
```toml
[redemption]
rate_limit_per_hour = 10  # 每小时最多10次
enable_ip_check = true
```

### Q4: 兑换码可以重复使用吗?

可以,在生成时设置 `--max-uses` 参数:
```bash
python code_generator.py generate --team TeamA --max-uses 10
```

### Q5: 如何设置兑换码过期时间?

生成时使用 `--valid-days` 参数:
```bash
python code_generator.py generate --team TeamA --valid-days 30
```

### Q6: Team席位满了怎么办?

系统会自动检测,如果席位已满,会提示用户"Team席位已满"并拒绝兑换。

### Q7: 如何查看某个用户的兑换记录?

访问管理后台 → 兑换记录,可查看所有兑换历史(包括邮箱、时间、状态等)。

### Q8: 可以同时管理多个Team吗?

可以,在 `team.json` 中添加多个Team配置即可:
```json
[
  {"user": {...}, "account": {...}, "accessToken": "..."},
  {"user": {...}, "account": {...}, "accessToken": "..."}
]
```

### Q9: 如何备份数据?

数据库文件: `redemption.db`
```bash
# 备份
cp redemption.db redemption.db.backup

# 定时备份 (cron)
0 2 * * * cp /path/to/redemption.db /path/to/backup/redemption.db.$(date +\%Y\%m\%d)
```

### Q10: 如何迁移到新服务器?

复制以下文件到新服务器:
- `redemption.db` (数据库)
- `config.toml` (配置)
- `team.json` (Team凭证)
- 所有Python脚本

---

## 安全建议

1. **修改默认密码**: 务必修改 `config.toml` 中的 `admin_password`
2. **使用HTTPS**: 生产环境建议配置SSL证书
3. **定期备份**: 定期备份 `redemption.db` 数据库
4. **限制访问**: 使用Nginx配置IP白名单(仅管理后台)
5. **监控日志**: 定期查看Web服务日志,发现异常行为

---

## 技术支持

如有问题,请查看:
- 设计文档: `REDEMPTION_SYSTEM_DESIGN.md`
- 代码注释: 各Python模块内的详细注释
- 日志文件: 运行时会输出详细日志

---

## 更新日志

### v1.0.0 (2026-01-05)
- ✅ 初始版本发布
- ✅ 兑换码生成和管理
- ✅ Web兑换界面
- ✅ 管理后台
- ✅ SQLite数据库
- ✅ 防刷机制
- ✅ 完整文档
