# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import Field, field_validator
from lingxingapi_httpx import utils
from lingxingapi_httpx.base.param import Parameter, PageOffestAndLength
from lingxingapi_httpx.fields import NonNegativeInt


# 多平台 - 店铺 ----------------------------------------------------------------------------------------------------------------
class MultiPlatformShops(PageOffestAndLength):
    # 平台code列表
    platform_code: Optional[list[int]] = None
    # 店铺同步状态 (1 启用, 0 停用)
    is_sync: Optional[int] = None
    # 店铺授权状态 (1 正常授权, 0 授权失败)
    status: Optional[int] = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("platform_code", mode="before")
    @classmethod
    def _validate_platform_code(cls, v) -> list[int] | None:
        if v is None:
            return None
        return utils.validate_array_of_int(v, "平台code platform_code")


# 多平台 - 平台订单 --------------------------------------------------------------------------------------------------------------
class PlatformOrders(Parameter):
    # 时间类型 (必填)
    # 0: 平台数据变动时间 1: 订购时间 2: 订购时间-北京 3: 支付时间 4: 支付时间-北京 5: 发货时间 6: 发货时间-北京
    date_type: int
    # 开始时间 (必填) 格式: 2025-10-22 00:00:01
    start_date: str
    # 结束时间 (必填) 格式: 2025-10-22 20:00:01
    end_date: str
    # 发货类型: 0-自发货 1-平台发货 2-部分自发货
    delivery_type_list: Optional[list[int]] = None
    # 查询起始位置
    page_num: Optional[int] = None
    # 分页大小
    page_size: Optional[int] = None
    # 平台CODE列表
    platform_code_list: Optional[list[str]] = None
    # 多个精确搜索查询值
    search_multi_value: Optional[list[str]] = None
    # 单个模糊搜索查询值
    search_single_value: Optional[str] = None
    # 搜索查询类型 (1: sku, 2: 品名, 3: msku, 4: 商品id, 5: 平台单号, 6: 参考号, 7: 商品标题)
    search_type: Optional[int] = None
    # 站点列表
    site_code_list: Optional[list[str]] = None
    # 排序字段 (purchaseTime, paymentTime, platformOrderModifiedTime, deliveryTime)
    sort_field: Optional[str] = None
    # 升降序 (asc, desc)
    sort_type: Optional[str] = None
    # 平台单状态编码列表
    status_list: Optional[list[str]] = None
    # 店铺唯一标识列表
    store_id_list: Optional[list[str]] = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("date_type", mode="before")
    @classmethod
    def _validate_date_type(cls, v) -> int:
        return utils.validate_int(v, "时间类型 date_type")

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v, info) -> str:
        dt = utils.validate_datetime(v, True, "查询日期 %s" % info.field_name)
        return "%04d-%02d-%02d %02d:%02d:%02d" % (
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
        )

    @field_validator("delivery_type_list", mode="before")
    @classmethod
    def _validate_delivery_type_list(cls, v) -> list[int] | None:
        if v is None:
            return None
        return utils.validate_array_of_int(v, "发货类型 delivery_type_list")

    @field_validator("platform_code_list", mode="before")
    @classmethod
    def _validate_platform_code_list(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_str(v, "平台CODE platform_code_list")

    @field_validator("site_code_list", mode="before")
    @classmethod
    def _validate_site_code_list(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_str(v, "站点列表 site_code_list")

    @field_validator("status_list", mode="before")
    @classmethod
    def _validate_status_list(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_str(v, "状态列表 status_list")

    @field_validator("store_id_list", mode="before")
    @classmethod
    def _validate_store_id_list(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_str(v, "店铺ID列表 store_id_list")

    @field_validator("search_multi_value", mode="before")
    @classmethod
    def _validate_search_multi_value(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_str(v, "搜索值 search_multi_value")


# 多平台 - 配对 ----------------------------------------------------------------------------------------------------------------
class MultiPlatformPairs(PageOffestAndLength):
    # MSKU列表
    msku: Optional[list[str]] = None
    # 本地SKU列表
    sku: Optional[list[str]] = None
    # 操作开始时间
    start_time: Optional[str] = None
    # 操作结束时间
    end_time: Optional[str] = None
    # 平台码列表
    platform_codes: Optional[list[str]] = None
    # 店铺id列表
    store_ids: Optional[list[str]] = None
    # 是否使用分页游标
    use_cursor: Optional[bool] = None
    # 游标id
    cursor_id: Optional[str] = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("msku", mode="before")
    @classmethod
    def _validate_msku(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_non_empty_str(v, "MSKU msku")

    @field_validator("sku", mode="before")
    @classmethod
    def _validate_sku(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_non_empty_str(v, "本地SKU sku")

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def _validate_time(cls, v, info) -> str | None:
        if v is None:
            return None
        dt = utils.validate_datetime(v, True, "操作时间 %s" % info.field_name)
        return "%04d-%02d-%02d %02d:%02d:%02d" % (
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
        )

    @field_validator("platform_codes", mode="before")
    @classmethod
    def _validate_platform_codes(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_str(v, "平台码 platform_codes")

    @field_validator("store_ids", mode="before")
    @classmethod
    def _validate_store_ids(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_str(v, "店铺ID store_ids")


# 多平台 - 订单管理 --------------------------------------------------------------------------------------------------------------
class MultiPlatformOrders(PageOffestAndLength):
    # 时间类型 (update_time, global_purchase_time, global_delivery_time, global_payment_time, delivery_time)
    date_type: Optional[str] = None
    # 开始时间, 时间戳格式【单位:秒】
    start_time: Optional[int] = None
    # 结束时间, 时间戳格式【单位:秒】
    end_time: Optional[int] = None
    # 店铺id列表
    store_id: Optional[list[str]] = None
    # 平台code列表
    platform_code: Optional[list[int]] = None
    # 平台单号列表
    platform_order_nos: Optional[list[str]] = None
    # 特定平台单号列表 (ebay/newegg/coupang/shopify/美客多/shopline)
    platform_order_names: Optional[list[str]] = None
    # 订单状态 (1 同步中, 2 已同步, 3 待付款, 4 待审核, 5 待发货, 6 已发货, 7 已取消/不发货, 8 不显示, 9 平台发货)
    order_status: Optional[int] = None
    # 平台单发货状态列表
    platform_shipping_status: Optional[list[str]] = None
    # 平台单支付状态列表
    platform_payment_status: Optional[list[str]] = None
    # 是否包含已删除订单
    include_delete: Optional[bool] = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("store_id", mode="before")
    @classmethod
    def _validate_store_id(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_str(v, "店铺ID store_id")

    @field_validator("platform_code", mode="before")
    @classmethod
    def _validate_platform_code(cls, v) -> list[int] | None:
        if v is None:
            return None
        return utils.validate_array_of_int(v, "平台code platform_code")

    @field_validator("platform_order_nos", mode="before")
    @classmethod
    def _validate_platform_order_nos(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_non_empty_str(v, "平台单号 platform_order_nos")

    @field_validator("platform_order_names", mode="before")
    @classmethod
    def _validate_platform_order_names(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_non_empty_str(v, "平台单号 platform_order_names")

    @field_validator("platform_shipping_status", mode="before")
    @classmethod
    def _validate_platform_shipping_status(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_str(v, "发货状态 platform_shipping_status")

    @field_validator("platform_payment_status", mode="before")
    @classmethod
    def _validate_platform_payment_status(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_str(v, "支付状态 platform_payment_status")
