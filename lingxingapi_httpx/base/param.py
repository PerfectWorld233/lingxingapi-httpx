# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel, ConfigDict
from lingxingapi_httpx.fields import NonNegativeInt


# 基础模型 -----------------------------------------------------------------------------------------------------------------------
class Parameter(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    def model_dump_params(
        self,
        *,
        include=None,
        exclude=None,
        context=None,
        by_alias=True,
        exclude_unset=False,
        exclude_defaults=False,
        exclude_none=True,
        round_trip=False,
        warnings=True,
        fallback=None,
        serialize_as_any=False,
    ) -> dict:
        """将模型转换为字典, 并按字母顺序排序键 `<'dict'>`."""
        res = self.model_dump(
            mode="python",
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            fallback=fallback,
            serialize_as_any=serialize_as_any,
        )
        return dict(sorted(res.items()))

    @classmethod
    def model_validate_params(cls, data: object) -> dict:
        """将传入的数据进行验证, 转换为字典, 且按字母顺序排序键"""
        if isinstance(data, BaseModel) and not isinstance(data, cls):
            data = data.model_dump()
        return cls.model_validate(data).model_dump_params()


# 公用参数 -----------------------------------------------------------------------------------------------------------------------
class PageOffestAndLength(Parameter):
    # 分页偏移量
    offset: Optional[NonNegativeInt] = None
    # 分页长度
    length: Optional[NonNegativeInt] = None
