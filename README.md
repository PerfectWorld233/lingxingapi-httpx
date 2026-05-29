<div align="center">

# lingxingapi-httpx

[![PyPI](https://img.shields.io/pypi/v/lingxingapi-httpx?style=flat-square)](https://pypi.org/project/lingxingapi-httpx/)
[![Python Version](https://img.shields.io/pypi/pyversions/lingxingapi-httpx?style=flat-square)](https://pypi.org/project/lingxingapi-httpx/)
[![License](https://img.shields.io/github/license/PerfectWorld233/lingxingapi-httpx?style=flat-square)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-black?style=flat-square)](https://github.com/psf/black)

领星 ERP 开放平台 API 客户端，基于 **httpx** 异步引擎实现。

</div>

---

## 目录

- [项目简介](#项目简介)
- [功能特性](#功能特性)
- [安装](#安装)
- [快速开始](#快速开始)
- [配置凭证](#配置凭证)
- [支持的 API 模块](#支持的-api-模块)
- [核心参数说明](#核心参数说明)
- [异常体系](#异常体系)
- [与官方 SDK 的差异](#与官方-sdk-的差异)
- [测试](#测试)
- [注意事项](#注意事项)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

---

## 项目简介

本项目是领星 ERP 官方 Python SDK 的现代化重构版本，将底层 HTTP 引擎从 `aiohttp` 替换为业界更主流的 `httpx`，完整保留了原始的签名算法、Token 自动刷新、错误重试等核心业务能力。

`httpx` 同时提供异步客户端（`AsyncClient`）与同步客户端（`Client`），本项目当前版本基于异步实现，充分发挥 Python `asyncio` 的高并发优势。如果你有同步调用需求，也可以基于 `httpx.Client` 自行封装同步接口。

---

## 功能特性

- **异步高性能**：基于 `httpx` 异步客户端（`AsyncClient`），充分利用 Python 异步特性，轻松应对高并发场景；`httpx` 也提供同步客户端（`Client`），同步封装逻辑完全通用
- **完整业务覆盖**：涵盖基础数据、销售、FBA、产品、采购、仓库、广告、财务、工具、亚马逊源数据等十大模块
- **自动鉴权**：`access_token` 与 `refresh_token` 在进程内自动缓存与刷新，多实例共享同一 Token
- **智能重试**：内置超时、限流、500 错误、网络断连等多场景自动重试机制，支持自定义重试策略
- **强类型校验**：基于 Pydantic 的请求参数与响应数据校验，减少运行时错误
- **完善异常体系**：十余种细粒度异常类型，便于精准捕获与处理各类 API 错误

---

## 安装

### 通过 PyPI 安装（推荐）

```bash
pip install lingxingapi-httpx
```

### 可选性能依赖

```bash
pip install orjson cytimes
```

### 从源码安装

```bash
git clone https://github.com/PerfectWorld233/lingxingapi-httpx.git
cd lingxingapi-httpx
pip install -e .
```

---

## 快速开始

- [httpx 异步版本](#httpx-异步版本)
- [httpx 同步说明](#httpx-同步说明)

### httpx 异步版本

```python
import asyncio
from lingxingapi_httpx import API

async def main():
    async with API(
        app_id="your_app_id",
        app_secret="your_app_secret",
        timeout=30,
        ignore_timeout=True,
        ignore_api_limit=True,
    ) as api:
        # 获取 Token
        token = await api.AccessToken()
        print(token.access_token)

        # 查询亚马逊市场列表
        mps = await api.basic.Marketplaces()
        for mp in mps.data:
            print(mp.country, mp.country_code)

        # 查询店铺列表
        sellers = await api.basic.Sellers()
        for seller in sellers.data:
            print(seller.seller_name, seller.status)

asyncio.run(main())
```

### httpx 同步说明

`httpx` 本身也支持同步客户端 `httpx.Client`。如果你不想使用 `async/await`，可以基于 `httpx.Client` 自行封装同步版本的领星 ERP API 调用：

```python
import httpx

with httpx.Client(timeout=30) as client:
    response = client.post(
        "https://openapi.lingxing.com/api/auth-server/oauth/token",
        data={...}
    )
    print(response.json())
```

同步封装的核心思路与异步版本完全一致：使用 `httpx.Client` 替代 `httpx.AsyncClient`，将 `async def` 改为普通 `def`，去掉 `await` 和 `async with` 即可。签名算法、Token 刷新、错误重试等逻辑完全通用。

---

## 配置凭证

### 方式一：.env 文件（推荐）

在项目根目录创建 `.env` 文件：

```ini
LINGXING_APP_ID=your_app_id
LINGXING_APP_SECRET=your_app_secret
```

### 方式二：环境变量

```bash
export LINGXING_APP_ID=your_app_id
export LINGXING_APP_SECRET=your_app_secret
```

### 方式三：代码中直接传入

```python
api = API(app_id="your_app_id", app_secret="your_app_secret")
```

---

## 支持的 API 模块

| 模块 | 命名空间 | 说明 |
|---|---|---|
| 授权 | `api.AccessToken()` / `api.RefreshToken()` | 获取与刷新访问令牌 |
| 基础数据 | `api.basic` | 市场、店铺、国家、汇率、账户信息 |
| 销售数据 | `api.sales` | Listing、订单、促销、刊登管理、自发货 |
| FBA 数据 | `api.fba` | STA 任务、货件、包装组、到货接收 |
| 产品数据 | `api.product` | 本地产品、SPU、捆绑产品、分类、品牌、标签 |
| 采购数据 | `api.purchase` | 供应商、采购方、采购计划 |
| 仓库数据 | `api.warehouse` | 仓库、仓位、FBA/AWD 库存、库存流水 |
| 广告数据 | `api.ads` | SP/SB/SD 广告基础数据与报表、DSP 报告 |
| 财务数据 | `api.finance` | 结算、交易、利润报表、库存分类账、广告发票 |
| 工具数据 | `api.tools` | 关键词监控、竞品监控 |
| 亚马逊源数据 | `api.source` | 源报表订单、库存、移除货件、报告导出 |

---

## 核心参数说明

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `app_id` | `str` | 必填 | 领星 ERP 开放平台应用 ID |
| `app_secret` | `str` | 必填 | 领星 ERP 开放平台应用密钥 |
| `timeout` | `int / float` | `60` | 请求超时（秒） |
| `ignore_timeout` | `bool` | `False` | 超时时是否自动重试 |
| `ignore_timeout_wait` | `int / float` | `1` | 超时重试等待间隔（秒） |
| `ignore_timeout_retry` | `int` | `10` | 超时最大重试次数，`-1` 为无限 |
| `ignore_api_limit` | `bool` | `False` | 限流时是否自动重试 |
| `ignore_api_limit_wait` | `int / float` | `1` | 限流重试等待间隔（秒） |
| `ignore_api_limit_retry` | `int` | `10` | 限流最大重试次数，`-1` 为无限 |
| `ignore_internal_server_error` | `bool` | `False` | 500 错误时是否自动重试 |
| `ignore_internal_server_error_wait` | `int / float` | `1` | 500 错误重试等待间隔（秒） |
| `ignore_internal_server_error_retry` | `int` | `10` | 500 错误最大重试次数，`-1` 为无限 |
| `ignore_internet_connection` | `bool` | `False` | 网络断开时是否自动重试 |
| `ignore_internet_connection_wait` | `int / float` | `1` | 网络断连重试等待间隔（秒） |
| `ignore_internet_connection_retry` | `int` | `10` | 网络断连最大重试次数，`-1` 为无限 |
| `max_tcp_connections` | `int` | `100` | 最大 TCP 连接数 |

---

## 异常体系

所有异常均继承自 `BaseApiError`，可按需捕获：

| 异常类 | 触发场景 |
|---|---|
| `ApiSettingsError` | 初始化参数非法 |
| `InternetConnectionError` | 无法连接互联网 |
| `ApiTimeoutError` | 请求超时 |
| `InternalServerError` | 领星 ERP 服务器 500 错误 |
| `AccessTokenExpiredError` | `access_token` 过期 |
| `RefreshTokenExpiredError` | `refresh_token` 过期 |
| `SignatureExpiredError` | 签名过期 |
| `TooManyRequestsError` / `ApiLimitError` | 请求被限流 |
| `AppIdOrSecretError` | `app_id` 或 `app_secret` 不正确 |
| `InvalidParametersError` | 请求参数非法 |
| `UnknownRequestError` | 未知错误 |

---

## 与官方 SDK 的差异

| 特性 | 官方 SDK (`aiohttp`) | 本项目 (`httpx`) |
|---|---|---|
| 异步 / 同步 | 仅异步 | 异步（`httpx` 原生支持同步扩展） |
| HTTP 引擎 | `aiohttp` | `httpx.AsyncClient` / `httpx.Client` |
| 上下文管理器 | `async with` | `async with` / `with` |
| 签名算法 | AES-ECB + MD5 + Base64 | 完全一致 |
| Token 自动刷新 | 支持 | 支持 |
| 限流 / 超时重试 | 支持 | 支持 |
| User-Agent | `python-requests/2.31.0` | 无（避免 WAF 拦截） |

---

## 测试

### 运行全部测试

```bash
# httpx 异步版本
python test_basic_api_httpx.py
```

### pytest 单测

已兼容 pytest，可在 PyCharm 中右键单独运行某个测试：

```bash
pytest test_basic_api_httpx.py::test_access_token -v
pytest test_basic_api_httpx.py::test_marketplaces -v
pytest test_basic_api_httpx.py::test_sellers -v
```

### 签名一致性验证

```bash
python test_signature_httpx.py
```

---

## 注意事项

1. **IP 白名单**：领星 ERP 开放平台要求将调用方的出口 IP 加入 API 白名单，否则可能返回 403。
2. **Token 复用**：`access_token` 和 `refresh_token` 在进程内自动缓存，多个 API 实例共享同一 Token。
3. **会话关闭**：httpx / requests 的会话在 `async with` / `with` 退出时自动关闭，建议始终使用上下文管理器。
4. **.env 安全**：`.env` 文件包含敏感信息，请勿提交到 Git 仓库。建议将 `.env` 加入 `.gitignore`。

---

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

请确保你的代码通过现有测试，并在必要时补充新的测试用例。

---

## 许可证

本项目为领星 ERP 官方 SDK 的翻译/改写版本，仅供学习和内部使用。
