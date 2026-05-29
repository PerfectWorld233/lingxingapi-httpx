# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import ValidationInfo, Field, field_validator
from lingxingapi_httpx import utils
from lingxingapi_httpx.fields import NonEmptyStr, NonNegativeInt
from lingxingapi_httpx.base.param import Parameter, PageOffestAndLength


# 店铺共享参数 --------------------------------------------------------------------------------------------------------------------
class Seller(PageOffestAndLength):
    """店铺共享参数"""

    # 领星店铺ID
    sid: NonNegativeInt


# 订单数据 -----------------------------------------------------------------------------------------------------------------------
# . Orders
class Orders(Seller):
    # 开始日期
    start_date: str
    # 结束日期
    end_date: str
    # 日期类型 (1: 下单日期, 2: 亚马逊订单更新时间 | 默认: 1)
    date_type: Optional[NonNegativeInt] = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v: str, info: ValidationInfo) -> str:
        dt = utils.validate_datetime(v, False, "订单数据日期 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)


# . FBA Shipments
class FbaShipments(Seller):
    """查询 FBA 发货订单参数"""

    # 发货开始时间 (本地时间), 时间间隔不超过7天
    start_time: str = Field(alias="shipment_date_after")
    # 发货结束时间 (本地时间), 时间间隔不超过7天
    end_time: str = Field(alias="shipment_date_before")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def _validate_time(cls, v: str, info: ValidationInfo) -> str:
        dt = utils.validate_datetime(v, False, "FBA发货订单时间 %s" % info.field_name)
        # fmt: off
        return "%04d-%02d-%02d %02d:%02d:%02d" % (
            dt.year, dt.month, dt.day,
            dt.hour, dt.minute, dt.second,
        )
        # fmt: on


# FBA 库存数据 -------------------------------------------------------------------------------------------------------------------
# . FBA Removal Orders
class FbaRemovalOrders(Orders):
    """查询 FBA 移除订单参数"""

    # 日期类型 ('update_date', 'request_date' | 默认: 'update_date')
    date_type: str = Field(alias="search_field_time")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("date_type", mode="before")
    @classmethod
    def _validate_date_type(cls, v) -> str:
        return "last_updated_date" if v == "update_date" else v


# . FBA Removal Shipments
class FbaRemovalShipments(Orders):
    """查询 FBA 移除货件参数"""

    # 领星店铺ID
    sid: Optional[NonNegativeInt] = None
    # 亚马逊卖家ID
    seller_id: Optional[str] = None


# . FBA Inventory Adjustments
class FbaInventoryAdjustments(PageOffestAndLength):
    """查询 FBA 库存调整参数"""

    # 开始日期
    start_date: str
    # 结束日期
    end_date: str
    # 领星店铺IDs (多个用逗号分隔)
    sids: Optional[str] = None
    # 搜索字段 ('asin', 'msku', 'fnsku', 'title', 'transaction_item_id')
    search_field: Optional[NonEmptyStr] = None
    # 搜索值
    search_value: Optional[NonEmptyStr] = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v: str, info: ValidationInfo) -> str:
        dt = utils.validate_datetime(v, False, "FBA库存调整日期 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)

    @field_validator("sids", mode="before")
    @classmethod
    def _validate_sids(cls, v) -> str | None:
        if v is None:
            return v
        sids = utils.validate_array_of_unsigned_int(v, "领星店铺IDs")
        return ",".join(map(str, sids))

    @field_validator("search_field", mode="before")
    @classmethod
    def _validate_search_field(cls, v) -> str | None:
        if v is None:
            return v
        if v == "title":
            return "item_name"
        return v


# 报告导出 -----------------------------------------------------------------------------------------------------------------------
# . Export Report Task
class ExportReportTask(Parameter):
    """创建报告导出任务参数"""

    # 亚马逊店铺ID (Seller.seller_id)
    seller_id: NonEmptyStr
    # 亚马逊市场ID列表 (Seller.marketplace_id)
    marketplace_ids: list[NonEmptyStr]
    # 店铺所在区域
    region: NonEmptyStr
    # 报告类型 具体参考亚马逊官方文档: https://developer-docs.amazon.com/sp-api/docs/report-type-values
    report_type: NonEmptyStr
    # 报告开始时间 (UTC时间, 例: '2023-01-01T00:00:00+00:00')
    start_time: Optional[str] = None
    # 报告结束时间 (UTC时间, 例: '2023-01-31T23:59:59+00:00')
    end_time: Optional[str] = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("marketplace_ids", mode="before")
    @classmethod
    def _validate_marketplace_ids(cls, v: str) -> str:
        return utils.validate_array_of_non_empty_str(v, "亚马逊市场IDs")

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def _validate_utc_time(cls, v: str, info: ValidationInfo) -> str | None:
        if v is None:
            return v
        dt = utils.validate_datetime(v, True, "报告导出时间 %s" % info.field_name)
        return dt.isoformat()


# . Export Report Result
class ExportReportResult(Parameter):
    """查询报告导出结果参数"""

    # 亚马逊卖家ID (Seller.seller_id)
    seller_id: NonEmptyStr
    # 报告导出任务ID (ExportReportTask.report_id)
    task_id: NonEmptyStr
    # 店铺所在区域
    region: NonEmptyStr


# . Export Report Refresh
class ExportReportRefresh(Parameter):
    """刷新报告导出结果参数"""

    # 亚马逊卖家ID (Seller.seller_id)
    seller_id: NonEmptyStr
    # 报告文件ID (ExportReportResultData.report_document_id)
    report_document_id: NonEmptyStr
    # 店铺所在区域
    region: NonEmptyStr
