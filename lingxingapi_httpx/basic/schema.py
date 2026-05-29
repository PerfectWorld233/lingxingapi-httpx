# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field, field_validator
from lingxingapi_httpx.fields import IntOrNone2Zero
from lingxingapi_httpx.base.schema import ResponseV1, ResponseResult


# 基础数据 -----------------------------------------------------------------------------------------------------------------------
# . Marketplaces
class Marketplace(BaseModel):
    """亚马逊站点."""

    # 领星站点ID [唯一标识]
    mid: int
    # 站点区域
    region: str
    # 站点亚马逊仓库所属区域 [原字段 'aws_region']
    region_aws: str = Field(validation_alias="aws_region")
    # 站点国家 (中文)
    country: str
    # 站点国家代码 [原字段 'code']
    country_code: str = Field(validation_alias="code")
    # 亚马逊市场ID
    marketplace_id: str


class Marketplaces(ResponseV1):
    """亚马逊站点查询结果."""

    data: list[Marketplace]


# . States
class State(BaseModel):
    """国家的省/州."""

    # 国家代码
    country_code: str
    # 省/州名称 [原字段 'state_or_province_name']
    state: str = Field(validation_alias="state_or_province_name")
    # 省/州代码 [原字段 'code']
    state_code: str = Field(validation_alias="code")


class States(ResponseV1):
    """国家的省/州查询结果."""

    data: list[State]


# . Sellers
class Seller(BaseModel):
    """领星店铺."""

    # 领星站点ID (Marketplace.mid)
    mid: int
    # 领星店铺ID [唯一标识]
    sid: int
    # 亚马逊卖家ID
    seller_id: str
    # 领星店铺名称 (含国家信息) [原字段 'name']
    seller_name: str = Field(validation_alias="name")
    # 领星店铺帐号ID [原字段 'seller_account_id']
    account_id: int = Field(validation_alias="seller_account_id")
    # 领星店铺帐号名称
    account_name: str
    # 亚马逊市场ID (Marketplace.marketplace_id)
    marketplace_id: str
    # 店铺区域
    region: str
    # 店铺国家 (中文)
    country: str
    # 店铺状态 (0: 停止同步, 1: 正常, 2: 授权异常, 3: 欠费停服)
    status: int
    # 店铺是否授权广告 (0: 否, 1: 是) [原字段 'has_ads_setting']
    ads_authorized: int = Field(validation_alias="has_ads_setting")


class Sellers(ResponseV1):
    """领星店铺查询结果."""

    data: list[Seller]


# . Concept Sellers
class ConceptSeller(BaseModel):
    """领星概念店铺."""

    # 领星概念站点ID [原字段 'mid']
    cmid: int = Field(validation_alias="mid")
    # 领星概念店铺ID [唯一标识, 原字段 'id']
    csid: int = Field(validation_alias="id")
    # 亚马逊卖家ID
    seller_id: str
    # 领星概念店铺名称 (含区域信息) [原字段 'name']
    seller_name: str = Field(validation_alias="name")
    # 领星概念店铺账号ID [原字段 'seller_account_id']
    account_id: int = Field(validation_alias="seller_account_id")
    # 领星概念店铺帐号名称 [原字段 'seller_account_name']
    account_name: str = Field(validation_alias="seller_account_name")
    # 概念店铺区域
    region: str
    # 概念店铺国家, 如: "北美共享", "欧洲共享"
    country: str
    # 概念店铺状态 (1: 启用, 2: 停用)
    status: int


class ConceptSellers(ResponseV1):
    """领星概念店铺查询结果."""

    data: list[ConceptSeller]


# . Rename Sellers
class RenameSellersFailureDetail(BaseModel):
    """批量修改店铺名称失败的详情."""

    # 领星店铺ID (Seller.sid)
    sid: int
    # 新店铺名称
    name: str
    # 失败信息 [原字段 'error']
    message: str = Field(validation_alias="error")


class RenameSellers(BaseModel):
    """批量修改店铺名称的结果."""

    success: IntOrNone2Zero = Field(validation_alias="success_num")
    # 修改失败数量 [原字段 'failure_num']
    failure: IntOrNone2Zero = Field(validation_alias="failure_num")
    # 修改失败详情
    failure_detail: list[RenameSellersFailureDetail]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("failure_detail", mode="before")
    def _validate_failure_detail(cls, v):
        if v is None:
            return []
        return [RenameSellersFailureDetail.model_validate(i) for i in v]


class RenameSellersResult(ResponseResult):
    """批量修改店铺名称的响应结果."""

    data: RenameSellers


# . Accounts
class Account(BaseModel):
    """领星账号."""

    # 领星账号所从属的ID (如主帐号ID) [原字段 'zid']
    parent_id: int = Field(validation_alias="zid")
    # 领星帐号ID [唯一标识] [原字段 'uid']
    user_id: int = Field(validation_alias="uid")
    # 是否为主账号 (0: 否, 1: 是)
    is_master: int
    # 帐号角色
    role: str
    # 领星帐号显示的姓名 [原字段 'realname']
    display_name: str = Field(validation_alias="realname")
    # 领星帐号登陆用户名
    username: str
    # 领星帐号电子邮箱
    email: str
    # 领星帐号电话号码 [原字段 'mobile']
    phone: str = Field(validation_alias="mobile")
    # 领星帐号创建时间 (北京时间)
    create_time: str
    # 领星帐号最后登录时间 (北京时间)
    last_login_time: str
    # 领星帐号最后登录IP
    last_login_ip: str
    # 领星帐号登录次数 [原字段 'login_num']
    login_count: int = Field(validation_alias="login_num")
    # 领星帐号状态 (0: 禁用, 1: 正常)
    status: int
    # 关联的领星店铺名称, 逗号分隔 [原字段 'seller']
    sellers: str = Field(validation_alias="seller")


class Accounts(ResponseV1):
    """领星账号查询结果."""

    data: list[Account]


# . Exchange Rates
class ExchangeRate(BaseModel):
    """货币汇率."""

    # 汇率日期 (格式: YYYY-MM-DD)
    date: str
    # 货币名称 (中文) [原字段 'name']
    currency: str = Field(validation_alias="name")
    # 货币代码 [原字段 'code']
    currency_code: str = Field(validation_alias="code")
    # 货币符号 [原字段 'icon']
    currency_icon: str = Field(validation_alias="icon")
    # 中国银行官方汇率 (对比人民币, 如: 7.1541) [原字段 'rate_org']
    boc_rate: float = Field(validation_alias="rate_org")
    # 用户汇率 (对比人民币, 如: 7.2008000000) [原字段 'my_rate']
    user_rate: float = Field(validation_alias="my_rate")
    # 用户汇率修改时间 (北京时间)
    update_time: str

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("date", mode="after")
    @classmethod
    def _validate_date(cls, v: str) -> str:
        return v + "-01"


class ExchangeRates(ResponseV1):
    """货币汇率查询结果."""

    data: list[ExchangeRate]
