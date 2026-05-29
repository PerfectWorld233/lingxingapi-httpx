# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import ValidationInfo, Field, field_validator
from lingxingapi_httpx import utils
from lingxingapi_httpx.base.param import Parameter, PageOffestAndLength
from lingxingapi_httpx.fields import NonEmptyStr, NonNegativeInt


# 采购 --------------------------------------------------------------------------------------------------------------------------
# . Edit Supplier
class EditSupplier(Parameter):
    """编辑产品供应商参数"""

    # 供应商名字
    supplier_name: NonEmptyStr
    # 供应商ID
    supplier_id: Optional[NonNegativeInt] = Field(None, alias="sys_supplier_id")
    # 供应商编码
    supplier_code: Optional[str] = None
    # 供应商等级
    supplier_level: Optional[int] = Field(None, alias="level")
    # 供应商员工数 (1: 少于50, 2: 50-150, 3: 150-500, 4: 500-1000, 5: 1000+)
    employees_level: Optional[int] = Field(None, alias="employees")
    # 供应商网址
    website_url: Optional[str] = Field(None, alias="url")
    # 供应商联系人
    contact_person: Optional[str] = None
    # 供应商联系电话
    phone: Optional[str] = Field(None, alias="contact_number")
    # 供应商联系邮箱
    email: Optional[str] = None
    # 供应商联系QQ
    qq: Optional[str] = None
    # 供应商传真
    fax: Optional[str] = None
    # 供应商地址
    address: Optional[str] = None
    # 供应商开户银行
    bank: Optional[str] = Field(None, alias="open_bank")
    # 供应商银行账号户名
    bank_account_name: Optional[str] = Field(None, alias="account_name")
    # 供应商银行账号卡号
    bank_account_number: Optional[str] = Field(None, alias="bank_card_number")
    # 供应商备注
    note: Optional[str] = Field(None, alias="remark")
    # 采购跟进人员ID
    purchase_staff_ids: Optional[list] = Field(None, alias="purchaser")
    # 采购支付方式 (1: 网银转账, 2: 网上支付)
    payment_method: Optional[int] = None
    # 采购结算方式 (7: 现结, 8: 月结)
    settlement_method: Optional[int] = None
    # 采购结算描述
    settlement_desc: Optional[str] = Field(None, alias="settlement_description")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("purchase_staff_ids", mode="before")
    @classmethod
    def _validate_purchase_staff_ids(cls, v) -> list[int] | None:
        if v is None:
            return None
        return utils.validate_array_of_unsigned_int(
            v, "采购跟进人员ID purchase_staff_ids"
        )


# . Purchase Plan
class PurchasePlans(PageOffestAndLength):
    """查询采购计划参数"""

    # fmt: off
    # 查询开始日期, 闭区间, 格式为 "YYYY-MM-DD"
    start_date: str
    # 查询结束日期, 闭区间, 格式为 "YYYY-MM-DD"
    end_date: str
    # 查询日期类型 (creator_time: 创建时间, expect_arrive_time: 预计到货日期, update_time: 更新时间)
    date_type: str = Field(alias="search_field_time")
    # 采购计划单号列表
    plan_ids: Optional[list] = Field(None, alias="plan_sns")
    # 采购计划状态列表 (2: 待采购, -2: 已完成, 121: 待审批, 122: 已驳回, -3或124: 已作废)
    status: Optional[list] = None
    # 是否为捆绑产品 (0: 否, 1: 是)
    is_bundled: Optional[NonNegativeInt] = Field(None, alias="is_combo")
    # 是否关联加工计划 (0: 否, 1: 是)
    is_process_plan_linked: Optional[NonNegativeInt] = Field(None, alias="is_related_process_plan")
    # 领星店铺ID列表
    sids: Optional[list] = None
    # fmt: on

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v, info: ValidationInfo) -> str:
        dt = utils.validate_datetime(v, True, "查询日期 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)

    @field_validator("date_type", mode="before")
    @classmethod
    def _validate_date_type(cls, v) -> str:
        if v == 1:
            return "creator_time"
        elif v == 2:
            return "expect_arrive_time"
        elif v == 3:
            return "update_time"
        return utils.validate_non_empty_str(v, "查询日期类型 date_type")

    @field_validator("plan_ids", mode="before")
    @classmethod
    def _validate_plan_ids(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_non_empty_str(v, "采购计划单号列表 plan_ids")

    @field_validator("status", mode="before")
    @classmethod
    def _validate_status(cls, v) -> list[int] | None:
        if v is None:
            return None
        return utils.validate_array_of_unsigned_int(v, "采购计划状态列表 status")

    @field_validator("sids", mode="before")
    @classmethod
    def _validate_sids(cls, v) -> list[int] | None:
        if v is None:
            return None
        return utils.validate_array_of_unsigned_int(v, "领星店铺ID列表 sids")
