# ⚡ 本地启动 - 5分钟快速指南

## 📌 必需文件

在项目根目录需要这2个文件：

### 1️⃣ team.json

访问 https://chatgpt.com/api/auth/session (需先登录ChatGPT Team管理员账号)

复制内容创建 `team.json`:

```json
[{
    "user": {
        "id": "user-从网页复制",
        "email": "你的Team管理员邮箱"
    },
    "account": {
        "id": "从网页复制",
        "organizationId": "从网页复制"
    },
    "accessToken": "从网页复制（很长一串）"
}]
```

### 2️⃣ config.toml

```bash
# 复制模板
copy config.toml.example config.toml  # Windows
cp config.toml.example config.toml    # Linux/macOS
```

编辑 `config.toml`，修改这一行：

```toml
admin_password = "改成你的密码"  # 第71行
```

---

## 🚀 启动步骤

```bash
# 1. 安装依赖
pip install flask gunicorn

# 2. 初始化数据库
python database.py

# 3. 生成兑换码（Team名 = 你的邮箱@前面的部分）
python code_generator.py generate --team admin --count 10

# 4. 启动服务
python start_redemption.py
```

---

## 🌐 访问地址

- 👤 **用户兑换**: http://localhost:5000/
- 🔧 **管理后台**: http://localhost:5000/admin

---

## ✅ 测试兑换

1. 打开 http://localhost:5000/
2. 输入邮箱和兑换码
3. 点击"立即兑换"
4. 查收邮件

---

## 📊 查看数据

- 登录管理后台: http://localhost:5000/admin
- 输入你设置的密码
- 可查看兑换记录、统计数据

---

## 🔧 常用命令

```bash
# 生成更多兑换码
python code_generator.py generate --team admin --count 100

# 查看兑换码列表
python code_generator.py list

# 查看统计
python code_generator.py stats

# 重启服务
# Ctrl+C 停止，然后再运行
python start_redemption.py
```

---

## ❓ 遇到问题？

### 找不到team.json
- 确保文件在项目**根目录**
- 文件名是 `team.json` 不是 `team.json.txt`

### Team名称错误
```
邮箱: admin@company.com
Team名: admin  ← 用@前面的部分

或者随便取个名字，保持一致即可
```

### 端口被占用
修改 `config.toml`:
```toml
port = 5001  # 改成其他端口
```

### 没收到邮件
- 检查垃圾邮件
- 管理后台查看兑换状态
- 确认Team还有空位

---

## 📁 文件位置

```
项目目录/
├── config.toml       ← 你创建的
├── team.json         ← 你创建的
├── redemption.db     ← 自动生成
└── ...其他代码文件
```

---

## 💡 记住

- **Team名** = 邮箱@前面的部分（或自定义）
- **管理密码** = config.toml 中设置的
- **数据保存在** redemption.db 中
- **每次重启只需** `python start_redemption.py`

---

详细说明见: [LOCAL_SETUP_GUIDE.md](LOCAL_SETUP_GUIDE.md)
