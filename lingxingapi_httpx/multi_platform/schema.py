# -*- coding: utf-8 -*-
from typing import Any
from pydantic import BaseModel, ConfigDict, Field, model_validator
from lingxingapi_httpx import errors
from lingxingapi_httpx.base.schema import ResponseV1, FlattenDataList
from lingxingapi_httpx.fields import FloatOrNone2Zero, IntOrNone2Zero, StrOrNone2Blank


# 兼容 total 为字符串的 FlattenDataList
class FlattenDataListSafe(BaseModel):
    """从嵌套数据中提取列表数据 (list), 兼容 total 为字符串的情况."""

    @model_validator(mode="before")
    def _flatten_data(cls, data: dict) -> dict:
        try:
            inner: dict = data.pop("data", {})
            total = inner.get("total", 0)
            if isinstance(total, str):
                total = int(total) if total else 0
            data["total"] = max(total, data.get("total", 0))
            data["data"] = inner.get("list", [])
        except Exception:
            raise errors.ResponseDataError(cls.__name__, data=data)
        return data


# 多平台 - 店铺 ----------------------------------------------------------------------------------------------------------------
class MultiPlatformShop(BaseModel):
    """多平台店铺."""

    # 店铺ID
    store_id: str
    # 店铺id【对应获取亚马逊店铺接口sid】
    sid: str = ""
    # 店铺名称
    store_name: str
    # 平台code
    platform_code: str
    # 平台名称
    platform_name: str
    # 店铺币种
    currency: str
    # 店铺同步状态 (1 启用, 0 停用)
    is_sync: int
    # 店铺授权状态 (1 正常授权, 0 授权失败)
    status: int


class MultiPlatformShops(ResponseV1, FlattenDataListSafe):
    """多平台店铺查询结果."""

    data: list[MultiPlatformShop]


# 多平台 - 平台订单 --------------------------------------------------------------------------------------------------------------
class PlatformOrderAddress(BaseModel):
    """平台订单地址."""

    model_config = ConfigDict(extra="allow")

    address_line1: str = Field("", validation_alias="addressLine1")
    address_line2: str = Field("", validation_alias="addressLine2")
    address_line3: str = Field("", validation_alias="addressLine3")
    address_type: int = Field(0, validation_alias="addressType")
    address_type_name: str = Field("", validation_alias="addressTypeName")
    company_name: str = Field("", validation_alias="companyName")
    detail_address: str = Field("", validation_alias="detailAddress")
    house_number: str = Field("", validation_alias="houseNumber")
    recipient_city: str = Field("", validation_alias="recipientCity")
    recipient_country: str = Field("", validation_alias="recipientCountry")
    recipient_name: str = Field("", validation_alias="recipientName")
    recipient_phone: str = Field("", validation_alias="recipientPhone")
    recipient_post_code: str = Field("", validation_alias="recipientPostCode")
    recipient_state: str = Field("", validation_alias="recipientState")


class PlatformOrderItem(BaseModel):
    """平台订单商品项."""

    model_config = ConfigDict(extra="allow")

    platform_sku: str = Field("", validation_alias="platformSku")
    sku: str = ""
    quantity: int = 0
    platform_currency: str = Field("", validation_alias="platformCurrency")
    platform_item_price: FloatOrNone2Zero = Field(0, validation_alias="platformItemPrice")
    platform_shipping_price: FloatOrNone2Zero = Field(0, validation_alias="platformShippingPrice")


class PlatformOrder(BaseModel):
    """平台订单."""

    model_config = ConfigDict(extra="allow")

    platform_order_no: str = Field("", validation_alias="platformOrderNo")
    platform_order_name: str = Field("", validation_alias="platformOrderName")
    store_id: str = Field("", validation_alias="storeId")
    store_name: str = Field("", validation_alias="storeName")
    platform_code: str = Field("", validation_alias="platformCode")
    platform_name: str = Field("", validation_alias="platformName")
    site_code: str = Field("", validation_alias="siteCode")
    site_name: str = Field("", validation_alias="siteName")
    purchase_time: str = Field("", validation_alias="purchaseTime")
    payment_time: str = Field("", validation_alias="paymentTime")
    delivery_time: str = Field("", validation_alias="deliveryTime")
    status: str = ""
    status_name: str = Field("", validation_alias="statusName")
    delivery_type: int = Field(0, validation_alias="deliveryType")
    delivery_type_name: str = Field("", validation_alias="deliveryTypeName")
    currency: str = ""
    total_amount: FloatOrNone2Zero = Field(0, validation_alias="totalAmount")
    buyer_name: str = Field("", validation_alias="buyerName")
    buyer_email: str = Field("", validation_alias="buyerEmail")
    buyer_phone: str = Field("", validation_alias="buyerPhone")
    address: PlatformOrderAddress | None = None
    items: list[PlatformOrderItem] = []
    remark: str = ""
    reference_no: str = Field("", validation_alias="referenceNo")

    @model_validator(mode="before")
    @classmethod
    def _validate_items(cls, data: dict) -> dict:
        if isinstance(data, dict):
            items = data.get("items")
            if items is None:
                data["items"] = []
        return data


class FlattenDataCurrentList(BaseModel):
    """从嵌套数据中提取列表数据 (current + list)"""

    @model_validator(mode="before")
    def _flatten_data(cls, data: dict) -> dict:
        try:
            inner: dict = data.pop("data", {})
            data["current"] = inner.get("current", 0)
            data["data"] = inner.get("list", [])
        except Exception:
            raise errors.ResponseDataError(cls.__name__, data=data)
        return data


class PlatformOrders(ResponseV1, FlattenDataCurrentList):
    """平台订单列表查询结果."""

    current: int = 0
    data: list[PlatformOrder]


# 多平台 - 配对 ----------------------------------------------------------------------------------------------------------------
class MultiPlatformPair(BaseModel):
    """多平台配对."""

    # 店铺ID
    store_id: str
    # 店铺名称
    store_name: str
    # 平台码
    platform_code: str
    # 平台名称
    platform_name: str
    # MSKU
    msku: str
    # 本地SKU
    sku: str
    # 本地SKU品名
    local_name: str
    # 操作时间
    modify_time: str


class MultiPlatformPairs(ResponseV1, FlattenDataListSafe):
    """多平台配对列表查询结果."""

    data: list[MultiPlatformPair]
    # 是否存在下一页 (使用分页游标时返回)
    has_next: bool = False
    # 游标id (使用分页游标时返回)
    next_cursor_id: str = ""

    @model_validator(mode="before")
    @classmethod
    def _set_cursor(cls, data: dict) -> dict:
        if isinstance(data, dict):
            inner: dict = data.get("data", {}) if "data" in data else {}
            if "has_next" not in data:
                data["has_next"] = inner.get("has_next", False)
            if "next_cursor_id" not in data:
                data["next_cursor_id"] = inner.get("next_cursor_id", "")
        return data


# 多平台 - 订单管理 --------------------------------------------------------------------------------------------------------------
class MultiPlatformOrderItem(BaseModel):
    """订单管理订单商品项."""

    model_config = ConfigDict(extra="allow")

    sku: str = ""
    msku: str = ""
    platform_sku: str = Field("", validation_alias="platform_sku")
    product_name: str = Field("", validation_alias="product_name")
    quantity: int = 0
    price: FloatOrNone2Zero = 0
    currency: str = ""


class MultiPlatformOrder(BaseModel):
    """订单管理订单."""

    model_config = ConfigDict(extra="allow")

    store_id: str = ""
    wid: str = ""
    reference_no: str = ""
    global_order_no: str = Field("", validation_alias="global_order_no")
    original_global_order_no: str = Field("", validation_alias="original_global_order_no")
    amount_currency: str = Field("", validation_alias="amount_currency")
    remark: str = ""
    order_from_name: str = Field("", validation_alias="order_from_name")
    status: int = 0
    flow_node: int = 0
    status_sub: int = 0
    split_type: str = ""
    platform_order_no: str = Field("", validation_alias="platform_order_no")
    platform_order_name: str = Field("", validation_alias="platform_order_name")
    platform_code: str = Field("", validation_alias="platform_code")
    platform_name: str = Field("", validation_alias="platform_name")
    store_name: str = Field("", validation_alias="store_name")
    site_code: str = Field("", validation_alias="site_code")
    site_name: str = Field("", validation_alias="site_name")
    purchase_time: int = 0
    payment_time: int = 0
    delivery_time: int = 0
    update_time: int = 0
    buyer_name: str = Field("", validation_alias="buyer_name")
    buyer_email: str = Field("", validation_alias="buyer_email")
    buyer_phone: str = Field("", validation_alias="buyer_phone")
    recipient_country: str = Field("", validation_alias="recipient_country")
    recipient_state: str = Field("", validation_alias="recipient_state")
    recipient_city: str = Field("", validation_alias="recipient_city")
    recipient_address: str = Field("", validation_alias="recipient_address")
    recipient_post_code: str = Field("", validation_alias="recipient_post_code")
    total_amount: FloatOrNone2Zero = Field(0, validation_alias="total_amount")
    paid_amount: FloatOrNone2Zero = Field(0, validation_alias="paid_amount")
    shipping_amount: FloatOrNone2Zero = Field(0, validation_alias="shipping_amount")
    discount_amount: FloatOrNone2Zero = Field(0, validation_alias="discount_amount")
    tax_amount: FloatOrNone2Zero = Field(0, validation_alias="tax_amount")
    items: list[MultiPlatformOrderItem] = []
    customer_shipping_list: list[str] = Field([], validation_alias="customer_shipping_list")

    @model_validator(mode="before")
    @classmethod
    def _validate_items(cls, data: dict) -> dict:
        if isinstance(data, dict):
            if data.get("items") is None:
                data["items"] = []
            if data.get("customer_shipping_list") is None:
                data["customer_shipping_list"] = []
        return data


class MultiPlatformOrders(ResponseV1, FlattenDataListSafe):
    """订单管理订单列表查询结果."""

    data: list[MultiPlatformOrder]
