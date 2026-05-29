# -*- coding: utf-8 -*-
from pydantic import Field, field_validator
from lingxingapi_httpx import utils
from lingxingapi_httpx.base.param import Parameter
from lingxingapi_httpx.fields import NonEmptyStr, CountryCode, CurrencyCode, NonNegativeInt


# 基础数据 -----------------------------------------------------------------------------------------------------------------------
# . Country Code
class CountryCode(Parameter):
    # 国家代码, 如: "US", "CA"
    country_code: CountryCode


# . Rename Sellers
class RenameSeller(Parameter):
    # 领星店铺ID (Seller.sid)
    sid: NonNegativeInt
    # 新的店铺名称
    name: NonEmptyStr


class RenameSellers(Parameter):
    # 修改店铺名称参数列表
    renames: list = Field(alias="sid_name_list")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("renames", mode="before")
    @classmethod
    def _validate_renames(cls, v) -> list[dict]:
        if not isinstance(v, (list, tuple)):
            res = [RenameSeller.model_validate_params(v)]
        else:
            res = [RenameSeller.model_validate_params(i) for i in v]
            if len(res) == 0:
                raise ValueError("必须提供至少一个 rename 来修改店铺名称")
        return res


# . Excahnge Rate Date
class ExchangeRateDate(Parameter):
    # 日期, 格式为 "YYYY-MM"
    date: str

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("date", mode="before")
    @classmethod
    def _validate_date(cls, v) -> str:
        dt = utils.validate_datetime(v, True, "汇率日期 date")
        return "%04d-%02d" % (dt.year, dt.month)


# . Edit Exchange Rate
class EditExchangeRate(Parameter):
    # 汇率日期, 格式为 "YYYY-MM"
    date: str
    # 货币代码, 如 "CNY", "USD", "EUR"
    currency_code: CurrencyCode = Field(alias="code")
    # 用户自定义汇率 (对比人民币, 如: 7.2008000000), 最多支持10位小数
    user_rate: str = Field(alias="my_rate")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("date", mode="before")
    @classmethod
    def _validate_date(cls, v) -> str:
        dt = utils.validate_datetime(v, False, "汇率日期 date")
        return "%04d-%02d" % (dt.year, dt.month)

    @field_validator("user_rate", mode="before")
    @classmethod
    def _validate_user_rate(cls, v) -> str:
        return str(utils.validate_exchange_rate(v, "用户自定义汇率 user_rate"))
