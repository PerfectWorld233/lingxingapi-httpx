# -*- coding: utf-8 -*-c
import datetime
from decimal import Decimal
from lingxingapi_httpx import errors
from lingxingapi_httpx.base.api import BaseAPI
from lingxingapi_httpx.base import schema as base_schema
from lingxingapi_httpx.basic import param, route, schema


# API ------------------------------------------------------------------------------------------------------------------
class BasicAPI(BaseAPI):
    """领星API `基础数据` 接口

    ## Notice
    请勿直接实例化此类
    """

    # 公共 API --------------------------------------------------------------------------------------
    # . 基础数据
    async def Marketplaces(self) -> schema.Marketplaces:
        """查询所有的亚马逊站点信息

        ## Docs
        - 基础数据: [查询亚马逊市场列表](https://apidoc.lingxing.com/#/docs/BasicData/AllMarketplace)

        :returns `<'Marketplaces'>`: 返回所有的亚马逊站点信息
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 领星站点ID [唯一标识]
                    "mid": 1,
                    # 站点区域
                    "region": "NA",
                    # 站点亚马逊仓库所属区域 [原字段 'aws_region']
                    "region_aws": "NA",
                    # 站点国家 (中文)
                    "country": "美国",
                    # 站点国家代码 [原字段 'code']
                    "country_code": "US",
                    # 亚马逊市场ID
                    "marketplace_id": "ATVPDKIKX0DER"
                },
                ...
            ],
        }
        """
        data = await self._request_with_sign("GET", route.MARKETPLACES)
        return schema.Marketplaces.model_validate(data)

    async def States(self, country_code: str) -> schema.States:
        """查询亚马逊指定国家的周/省信息

        ## Docs
        - 基础数据: [查询亚马逊国家下地区列表](https://apidoc.lingxing.com/#/docs/BasicData/WorldStateLists)

        :param country_code `<'str'>`: 国家代码, 如: `"US"`
        :returns `<'States'>`: 返回指定国家的省/州信息
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 国家代码
                    "country_code": "US",
                    # 省/州名称 [原字段 'state_or_province_name']
                    "state": "California",
                    # 省/州代码 # [原字段 'code']
                    "state_code": "CA"
                },
                ...
            ],
        }
        ```
        """
        url = route.STATES
        # 解析并验证参数
        args = {"country_code": country_code}
        try:
            p = param.CountryCode.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err
        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.States.model_validate(data)

    async def Sellers(self) -> schema.Sellers:
        """查询已授权到领星 ERP 全部的亚马逊店铺信息

        ## Docs
        - 基础数据: [查询亚马逊店铺列表](https://apidoc.lingxing.com/#/docs/BasicData/SellerLists)

        :returns `<'Sellers'>`: 返回已授权到领星 ERP 全部的亚马逊店铺信息
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 领星站点ID (Marketplace.mid)
                    "mid": 1,
                    # 领星店铺ID [唯一标识]
                    "sid": 1,
                    # 亚马逊卖家ID
                    "seller_id": "AZTOL********",
                    # 领星店铺名称 (含国家信息) [原字段 'name']
                    "seller_name": "account**-ES",
                    # 领星店铺帐号ID [原字段 'seller_account_id']
                    "account_id": 1,
                    # 领星店铺帐号名称
                    "account_name": "account**",
                    # 亚马逊市场ID (Marketplace.marketplace_id)
                    "marketplace_id": "ATVPDKIKX0DER",
                    # 店铺区域
                    "region": "EU",
                    # 店铺国家 (中文)
                    "country": "西班牙",
                    # 店铺状态 (0: 停止同步, 1: 正常, 2: 授权异常, 3: 欠费停服)
                    "status": 1
                    # 店铺是否授权广告 (0: 否, 1: 是) [原字段 'has_ads_setting']
                    "ads_authorized": 0,
                },
                ...
            ],
        }
        ```
        """
        data = await self._request_with_sign("GET", route.SELLERS)
        return schema.Sellers.model_validate(data)

    async def ConceptSellers(self) -> schema.ConceptSellers:
        """查询全部的亚马逊概念店铺信息

        ## Docs
        - 基础数据: [查询亚马逊概念店铺列表](https://apidoc.lingxing.com/#/docs/BasicData/ConceptSellerLists)

        :returns `<'ConceptSellers'>`: 返回全部的亚马逊概念店铺信息
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 领星概念站点ID [原字段 'mid']
                    "cmid": 10*****,
                    # 领星概念店铺ID [唯一标识, 原字段 'id']
                    "csid": 1222**************,
                    # 亚马逊卖家ID
                    "seller_id": "AZTOL********",
                    # 领星概念店铺名称 (含区域信息)
                    "seller_name": "account**-EU",
                    # 领星概念店铺账号ID [原字段 'seller_account_id']
                    "account_id": 1,
                    # 领星概念店铺帐号名称 [原字段 'seller_account_name']
                    "account_name": "account**",
                    # 概念店铺区域
                    "region": "EU",
                    # 概念店铺国家, 如: "北美共享", "欧洲共享"
                    "country": "欧洲共享",
                    # 概念店铺状态 (1: 启用, 2: 停用)
                    "status": 1
                },
                ...
            ],
        }
        """
        data = await self._request_with_sign("GET", route.CONCEPT_SELLERS)
        return schema.ConceptSellers.model_validate(data)

    async def RenameSellers(self, *rename: dict) -> schema.RenameSellersResult:
        """批量修改领星店铺名称

        ## Docs
        - 基础数据: [批量修改店铺名称](https://apidoc.lingxing.com/#/docs/BasicData/SellerBatchRename)

        :param *rename `<'dict'>`: 支持最多10个店铺名称的批量修改

            - 每个字典必须包含 `sid` 和 `name` 字段, 如:
              `{"sid": 1, "name": "account-ES"}`
            - 必填字段 `sid` 领星店铺ID, 必须是 int 类型, 参数来源: `Seller.sid`
            - 必填字段 `name` 新的店铺名称, 必须是 str 类型

        :returns `<'RenameSellerResult'>`: 返回批量修改的结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应结果
            "data": {
                # 修改成功数量 [原字段 'success_num']
                "success": 1,
                # 修改失败数量 [原字段 'failure_num']
                "failure": 1,
                # 修改失败详情
                "failure_detail": [
                    {
                        # 领星店铺ID (Seller.sid)
                        "sid": 1,
                        # 新店铺名称
                        "name": "account-ES",
                        # 失败信息 [原字段 'error']
                        "message": "新旧店铺名相同",
                    },
                    ...
                ],
            },
        }
        ```
        """
        url = route.RENAME_SELLERS
        # 解析并验证参数
        args = {"renames": rename}
        try:
            p = param.RenameSellers.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.RenameSellersResult.model_validate(data)

    async def Accounts(self) -> schema.Accounts:
        """查询所有领星的ERP账号信息

        ## Docs
        - 基础数据: [查询ERP用户信息列表](https://apidoc.lingxing.com/#/docs/BasicData/AccoutLists)

        :returns `<'Accounts'>`: 返回所有领星的ERP账号信息
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 领星账号所从属的ID (如主帐号ID) [原字段 'zid']
                    "parent_id": 1,
                    # 领星帐号ID [唯一标识] [原字段 'uid']
                    "user_id": 1,
                    # 是否为主账号 (0: 否, 1: 是)
                    "is_master": 1
                    # 帐号角色
                    "role": "",
                    # 领星帐号显示的姓名 [原字段 'realname']
                    "display_name": "超级管理员",
                    # 领星帐号登陆用户名
                    "username": "user****",
                    # 领星帐号电子邮箱
                    "email": "15*******@qq.com",
                    # 领星帐号电话号码 [原字段 'mobile']
                    "phone": "15********",
                    # 领星帐号创建时间 (北京时间)
                    "create_time": "2024-07-12 19:07",
                    # 领星帐号最后登录时间 (北京时间)
                    "last_login_time": "2024-07-12 19:07",
                    # 领星帐号最后登录IP
                    "last_login_ip": "",
                    # 领星帐号登录次数 [原字段 'login_num']
                    "login_count": 1
                    # 领星帐号状态 (0: 禁用, 1: 正常)
                    "status": 1,
                    # 关联的领星店铺名称, 逗号分隔 [原字段 'seller']
                    "sellers": "acc**1,acc**2",
                },
                ...
            ],
        }
        ```
        """
        data = await self._request_with_sign("GET", route.ACCOUNTS)
        return schema.Accounts.model_validate(data)

    async def ExchangeRates(
        self,
        date: str | datetime.date | datetime.datetime | None = None,
    ) -> schema.ExchangeRates:
        """查询指定月份的汇率信息

        ## Docs
        - 基础数据: [查询汇率](https://apidoc.lingxing.com/#/docs/BasicData/Currency)

        :param date `<'str/date/datetime'>`: 指定查询的月份, 默认 `None` (当前月份)

            - 如果是字符串, 必须是有效的日期字符串, 如: `"2025-07"`, `"2025-07-01"`
            - 如果是 `date` 或 `datetime` 对象, 将自动转换为 `YYYY-MM` 格式
            - 如果为 `None`, 则使用当前月份作为参数

        :returns `<'ExchangeRates'>`: 返回指定月份的汇率信息
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 汇率日期 (格式: YYYY-MM-DD)
                    "date": "2025-01-01",
                    # 货币名称 (中文) [原字段 'name']
                    "currency": "美元",
                    # 货币代码 [原字段 'code']
                    "currency_code": "USD",
                    # 货币符号 [原字段 'icon']
                    "currency_icon": "$",
                    # 中国银行官方汇率 (对比人民币) [原字段 'rate_org']
                    "boc_rate": "7.1698",
                    # 用户汇率 (对比人民币) [原字段 'my_rate']
                    "user_rate": "7.1315",
                    # 用户汇率修改时间 (北京时间)
                    "update_time": "2025-03-10 17:14:10",
                },
                ...
            ],
        }
        ```
        """
        url = route.EXCHANGE_RATES
        # 解析并验证参数
        args = {"date": date}
        try:
            p = param.ExchangeRateDate.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body={"date": p.date})
        return schema.ExchangeRates.model_validate(data)

    async def EditExchangeRate(
        self,
        date: str | datetime.date | datetime.datetime,
        currency_code: str,
        user_rate: str | float | Decimal,
    ) -> base_schema.ResponseResult:
        """修改指定月份的用户汇率

        ## Docs
        - 基础数据: [修改我的汇率](https://apidoc.lingxing.com/#/docs/BasicData/ExchangeRateUpdate)

        :param date `<'str/date/datetime'>`: 指定要修改的汇率月份

            - 如果是字符串, 必须是有效的日期字符串, 如: `"2025-07"`, `"2025-07-01"`
            - 如果是 `date` 或 `datetime` 对象, 将自动转换为 `YYYY-MM` 格式

        :param currency_code `<'str'>`: 指定的货币代码, 如: `"USD"`
        :param user_rate `<'str/float/Decimal'>`: 用户自定义汇率, 对比人民币,
            如: `"7.2008000000"`, 最多支持10位小数
        :returns `<'ResponseResult'>`: 返回修改结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 编辑结果
            "data": None
        }
        ```
        """
        url = route.EDIT_EXCHANGE_RATE
        # 解析并验证参数
        args = {
            "date": date,
            "currency_code": currency_code,
            "user_rate": user_rate,
        }
        try:
            p = param.EditExchangeRate.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return base_schema.ResponseResult.model_validate(data)
