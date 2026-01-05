#!/usr/bin/env python3
"""
测试accessToken是否有效
"""

import requests
import json
from pathlib import Path

def test_token():
    # 读取team.json
    team_file = Path(__file__).parent / "team.json"
    with open(team_file, "r", encoding="utf-8") as f:
        teams = json.load(f)

    if not teams:
        print("[错误] team.json为空")
        return

    team = teams[0]
    access_token = team.get("accessToken", "")
    account_id = team.get("account", {}).get("id", "")
    org_id = team.get("account", {}).get("organizationId", "")

    print(f"[信息] 正在测试token...")
    print(f"[信息] Account ID: {account_id}")
    print(f"[信息] Org ID: {org_id}")
    print(f"[信息] Token前缀: {access_token[:50]}...")
    print()

    # 测试获取订阅信息
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "authorization": f"Bearer {access_token}",
        "chatgpt-account-id": account_id,
        "content-type": "application/json",
        "origin": "https://chatgpt.com",
        "referer": "https://chatgpt.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="135", "Not)A;Brand";v="99", "Google Chrome";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
    }

    url = f"https://chatgpt.com/backend-api/subscriptions?account_id={account_id}"

    try:
        print(f"[测试] 发送请求到: {url}")
        response = requests.get(url, headers=headers, timeout=10)

        print(f"[结果] HTTP状态码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("[成功] Token有效!")
            print(f"[信息] 总席位: {data.get('seats_entitled', 0)}")
            print(f"[信息] 已使用: {data.get('seats_in_use', 0)}")
            print(f"[信息] 待处理邀请: {data.get('pending_invites', 0)}")
            print(f"[信息] 可用席位: {data.get('seats_entitled', 0) - data.get('seats_in_use', 0) - data.get('pending_invites', 0)}")
        elif response.status_code == 401:
            print("[失败] Token已过期或无效 (HTTP 401)")
            print("[提示] 请重新获取token:")
            print("  1. 访问 https://chatgpt.com 并登录")
            print("  2. 访问 https://chatgpt.com/api/auth/session")
            print("  3. 复制accessToken字段到team.json")
        else:
            print(f"[失败] 请求失败: HTTP {response.status_code}")
            print(f"[响应] {response.text[:200]}")

    except Exception as e:
        print(f"[错误] 请求异常: {e}")

if __name__ == "__main__":
    test_token()
