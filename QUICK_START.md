# 兑换码系统 - 快速参考

## 🚀 3分钟快速启动

### 步骤1: 准备Team凭证

访问 https://chatgpt.com/api/auth/session (需先登录Team管理员账号)

复制JSON内容创建 `team.json`:

```json
[{
    "user": {"id": "user-xxx", "email": "admin@example.com"},
    "account": {"id": "account-xxx", "organizationId": "org-xxx"},
    "accessToken": "eyJhbGci..."
}]
```

### 步骤2: 配置密码

复制配置文件:
```bash
cp config.toml.example config.toml
```

修改管理密码:
```toml
[web]
admin_password = "your-secure-password"
```

### 步骤3: 生成兑换码

```bash
python code_generator.py generate --team TeamA --count 10
```

### 步骤4: 启动服务

```bash
python start_redemption.py
```

访问:
- 用户兑换: http://localhost:5000/
- 管理后台: http://localhost:5000/admin

---

## 📋 常用命令速查

### 生成兑换码

```bash
# 基础生成
python code_generator.py generate --team TeamA --count 10

# 多次使用 + 有效期
python code_generator.py generate --team TeamA --count 100 --max-uses 5 --valid-days 30

# 自定义前缀 + 导出CSV
python code_generator.py generate --team TeamA --count 50 --prefix PROMO --export codes.csv
```

### 管理兑换码

```bash
# 查看列表
python code_generator.py list
python code_generator.py list --team TeamA
python code_generator.py list --status active

# 禁用/启用
python code_generator.py disable TEAM-XXXX-XXXX-XXXX
python code_generator.py enable TEAM-XXXX-XXXX-XXXX

# 查看统计
python code_generator.py stats
```

### 启动服务

```bash
# 快速启动(自动检查)
python start_redemption.py

# 直接启动
python web_server.py

# 生产环境(Gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 web_server:app
```

---

## 🔧 配置速查

### config.toml 关键配置

```toml
[redemption]
database_file = "redemption.db"       # 数据库文件
rate_limit_per_hour = 10              # IP限流
enable_ip_check = true                # IP检查

[web]
host = "0.0.0.0"                      # 监听地址
port = 5000                           # 端口
debug = false                         # 调试模式
admin_password = "change-me"          # 管理密码
enable_admin = true                   # 启用后台
```

---

## 📊 数据库文件

- `redemption.db` - SQLite数据库(兑换码+记录)
- 备份: `cp redemption.db redemption.db.backup`
- 查看: 使用SQLite客户端或管理后台

---

## 🔐 安全检查清单

- [ ] 修改默认管理密码
- [ ] 配置IP限流
- [ ] 生产环境关闭debug模式
- [ ] 使用HTTPS (Nginx反向代理)
- [ ] 定期备份数据库
- [ ] 监控兑换记录

---

## ❓ 常见问题速答

**Q: 如何添加多个Team?**
A: 在 `team.json` 中添加多个JSON对象即可

**Q: 兑换码格式是什么?**
A: `TEAM-XXXX-XXXX-XXXX` (前缀-4位-4位-4位)

**Q: 如何限制每人只能兑换一次?**
A: 系统默认检查邮箱唯一性，无需额外配置

**Q: 兑换后用户收不到邮件?**
A: 检查Team席位是否已满，查看管理后台的兑换记录状态

**Q: 如何查看某个兑换码被谁用了?**
A: 访问管理后台 → 兑换记录

---

## 📁 文件结构

```
兑换系统核心文件:
├── database.py              # 数据库管理
├── redemption_service.py    # 兑换服务
├── code_generator.py        # 兑换码生成器
├── web_server.py            # Web服务器
├── start_redemption.py      # 快速启动脚本
│
├── static/
│   ├── index.html           # 用户兑换页面
│   └── admin.html           # 管理后台
│
├── config.toml              # 配置文件
├── team.json                # Team凭证
└── redemption.db            # 数据库
```

---

## 📞 获取帮助

- 完整文档: [REDEMPTION_GUIDE.md](REDEMPTION_GUIDE.md)
- 设计文档: [REDEMPTION_SYSTEM_DESIGN.md](REDEMPTION_SYSTEM_DESIGN.md)
- 项目README: [README.md](README.md)

---

## 🎯 典型使用流程

### 管理员流程

1. 配置Team凭证 → 2. 生成兑换码 → 3. 启动服务 → 4. 分发兑换码

### 用户流程

1. 访问兑换页面 → 2. 输入邮箱+兑换码 → 3. 点击兑换 → 4. 查收邮件

### 监控流程

1. 登录管理后台 → 2. 查看兑换记录 → 3. 监控Team席位 → 4. 管理兑换码
