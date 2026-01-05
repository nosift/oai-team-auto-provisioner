# ⚡ 配置速查卡

## 📝 需要配置的2个文件

### 1️⃣ config.toml (已创建)

**只需改1处：**

找到第71行：
```toml
admin_password = "change-me-to-secure-password"
```

改成：
```toml
admin_password = "你的密码"
```

✅ 完成！其他不用改。

---

### 2️⃣ team.json (需要创建)

#### 获取凭证

1. 登录 https://chatgpt.com (Team管理员账号)
2. 访问 https://chatgpt.com/api/auth/session
3. 复制JSON数据

#### 创建文件

创建 `team.json`，内容：

```json
[
  {
    "user": {
      "id": "复制网页中的 user.id",
      "email": "复制网页中的 user.email"
    },
    "account": {
      "id": "复制网页中的 account.id",
      "organizationId": "复制网页中的 account.organizationId"
    },
    "accessToken": "复制网页中的 accessToken（很长的字符串）"
  }
]
```

#### 填写示例

网页JSON:
```json
{
  "user": {"id": "user-abc123", "email": "admin@company.com"},
  "account": {"id": "def456", "organizationId": "org-xyz987"},
  "accessToken": "eyJhbGci..."
}
```

你的team.json:
```json
[
  {
    "user": {
      "id": "user-abc123",
      "email": "admin@company.com"
    },
    "account": {
      "id": "def456",
      "organizationId": "org-xyz987"
    },
    "accessToken": "eyJhbGci...（完整复制）"
  }
]
```

---

## 📋 字段对照表

| 需要的字段 | 在网页JSON中的位置 |
|-----------|-------------------|
| user.id | `user` → `id` |
| user.email | `user` → `email` |
| account.id | `account` → `id` |
| account.organizationId | `account` → `organizationId` |
| accessToken | `accessToken` (最外层) |

---

## ✅ 检查清单

- [ ] config.toml 已修改密码
- [ ] team.json 已创建
- [ ] team.json 外面有 `[ ]`
- [ ] 所有字段都有引号 `""`
- [ ] accessToken 完整复制

---

## 🎯 Team名称

```
你的邮箱: admin@company.com
Team名: admin  ← 用这个

生成兑换码时:
python code_generator.py generate --team admin --count 10
                                        ↑
                                  用邮箱@前面的
```

---

详细说明: [CONFIG_GUIDE.md](CONFIG_GUIDE.md)
