# -*- coding: utf-8 -*-
from typing import Annotated
from pydantic_core import CoreSchema, core_schema
from pydantic import GetCoreSchemaHandler, Field
from pydantic import NonNegativeInt, NonNegativeFloat


# Custom Field -----------------------------------------------------------------------------------------------------------------
NonEmptyStr = Annotated[str, Field(min_length=1)]  # 非空字符串
CountryCode = Annotated[str, Field(min_length=2, max_length=2)]  # 国家代码, 2位字符
CurrencyCode = Annotated[str, Field(min_length=3, max_length=3)]  # 货币代码, 3位字符


class IntOrNone2Zero(int):
    """自定义 int 数据类型解析

    - 当传入 None 或空字符串时, 返回 0
    - 其他情况按正常的 int 处理
    """

    def __get_pydantic_core_schema__(self, handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_before_validator_function(
            lambda v: 0 if v is None or v == "" else v, handler(int)
        )


class FloatOrNone2Zero(float):
    """自定义 float 数据类型解析

    - 当传入 None 或空字符串时, 返回 0.0
    - 其他情况按正常的 float 处理
    """

    def __get_pydantic_core_schema__(self, handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_before_validator_function(
            lambda v: 0.0 if v is None or v == "" else v, handler(float)
        )


class StrOrNone2Blank(str):
    """自定义 str 数据类型解析

    - 当传入 None 时, 返回空字符串
    - 其他情况按正常的 str 处理
    """

    def __get_pydantic_core_schema__(self, handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_before_validator_function(
            lambda v: "" if v is None else v, handler(str)
        )
