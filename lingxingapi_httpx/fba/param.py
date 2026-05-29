# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import ValidationInfo, Field, field_validator
from lingxingapi_httpx import utils
from lingxingapi_httpx.base.param import Parameter, PageOffestAndLength
from lingxingapi_httpx.fields import NonEmptyStr, NonNegativeInt


# 共享参数 ---------------------------------------------------------------------------------------------------------------------
# . STA Plan ID
class StaID(Parameter):
    """查询STA计划ID参数"""

    # 领星店铺ID
    sid: NonNegativeInt
    # STA计划ID
    inbound_plan_id: NonEmptyStr = Field(alias="inboundPlanId")


# FBA - FBA货件 (STA) ----------------------------------------------------------------------------------------------------------
# . STA Plans
class StaPlans(Parameter):
    """查询STA计划参数"""

    # 开始日期 (北京时间), 双闭区间, 格式: YYYY-MM-DD
    start_date: str = Field(alias="dateBegin")
    # 结束日期 (北京时间), 双闭区间, 格式: YYYY-MM-DD
    end_date: str = Field(alias="dateEnd")
    # 日期类型 (1: 创建日期; 2: 更新日期)
    date_type: NonNegativeInt = Field(alias="dateType")
    # STA计划名称 (模糊搜索)
    plan_name: Optional[NonEmptyStr] = Field(None, alias="planName")
    # 货件ID或货件单号列表 (精确搜索)
    shipment_ids: Optional[list] = Field(None, alias="shipmentIdList")
    # STA计划状态列表 ('ACTIVE', 'VOIDED', 'SHIPPED', 'ERRORED')
    statuses: Optional[list] = Field(None, alias="statusList")
    # 领星店铺ID列表
    sids: Optional[list] = None
    # 分页页码
    page: NonNegativeInt = 1
    # 分页大小
    length: NonNegativeInt = 200

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v, info: ValidationInfo) -> str:
        dt = utils.validate_datetime(v, False, "日期 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)

    @field_validator("shipment_ids", mode="before")
    @classmethod
    def _validate_shipment_ids(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_non_empty_str(
            v, "货件ID或货件单号列表 shipment_ids"
        )

    @field_validator("statuses", mode="before")
    @classmethod
    def _validate_statuses(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_non_empty_str(v, "STA计划状态列表 statuses")

    @field_validator("sids", mode="before")
    @classmethod
    def _validate_sids(cls, v) -> list[int] | None:
        if v is None:
            return None
        return utils.validate_array_of_unsigned_int(v, "领星店铺ID列表 sids")


# . Packing Group Boxes
class PackingGroupBoxes(StaID):
    """查询包装箱信息参数"""

    packing_group_ids: list = Field(alias="packingGroupIdList")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("packing_group_ids", mode="before")
    @classmethod
    def _validate_packing_group_ids(cls, v) -> list[str]:
        return utils.validate_array_of_non_empty_str(
            v, "包装箱ID列表 packing_group_ids"
        )


# . Shipments
class Shipments(PageOffestAndLength):
    """查询FBA货件列表参数"""

    # 领星店铺IDs (多个ID用逗号分隔)
    sids: NonEmptyStr = Field(alias="sid")
    # 货件创建开始日期, 左闭右开
    start_date: str
    # 货件创建结束日期, 左闭右开
    end_date: str
    # 子筛选开始日期, 左闭右开
    sub_start_date: Optional[str] = Field(None, alias="start_extra_date")
    # 子筛选结束日期, 左闭右开
    sub_end_date: Optional[str] = Field(None, alias="end_extra_date")
    # 子筛选日期类型 (1: 货件修改日期)
    sub_date_type: Optional[str] = Field(None, alias="extra_date_field")
    # 货件IDs (多个ID用逗号分隔)
    shipment_ids: Optional[str] = Field(None, alias="shipment_id")
    # 货件状态 (多个状态用逗号分隔)
    # ('DELETED', 'CLOSED', 'CANCELLED', 'WORKING', 'RECEIVING', 'SHIPPED', 'READY_TO_SHIP')
    shipment_statuses: Optional[str] = Field(None, alias="shipment_status")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("sids", mode="before")
    @classmethod
    def _validate_sids(cls, v) -> str:
        ids = utils.validate_array_of_unsigned_int(v, "领星店铺ID列表 sids")
        return ",".join(map(str, ids))

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v, info: ValidationInfo) -> str:
        dt = utils.validate_datetime(v, False, "日期 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)

    @field_validator("sub_start_date", "sub_end_date", mode="before")
    @classmethod
    def _validate_sub_date(cls, v, info: ValidationInfo) -> str | None:
        if v is None:
            return None
        dt = utils.validate_datetime(v, False, "日期 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)

    @field_validator("sub_date_type", mode="before")
    @classmethod
    def _validate_sub_date_type(cls, v) -> str | None:
        if v is None:
            return None
        if v == 1:
            return "update"
        if v == "update":
            return v
        raise ValueError("子筛选日期类型 sub_date_type 只能为 (1: 货件修改日期)")

    @field_validator("shipment_ids", mode="before")
    @classmethod
    def _validate_shipment_ids(cls, v) -> str | None:
        if v is None:
            return None
        ids = utils.validate_array_of_non_empty_str(v, "货件IDs shipment_ids")
        return ",".join(ids)

    @field_validator("shipment_statuses", mode="before")
    @classmethod
    def _validate_shipment_statuses(cls, v) -> str | None:
        if v is None:
            return None
        statuses = utils.validate_array_of_non_empty_str(
            v, "货件状态 shipment_statuses"
        )
        return ",".join(statuses)


# . Shipment Details
class ShipmentDetails(StaID):
    """查询FBA货件详情参数"""

    # FBA货件ID
    shipment_ids: list[str] = Field(alias="shipmentIds")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("shipment_ids", mode="before")
    @classmethod
    def _validate_shipment_ids(cls, v) -> list[str]:
        return utils.validate_array_of_non_empty_str(v, "FBA货件IDs shipment_ids")


# . Shipment Boxes
class ShipmentBoxes(StaID):
    """查询FBA货件箱子信息参数"""

    # FBA货件ID
    shipment_ids: list[str] = Field(alias="shipmentIdList")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("shipment_ids", mode="before")
    @classmethod
    def _validate_shipment_ids(cls, v) -> list[str]:
        return utils.validate_array_of_non_empty_str(v, "FBA货件IDs shipment_ids")


# . Shipment Transports
class ShipmentTransports(StaID):
    """查询STA计划ID和货件ID参数"""

    # FBA货件ID
    shipment_id: NonEmptyStr = Field(alias="shipmentId")


# . Shipment Receipt
class ShipmentReceiptRecords(PageOffestAndLength):
    """查询FBA货件收货信息参数"""

    # 领星店铺ID
    sid: NonNegativeInt
    # 收件日期
    date: str = Field(alias="event_date")
    # FBA货件单号
    shipment_ids: Optional[list] = Field(None, alias="fba_shipment_id")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("date", mode="before")
    @classmethod
    def _validate_date(cls, v) -> str:
        dt = utils.validate_datetime(v, False, "收件日期 date")
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)

    @field_validator("shipment_ids", mode="before")
    @classmethod
    def _validate_shipment_ids(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_non_empty_str(v, "FBA货件单号列表 shipment_ids")


# . Shipment Delivery Address
class ShipmentDeliveryAddress(Parameter):
    """查询FBA货件收货地址参数"""

    # 货件唯一记录ID (Shipment.id)
    id: NonNegativeInt


# . Ship From Addresses
class ShipFromAddresses(PageOffestAndLength):
    """查询FBA货件发货地址参数"""

    # 领星店铺ID
    sids: Optional[list] = Field(None, alias="sid")
    # 搜索字段 ('alias_name', 'sender_name')
    search_field: Optional[NonEmptyStr] = None
    # 搜索内容 (模糊搜索)
    search_value: Optional[NonEmptyStr] = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("sids", mode="before")
    @classmethod
    def _validate_sids(cls, v) -> list[int] | None:
        if v is None:
            return None
        return utils.validate_array_of_unsigned_int(v, "领星店铺ID列表 sids")
