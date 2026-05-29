# -*- coding: utf-8 -*-
"""
基础接口测试脚本 (httpx 异步版本)
用于验证 lingxingapi_httpx 方案的可行性

使用方法:
    python test_basic_api_httpx.py <app_id> <app_secret>

测试接口:
    1. AccessToken - POST 获取授权令牌
    2. Marketplaces - GET 查询亚马逊市场列表
    3. Sellers - GET 查询亚马逊店铺列表
"""
import os
import sys
import asyncio
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

from lingxingapi_httpx import API, errors


def load_env(filepath: str = ".env") -> dict:
    """简易 .env 文件加载器"""
    env = {}
    if not os.path.isfile(filepath):
        return env
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def get_credentials() -> tuple[str, str]:
    """获取 API 凭证，优先级: 环境变量 > .env 文件 > 命令行参数"""
    app_id = os.environ.get("LINGXING_APP_ID")
    app_secret = os.environ.get("LINGXING_APP_SECRET")

    if not app_id or not app_secret:
        env = load_env()
        app_id = app_id or env.get("LINGXING_APP_ID")
        app_secret = app_secret or env.get("LINGXING_APP_SECRET")

    if not app_id or not app_secret:
        if len(sys.argv) >= 3:
            app_id = sys.argv[1]
            app_secret = sys.argv[2]

    if not app_id or not app_secret:
        print("用法: python test_basic_api_httpx.py <app_id> <app_secret>")
        print("或者设置环境变量 / .env 文件:")
        print("  LINGXING_APP_ID=your_app_id")
        print("  LINGXING_APP_SECRET=your_app_secret")
        sys.exit(1)

    return app_id, app_secret


def _create_api():
    """创建 API 客户端实例"""
    app_id, app_secret = get_credentials()
    return API(
        app_id=app_id,
        app_secret=app_secret,
        timeout=30,
        ignore_timeout=True,
        ignore_timeout_retry=3,
        ignore_api_limit=True,
        ignore_api_limit_retry=3,
    )


def test_access_token():
    """测试获取 AccessToken (POST 请求)"""
    print("\n" + "=" * 60)
    print("测试 1: AccessToken (POST)")
    print("=" * 60)

    async def _run():
        api = _create_api()
        async with api:
            return await api.AccessToken()

    try:
        token = asyncio.run(_run())
        print("[PASS] 获取 Token 成功")
        print(f"  access_token:  {token.access_token[:20]}...")
        print(f"  refresh_token: {token.refresh_token[:20]}...")
        print(f"  expires_in:    {token.expires_in} 秒")
        assert token.access_token
    except errors.BaseApiError as e:
        print(f"[FAIL] 获取 Token 失败: {e}")
        raise


def test_marketplaces():
    """测试查询亚马逊市场列表 (GET 请求)"""
    print("\n" + "=" * 60)
    print("测试 2: Marketplaces (GET)")
    print("=" * 60)

    async def _run():
        api = _create_api()
        async with api:
            return await api.basic.Marketplaces()

    try:
        result = asyncio.run(_run())
        print("[PASS] 查询市场列表成功")
        print(f"  返回数据量: {result.response_count}")
        print(f"  总数据量:   {result.total_count}")
        if result.data:
            mp = result.data[0]
            print("  第一条记录:")
            print(f"    mid={mp.mid}, country={mp.country}, country_code={mp.country_code}")
        assert result.code == 0
    except errors.BaseApiError as e:
        print(f"[FAIL] 查询市场列表失败: {e}")
        raise


def test_sellers():
    """测试查询亚马逊店铺列表 (GET 请求)"""
    print("\n" + "=" * 60)
    print("测试 3: Sellers (GET)")
    print("=" * 60)

    async def _run():
        api = _create_api()
        async with api:
            return await api.basic.Sellers()

    try:
        result = asyncio.run(_run())
        print("[PASS] 查询店铺列表成功")
        print(f"  返回数据量: {result.response_count}")
        print(f"  总数据量:   {result.total_count}")
        if result.data:
            seller = result.data[0]
            print("  第一条记录:")
            print(f"    sid={seller.sid}, seller_name={seller.seller_name}, status={seller.status}")
        assert result.code == 0
    except errors.BaseApiError as e:
        print(f"[FAIL] 查询店铺列表失败: {e}")
        raise


def main():
    app_id, app_secret = get_credentials()

    print("=" * 60)
    print("领星 API httpx 方案测试")
    print("=" * 60)
    print(f"app_id: {app_id[:10]}...")

    results = []
    try:
        test_access_token()
        results.append(("AccessToken", True))
    except Exception:
        results.append(("AccessToken", False))

    try:
        test_marketplaces()
        results.append(("Marketplaces", True))
    except Exception:
        results.append(("Marketplaces", False))

    try:
        test_sellers()
        results.append(("Sellers", True))
    except Exception:
        results.append(("Sellers", False))

    print("\n" + "=" * 60)
    print("测试汇总")
    print("=" * 60)
    for name, ok in results:
        status = "[PASS]" if ok else "[FAIL]"
        print(f"  {name}: {status}")

    all_pass = all(ok for _, ok in results)
    if all_pass:
        print("\n所有测试通过! httpx 方案可行。")
    else:
        print("\n部分测试失败, 请检查 app_id/app_secret 及网络配置。")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
