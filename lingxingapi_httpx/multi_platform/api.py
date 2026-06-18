# -*- coding: utf-8 -*-c
import datetime
from lingxingapi_httpx import errors
from lingxingapi_httpx.base.api import BaseAPI
from lingxingapi_httpx.multi_platform import param, route, schema


# API ------------------------------------------------------------------------------------------------------------------
class MultiPlatformAPI(BaseAPI):
    """领星API `多平台` 接口

    ## Notice
    请勿直接实例化此类
    """

    # 多平台 - 店铺 ---------------------------------------------------------------------------------------------------------------
    async def Shops(
        self,
        offset: int | None = None,
        length: int | None = None,
        *,
        platform_code: int | list[int] | None = None,
        is_sync: int | None = None,
        status: int | None = None,
    ) -> schema.MultiPlatformShops:
        """查询多平台店铺信息

        ## Docs
        - 多平台: [查询多平台店铺信息](https://apidoc.lingxing.com/#/docs/MultiPlatform/V2/StoreInfoV2)

        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 上限200, 默认 `None` (使用: 200)
        :param platform_code `<'int/list[int]'>`: 平台code列表, 默认 `None`

            - `10001` AMAZON
            - `10002` Shopify
            - `10003` eBay
            - `10004` Wish
            - `10005` AliExpress
            - `10006` Shopee
            - `10007` Lazada
            - `10008` Walmart
            - `10009` 自定义平台
            - `10010` Wayfair
            - `10011` TikTok
            - `10012` MERCADO
            - `10013` CDISCOUNT
            - `10014` NEWEGG
            - `10015` RAKUTEN
            - `10016` SHOPLINE
            - `10017` TEAPPLIX
            - `10018` SHOPLAZZA
            - `10019` UEESHOP
            - `10020` COUPANG
            - `10021` SHEIN
            - `10022` Temu全托管
            - `10024` Temu半托管
            - `10025` OTTO
            - `10026` OZON
            - `10027` SHEIN全托管
            - `10028` SHEIN半托管
            - `10029` AliExpress半托管
            - `10030` AliExpress全托管
            - `10033` Qoo10
            - `10035` Amazon VC
            - `10038` line shopping
            - `10039` SPS Commerce

        :param is_sync `<'int'>`: 店铺同步状态, 默认 `None`

            - `1`: 启用
            - `0`: 停用

        :param status `<'int'>`: 店铺授权状态, 默认 `None`

            - `1`: 正常授权
            - `0`: 授权失败

        :returns `<'MultiPlatformShops'>`: 返回多平台店铺信息列表
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "fa58d84e-c843-4616-9fff-9b4065964465.1721704107513",
            # 响应时间
            "response_time": "2024-07-23 11:08:27",
            # 响应数据量
            "response_count": 1,
            # 总数据量
            "total_count": 1,
            # 响应数据
            "data": [
                {
                    # 店铺ID
                    "store_id": "1108413237731xxxx",
                    # 店铺id【对应获取亚马逊店铺接口sid】
                    "sid": "",
                    # 店铺名称
                    "store_name": "Walmart测试店铺",
                    # 平台code
                    "platform_code": "10008",
                    # 平台名称
                    "platform_name": "Walmart",
                    # 店铺币种
                    "currency": "USD",
                    # 店铺同步状态 (1 启用, 0 停用)
                    "is_sync": 1,
                    # 店铺授权状态 (1 正常授权, 0 授权失败)
                    "status": 0,
                },
                ...
            ],
        }
        ```
        """
        url = route.SHOPS
        # 解析并验证参数
        args = {
            "offset": offset,
            "length": length,
            "platform_code": platform_code,
            "is_sync": is_sync,
            "status": status,
        }
        try:
            p = param.MultiPlatformShops.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.MultiPlatformShops.model_validate(data)

    # 多平台 - 平台订单 -------------------------------------------------------------------------------------------------------------
    async def PlatformOrders(
        self,
        date_type: int,
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        *,
        delivery_type_list: int | list[int] | None = None,
        page_num: int | None = None,
        page_size: int | None = None,
        platform_code_list: str | list[str] | None = None,
        search_multi_value: str | list[str] | None = None,
        search_single_value: str | None = None,
        search_type: int | None = None,
        site_code_list: str | list[str] | None = None,
        sort_field: str | None = None,
        sort_type: str | None = None,
        status_list: str | list[str] | None = None,
        store_id_list: str | list[str] | None = None,
    ) -> schema.PlatformOrders:
        """查询平台订单列表

        ## Docs
        - 多平台: [查询平台订单列表](https://apidoc.lingxing.com/#/docs/MultiPlatform/V2/newPlatformOrderList)

        :param date_type `<'int'>`: 时间类型 (必填)

            - `0`: 平台数据变动时间
            - `1`: 订购时间
            - `2`: 订购时间-北京
            - `3`: 支付时间
            - `4`: 支付时间-北京
            - `5`: 发货时间
            - `6`: 发货时间-北京

        :param start_date `<'str/date/datetime'>`: 开始时间, 闭区间, 格式: `"2025-10-22 00:00:01"`
        :param end_date `<'str/date/datetime'>`: 结束时间, 闭区间, 格式: `"2025-10-22 20:00:01"`
        :param delivery_type_list `<'int/list[int]'>`: 发货类型, 默认 `None`

            - `0`: 自发货
            - `1`: 平台发货
            - `2`: 部分自发货

        :param page_num `<'int'>`: 查询起始位置, 默认 `None`
        :param page_size `<'int'>`: 分页大小, 默认 `None`
        :param platform_code_list `<'str/list[str]'>`: 平台CODE列表, 默认 `None`
        :param search_multi_value `<'str/list[str]'>`: 多个精确搜索查询值, 默认 `None`
        :param search_single_value `<'str'>`: 单个模糊搜索查询值, 默认 `None`
        :param search_type `<'int'>`: 搜索查询类型, 默认 `None`

            - `1`: sku
            - `2`: 品名
            - `3`: msku
            - `4`: 商品id
            - `5`: 平台单号
            - `6`: 参考号
            - `7`: 商品标题

        :param site_code_list `<'str/list[str]'>`: 站点列表, 默认 `None`
        :param sort_field `<'str'>`: 排序字段, 默认 `None`

            - `purchaseTime`
            - `paymentTime`
            - `platformOrderModifiedTime`
            - `deliveryTime`

        :param sort_type `<'str'>`: 升降序, 默认 `None`

            - `asc`
            - `desc`

        :param status_list `<'str/list[str]'>`: 平台单状态编码列表, 默认 `None`
        :param store_id_list `<'str/list[str]'>`: 店铺唯一标识列表, 默认 `None`
        :returns `<'PlatformOrders'>`: 返回平台订单列表
        """
        url = route.PLATFORM_ORDERS
        # 解析并验证参数
        args = {
            "date_type": date_type,
            "start_date": start_date,
            "end_date": end_date,
            "delivery_type_list": delivery_type_list,
            "page_num": page_num,
            "page_size": page_size,
            "platform_code_list": platform_code_list,
            "search_multi_value": search_multi_value,
            "search_single_value": search_single_value,
            "search_type": search_type,
            "site_code_list": site_code_list,
            "sort_field": sort_field,
            "sort_type": sort_type,
            "status_list": status_list,
            "store_id_list": store_id_list,
        }
        try:
            p = param.PlatformOrders.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.PlatformOrders.model_validate(data)

    # 多平台 - 配对 ---------------------------------------------------------------------------------------------------------------
    async def Pairs(
        self,
        offset: int | None = None,
        length: int | None = None,
        *,
        msku: str | list[str] | None = None,
        sku: str | list[str] | None = None,
        start_time: str | datetime.date | datetime.datetime | None = None,
        end_time: str | datetime.date | datetime.datetime | None = None,
        platform_codes: str | list[str] | None = None,
        store_ids: str | list[str] | None = None,
        use_cursor: bool | None = None,
        cursor_id: str | None = None,
    ) -> schema.MultiPlatformPairs:
        """查询多平台配对列表

        ## Docs
        - 多平台: [查询多平台配对列表](https://apidoc.lingxing.com/#/docs/MultiPlatform/V2/PairListV2)

        获取多平台系统中【产品】>【配对列表】中数据已配对的数据。
        该模块数据为多平台MSKU与本地SKU的配对关系。

        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页条数, 默认 `None` (使用: 20)
        :param msku `<'str/list[str]'>`: MSKU列表, 默认 `None`
        :param sku `<'str/list[str]'>`: 本地SKU列表, 默认 `None`
        :param start_time `<'str/date/datetime'>`: 操作开始时间, 闭区间, 默认 `None`
        :param end_time `<'str/date/datetime'>`: 操作结束时间, 开区间, 默认 `None`
        :param platform_codes `<'str/list[str]'>`: 平台码列表, 默认 `None`
        :param store_ids `<'str/list[str]'>`: 店铺id列表, 默认 `None`
        :param use_cursor `<'bool'>`: 是否使用分页游标, 默认 `None` (使用: False)

            - 如配对数据多时, 强烈建议您使用分页游标的方式分页, 可加快接口响应速度

        :param cursor_id `<'str'>`: 游标id, 当use_cursor为True时必填, 默认 `None`
        :returns `<'MultiPlatformPairs'>`: 返回多平台配对列表
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "1e76129e-c622-420f-852e-08262755cfcc.1721705863164",
            # 响应时间
            "response_time": "2024-07-23 11:37:43",
            # 响应数据量
            "response_count": 1,
            # 总数据量
            "total_count": 1,
            # 响应数据
            "data": [
                {
                    # 店铺ID
                    "store_id": "11084135313207808",
                    # 店铺名称
                    "store_name": "eBay店铺1号",
                    # 平台码
                    "platform_code": "10003",
                    # 平台名称
                    "platform_name": "eBay",
                    # MSKU
                    "msku": "custom001",
                    # 本地SKU
                    "sku": "Book-A4-60",
                    # 本地SKU品名
                    "local_name": "2-白色-M",
                    # 操作时间
                    "modify_time": "2021-06-24 22:09:43",
                },
                ...
            ],
        }
        ```
        """
        url = route.PAIRS
        # 解析并验证参数
        args = {
            "offset": offset,
            "length": length,
            "msku": msku,
            "sku": sku,
            "start_time": start_time,
            "end_time": end_time,
            "platform_codes": platform_codes,
            "store_ids": store_ids,
            "use_cursor": use_cursor,
            "cursor_id": cursor_id,
        }
        try:
            p = param.MultiPlatformPairs.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.MultiPlatformPairs.model_validate(data)

    # 多平台 - 订单管理 -------------------------------------------------------------------------------------------------------------
    async def Orders(
        self,
        offset: int,
        length: int,
        *,
        date_type: str | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        store_id: str | list[str] | None = None,
        platform_code: int | list[int] | None = None,
        platform_order_nos: str | list[str] | None = None,
        platform_order_names: str | list[str] | None = None,
        order_status: int | None = None,
        platform_shipping_status: str | list[str] | None = None,
        platform_payment_status: str | list[str] | None = None,
        include_delete: bool | None = None,
    ) -> schema.MultiPlatformOrders:
        """查询订单管理订单列表

        ## Docs
        - 多平台: [查询订单管理订单列表](https://apidoc.lingxing.com/#/docs/MultiPlatform/V2/MultiPlatOrderV2)

        数据对应多平台管理系统中【订单】>【订单管理】的订单数据, 涵盖所有平台自发货订单数据。
        该接口查询到的订单可修改, 可能会与原始销售订单数据有差异。

        :param offset `<'int'>`: 分页偏移量 (必填)
        :param length `<'int'>`: 分页长度, 上限500 (必填)
        :param date_type `<'str'>`: 时间类型, 默认 `None`

            - `update_time`: 更新时间
            - `global_purchase_time`: 订购时间
            - `global_delivery_time`: 发货时间
            - `global_payment_time`: 付款时间
            - `delivery_time`: 平台发货时间

        :param start_time `<'int'>`: 开始时间, 时间戳格式【单位:秒】, 双开区间, 默认 `None`
        :param end_time `<'int'>`: 结束时间, 时间戳格式【单位:秒】, 双开区间, 默认 `None`
        :param store_id `<'str/list[str]'>`: 店铺id列表, 默认 `None`
        :param platform_code `<'int/list[int]'>`: 平台code列表, 默认 `None`
        :param platform_order_nos `<'str/list[str]'>`: 平台单号列表, 默认 `None`

            - 以下平台不可用, 需要用 platform_order_names 查询:
              10003-ebay, 10014-newegg, 10020-coupang, 10002-shopify,
              10012-美客多, 10016-shopline

        :param platform_order_names `<'str/list[str]'>`: 特定平台单号列表, 默认 `None`

            - 10003-ebay, 10014-newegg, 10020-coupang, 10002-shopify,
              10012-美客多, 10016-shopline 使用该字段查询

        :param order_status `<'int'>`: 订单状态, 默认 `None`

            - `1`: 同步中
            - `2`: 已同步
            - `3`: 待付款
            - `4`: 待审核
            - `5`: 待发货
            - `6`: 已发货
            - `7`: 已取消/不发货
            - `8`: 不显示
            - `9`: 平台发货

        :param platform_shipping_status `<'str/list[str]'>`: 平台单发货状态列表, 默认 `None`
        :param platform_payment_status `<'str/list[str]'>`: 平台单支付状态列表, 默认 `None`
        :param include_delete `<'bool'>`: 是否包含已删除订单, 默认 `None` (使用: False)
        :returns `<'MultiPlatformOrders'>`: 返回订单管理订单列表
        """
        url = route.ORDERS
        # 解析并验证参数
        args = {
            "offset": offset,
            "length": length,
            "date_type": date_type,
            "start_time": start_time,
            "end_time": end_time,
            "store_id": store_id,
            "platform_code": platform_code,
            "platform_order_nos": platform_order_nos,
            "platform_order_names": platform_order_names,
            "order_status": order_status,
            "platform_shipping_status": platform_shipping_status,
            "platform_payment_status": platform_payment_status,
            "include_delete": include_delete,
        }
        try:
            p = param.MultiPlatformOrders.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.MultiPlatformOrders.model_validate(data)
