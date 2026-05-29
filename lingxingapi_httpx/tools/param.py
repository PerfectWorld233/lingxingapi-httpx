# -*- coding: utf-8 -*-
from typing import Any, Optional
from typing_extensions import Self
from pydantic import ValidationInfo, Field, field_validator, model_validator
from lingxingapi_httpx import utils
from lingxingapi_httpx.base.param import Parameter, PageOffestAndLength
from lingxingapi_httpx.fields import NonEmptyStr, NonNegativeInt, CurrencyCode


# 工具数据 ----------------------------------------------------------------------------------------------------------------------
# . Monitor Keywords
class MonitorKeywords(PageOffestAndLength):
    """查询关键词参数"""

    # 领星站点ID列表 (Seller.mid)
    mid: Optional[NonNegativeInt] = None
    # 关键词监控创建开始日期
    start_date: Optional[str] = None
    # 关键词监控创建结束日期
    end_date: Optional[str] = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v: Any, info: ValidationInfo) -> Optional[str]:
        if v is None:
            return v
        dt = utils.validate_datetime(v, False, "关键词创建日期 %s" % info.field_name)
        return "%4d-%02d-%02d" % (dt.year, dt.month, dt.day)


# . Monitor Asins
class MonitorAsins(PageOffestAndLength):
    """查询ASIN监控参数"""

    # 更新开始时间
    start_time: Optional[str] = None
    # 更新结束时间
    end_time: Optional[str] = None
    # 监控等级 (1: A, 2: B, 3: C, 4: D)
    monitor_levels: Optional[list] = Field(None, alias="levels")
    # 搜索字段
    search_field: Optional[NonEmptyStr] = None
    # 搜索值
    search_value: Optional[NonEmptyStr] = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def _validate_datetime(cls, v: Any, info: ValidationInfo) -> Optional[str]:
        if v is None:
            return v
        dt = utils.validate_datetime(v, True, "更新时间 %s" % info.field_name)
        # fmt: off
        return "%4d-%02d-%02d %02d:%02d:%02d" % (
            dt.year, dt.month, dt.day, 
            dt.hour, dt.minute, dt.second
        )
        # fmt: on

    @field_validator("monitor_levels", mode="before")
    @classmethod
    def _validate_levels(cls, v) -> list[int] | None:
        if v is None:
            return None
        return utils.validate_array_of_unsigned_int(v, "监控等级 monitor_levels")

    @field_validator("search_value", mode="before")
    @classmethod
    def _validate_search_value(cls, v) -> str | None:
        if v is None:
            return None
        return ",".join(utils.validate_array_of_non_empty_str(v, "搜索值 search_value"))
