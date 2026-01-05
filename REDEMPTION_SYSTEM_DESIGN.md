# 兑换码系统设计文档

## 系统概述

将原自动化批量注册工具改造为基于Web的兑换码系统，用户可以通过输入邮箱和兑换码来兑换ChatGPT Team席位。

## 系统架构

```
┌─────────────────┐
│   用户浏览器     │
│  (输入邮箱+码)   │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│  Flask Web服务  │
│  - 兑换接口     │
│  - 管理后台     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  SQLite数据库   │
│  - 兑换码表     │
│  - 兑换记录表   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Team Service   │
│  (邀请到Team)   │
└─────────────────┘
```

## 数据库设计

### 表结构

#### 1. redemption_codes (兑换码表)
```sql
CREATE TABLE redemption_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(32) UNIQUE NOT NULL,           -- 兑换码
    team_name VARCHAR(100) NOT NULL,            -- 关联的Team
    max_uses INTEGER DEFAULT 1,                 -- 最大使用次数
    used_count INTEGER DEFAULT 0,               -- 已使用次数
    expires_at DATETIME,                        -- 过期时间
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active',        -- active/disabled/expired
    notes TEXT                                  -- 备注
);
```

#### 2. redemptions (兑换记录表)
```sql
CREATE TABLE redemptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code_id INTEGER NOT NULL,                   -- 关联兑换码ID
    email VARCHAR(255) NOT NULL,                -- 用户邮箱
    team_name VARCHAR(100) NOT NULL,            -- Team名称
    redeemed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    invite_status VARCHAR(20) DEFAULT 'pending', -- pending/success/failed
    error_message TEXT,                         -- 错误信息
    ip_address VARCHAR(45),                     -- 用户IP
    FOREIGN KEY (code_id) REFERENCES redemption_codes(id)
);
```

#### 3. teams_stats (Team统计表)
```sql
CREATE TABLE teams_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name VARCHAR(100) UNIQUE NOT NULL,
    total_seats INTEGER DEFAULT 0,              -- 总席位数
    used_seats INTEGER DEFAULT 0,               -- 已使用席位
    pending_invites INTEGER DEFAULT 0,          -- 待接受邀请
    available_seats INTEGER DEFAULT 0,          -- 可用席位
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 核心模块

### 1. database.py - 数据库管理模块
- 初始化数据库
- CRUD操作封装
- 事务管理

### 2. redemption_service.py - 兑换服务模块
- 验证兑换码
- 执行兑换逻辑
- 更新统计信息

### 3. code_generator.py - 兑换码生成工具
- 批量生成兑换码
- 支持自定义前缀
- 导出兑换码列表

### 4. web_server.py - Web服务器
- Flask应用
- API路由
- 静态文件服务

### 5. admin.py - 管理后台
- 兑换码管理
- 兑换记录查询
- Team统计监控

## API接口设计

### 1. 兑换接口
```
POST /api/redeem
Content-Type: application/json

Request:
{
    "email": "user@example.com",
    "code": "TEAM-ABCD-1234"
}

Response (成功):
{
    "success": true,
    "message": "兑换成功！邀请邮件已发送到 user@example.com",
    "data": {
        "email": "user@example.com",
        "team": "TeamA",
        "redeemed_at": "2026-01-05 12:00:00"
    }
}

Response (失败):
{
    "success": false,
    "error": "兑换码无效或已过期",
    "code": "INVALID_CODE"
}
```

### 2. 验证兑换码
```
GET /api/verify?code=TEAM-ABCD-1234

Response:
{
    "valid": true,
    "team": "TeamA",
    "expires_at": "2026-12-31 23:59:59",
    "remaining_uses": 5
}
```

### 3. 管理接口 (需要认证)
```
GET /api/admin/codes - 获取所有兑换码
POST /api/admin/codes - 生成新兑换码
GET /api/admin/redemptions - 获取兑换记录
GET /api/admin/stats - 获取统计信息
```

## 前端页面

### 1. 用户兑换页面 (index.html)
- 简洁的输入表单
- 实时验证
- 成功/失败提示
- 响应式设计

### 2. 管理后台 (admin.html)
- 兑换码列表和管理
- 兑换记录查询
- Team统计仪表盘
- 批量生成兑换码

## 工作流程

### 用户兑换流程
```
1. 用户访问兑换页面
2. 输入邮箱 + 兑换码
3. 前端验证格式
4. 提交到 /api/redeem
5. 后端验证兑换码
   - 检查有效性
   - 检查过期时间
   - 检查使用次数
6. 调用 team_service.batch_invite_to_team()
7. 更新数据库记录
8. 返回结果给用户
```

### 管理员生成兑换码流程
```
1. 运行 code_generator.py
2. 输入生成参数:
   - 数量
   - Team名称
   - 有效期
   - 单码可用次数
3. 生成随机兑换码
4. 保存到数据库
5. 导出CSV文件分发
```

## 安全措施

1. **防刷机制**
   - IP限流 (同一IP每小时最多10次)
   - 邮箱限制 (同一邮箱最多兑换1次)
   - 验证码 (可选)

2. **兑换码保护**
   - 随机生成 (26字符混合)
   - 使用次数限制
   - 过期时间控制
   - 禁用/启用开关

3. **管理后台认证**
   - 简单密码认证
   - Session管理

## 配置更新

在 config.toml 中添加:
```toml
[redemption]
database_file = "redemption.db"
rate_limit_per_hour = 10
enable_ip_check = true

[web]
host = "0.0.0.0"
port = 5000
debug = false
admin_password = "your-secure-password"
```

## 部署方案

### 本地运行
```bash
# 1. 安装依赖
pip install flask

# 2. 初始化数据库
python database.py

# 3. 生成兑换码
python code_generator.py --team TeamA --count 100

# 4. 启动Web服务
python web_server.py
```

### 生产部署
```bash
# 使用 Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_server:app

# 或使用 Nginx 反向代理
```

## 文件清单

新增文件:
- `database.py` - 数据库管理
- `redemption_service.py` - 兑换服务
- `code_generator.py` - 兑换码生成器
- `web_server.py` - Web服务器
- `admin.py` - 管理模块
- `static/index.html` - 用户兑换页面
- `static/admin.html` - 管理后台
- `static/style.css` - 样式文件
- `static/script.js` - 前端脚本
- `redemption.db` - SQLite数据库

保留文件:
- `team_service.py` - 继续使用邀请功能
- `config.py` - 扩展配置
- `logger.py` - 日志系统

## 使用场景

1. **一次性兑换码**
   - 每个码只能用一次
   - 适合活动推广

2. **多次兑换码**
   - 每个码可用N次
   - 适合团队批量分发

3. **限时兑换码**
   - 设置过期时间
   - 适合时效性活动

4. **团队专属码**
   - 绑定特定Team
   - 方便多Team管理
