# -*- coding: utf-8 -*-
from typing import Any, Optional
from typing_extensions import Self
from pydantic import ValidationInfo, Field, field_validator, model_validator
from lingxingapi_httpx import utils
from lingxingapi_httpx.base.param import Parameter, PageOffestAndLength
from lingxingapi_httpx.fields import NonEmptyStr, NonNegativeInt, CurrencyCode


# 公共参数 ----------------------------------------------------------------------------------------------------------------------
class FinanceShare(PageOffestAndLength):
    """财务数据共享参数"""

    # 领星站点ID列表 (Seller.mid)
    mids: Optional[list] = Field(None, alias="countryCodes")
    # 领星店铺ID列表 (Seller.sid)
    sids: Optional[list] = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("mids", mode="before")
    @classmethod
    def _validate_mids(cls, v) -> list[int] | None:
        if v is None:
            return None
        return utils.validate_array_of_unsigned_int(v, "站点ID mids")

    @field_validator("sids", mode="before")
    @classmethod
    def _validate_sids(cls, v) -> list[int] | None:
        if v is None:
            return None
        return utils.validate_array_of_unsigned_int(v, "店铺ID sids")


# 亚马逊交易数据 -----------------------------------------------------------------------------------------------------------------
# . Transactions
class Transactions(FinanceShare):
    """查询亚马逊交易明细参数"""

    # 交易开始日期 (本地时间), 双闭区间, 间隔不超过7天
    transaction_start_date: Optional[str] = Field(None, alias="startDate")
    # 交易结束日期 (本地时间), 双闭区间, 间隔不超过7天
    transaction_end_date: Optional[str] = Field(None, alias="endDate")
    # 数据更新开始时间 (中国时间), 间隔不超过7天
    update_start_time: Optional[str] = Field(None, alias="gmtModifiedStart")
    # 数据更新结束时间 (中国时间), 间隔不超过7天
    update_end_time: Optional[str] = Field(None, alias="gmtModifiedEnd")
    # 事件类型
    event_types: Optional[str] = Field(None, alias="eventType")
    # 交易类型
    transaction_type: Optional[NonEmptyStr] = Field(None, alias="type")
    # 搜索字段 ('transaction_id', 'transaction_number', 'amazon_order_id', 'settlement_id')
    search_field: Optional[NonEmptyStr] = Field(None, alias="searchField")
    # 搜索值
    search_value: Optional[NonEmptyStr] = Field(None, alias="searchValue")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("transaction_start_date", "transaction_end_date", mode="before")
    @classmethod
    def _validate_date(cls, v, info: ValidationInfo) -> str | None:
        if v is None:
            return None
        dt = utils.validate_datetime(v, False, "交易日期 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)

    @field_validator("update_start_time", "update_end_time", mode="before")
    @classmethod
    def _validate_time(cls, v, info: ValidationInfo) -> str | None:
        if v is None:
            return None
        dt = utils.validate_datetime(v, True, "数据更新时间 %s" % info.field_name)
        # fmt: off
        return "%04d-%02d-%02d %02d:%02d:%02d" % (
            dt.year, dt.month, dt.day, 
            dt.hour, dt.minute, dt.second
        )
        # fmt: on

    @field_validator("event_types", mode="before")
    @classmethod
    def _validate_event_types(cls, v) -> str | None:
        if v is None:
            return None
        return ",".join(utils.validate_non_empty_str(v, "事件类型 event_types"))

    @field_validator("search_field", mode="before")
    @classmethod
    def _validate_search_field(cls, v) -> str | None:
        if v is None:
            return None
        if v == "transaction_id":
            return "primary_id"
        if v == "transaction_number":
            return "id"
        return v


# . Settlements
class Settlements(FinanceShare):
    """查询亚马逊结算汇总参数"""

    # 开始日期, 间隔不超过90天
    start_date: str = Field(alias="startDate")
    # 结束日期, 间隔不超过90天
    end_date: str = Field(alias="endDate")
    # 日期类型 (0: 结算开始时间, 1: 结算结束时间, 2: 转账时间)
    date_type: NonNegativeInt = Field(alias="dateType")
    # 搜索字段 ('settlement_id': 结算ID, 'settlement_number': 账单编号)
    search_field: Optional[NonEmptyStr] = Field(None, alias="searchField")
    # 搜索值
    search_value: Optional[NonEmptyStr] = Field(None, alias="searchValue")
    # 结算金额目标转换货币代码, 默认保持原币种
    currency_code: Optional[CurrencyCode] = Field(None, alias="currencyCode")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v, info: ValidationInfo) -> str:
        dt = utils.validate_datetime(v, False, "查询日期 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)

    @field_validator("search_field", mode="before")
    @classmethod
    def _validate_search_field(cls, v) -> str | None:
        if v is None:
            return None
        return "id" if v == "settlement_number" else v


# . Settlement Variances
class ShipmentSettlement(FinanceShare):
    """查询亚马逊结算与发货差异参数"""

    # 亚马逊卖家ID列表 (Seller.seller_id)
    seller_ids: list = Field(alias="amazonSellerIds")
    # 查询开始日期, 闭合区间
    start_date: str = Field(alias="filterBeginDate")
    # 查询结束日期, 闭合区间
    end_date: str = Field(alias="filterEndDate")
    # 日期类型 (01: 下单时间, 02: 付款时间, 03: 发货时间, 04: 结算时间, 05: 转账时间, 06: 更新时间)
    date_type: NonEmptyStr = Field(alias="timeType")
    # 亚马逊SKU列表
    mskus: Optional[list] = None
    # 领星本地SKU列表
    lskus: Optional[list] = Field(None, alias="skus")
    # 领星本地商品名称列表
    product_names: Optional[list] = Field(None, alias="productNames")
    # 亚马逊订单编码列表
    amazon_order_ids: Optional[list] = Field(None, alias="orderNumbers")
    # 配送编号列表
    shipment_ids: Optional[list] = Field(None, alias="shipmentNumbers")
    # 物流跟踪号列表
    tracking_numbers: Optional[list] = Field(None, alias="trackCodes")
    # 国家代码
    country_codes: Optional[list] = Field(None, alias="countryCodes")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("seller_ids", mode="before")
    @classmethod
    def _validate_seller_ids(cls, v) -> list[str]:
        return utils.validate_array_of_non_empty_str(v, "卖家ID seller_ids")

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v, info: ValidationInfo) -> str:
        dt = utils.validate_datetime(v, False, "查询日期 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)

    @field_validator("date_type", mode="before")
    @classmethod
    def _validate_date_type(cls, v) -> str:
        if v == 1:
            return "01"
        if v == 2:
            return "02"
        if v == 3:
            return "03"
        if v == 4:
            return "04"
        if v == 5:
            return "05"
        if v == 6:
            return "06"
        return v

    @field_validator(
        "mskus",
        "lskus",
        "product_names",
        "amazon_order_ids",
        "shipment_ids",
        "tracking_numbers",
        "country_codes",
        mode="before",
    )
    @classmethod
    def _validate_list_of_str(cls, v, info: ValidationInfo) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_non_empty_str(v, "参数 %s" % info.field_name)


# . Receivables
class Receivables(FinanceShare):
    """查询亚马逊应收账款参数"""

    # 结算日期
    settlement_date: str = Field(alias="settleMonth")
    # 对账状态 (0: 未对账, 1: 已对账)
    archive_status: Optional[NonNegativeInt] = Field(None, alias="archiveStatus")
    # 应收状态 (0: 未收款, 1: 已收款)
    received_state: Optional[NonNegativeInt] = Field(None, alias="receivedState")
    # 排序字段 ('opening_balance': 期初余额, 'income': 收入, 'refund': 退款, 'spend' 支出, 'other': 其他)
    sort_field: Optional[NonEmptyStr] = Field(None, alias="sortField")
    # 排序方式 (0: 升序, 1: 降序)
    sort_type: Optional[NonEmptyStr] = Field(None, alias="sortType")
    # 结算金额目标转换货币代码, 默认保持原币种
    currency_code: Optional[CurrencyCode] = Field(None, alias="currencyCode")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("settlement_date", mode="before")
    @classmethod
    def _validate_settlement_date(cls, v) -> str:
        dt = utils.validate_datetime(v, False, "结算日期 settlement_date")
        return "%04d-%02d" % (dt.year, dt.month)

    @field_validator("sort_field", mode="before")
    @classmethod
    def _validate_sort_field(cls, v) -> str | None:
        if v is None:
            return None
        if v == "opening_balance":
            return "beginningBalanceCurrencyAmount"
        if v == "income":
            return "incomeAmount"
        if v == "refund":
            return "refundAmount"
        if v == "spend":
            return "spendAmount"
        return v

    @field_validator("sort_type", mode="before")
    @classmethod
    def _validate_sort_type(cls, v) -> str | None:
        if v is None:
            return None
        if v == 0:
            return "asc"
        if v == 1:
            return "desc"
        raise ValueError("排序方式 sort_type 必须为 0 (升序) 或 1 (降序)")


# 亚马逊库存数据 -----------------------------------------------------------------------------------------------------------------
# . Ledger Details
class LedgerDetail(PageOffestAndLength):
    """查询亚马逊库存明细台账参数"""

    # 亚马逊卖家ID列表 (Seller.seller_id)
    seller_ids: list = Field(alias="sellerIds")
    # 统计开始日期, 闭合区间
    start_date: str = Field(alias="startDate")
    # 统计结束日期, 闭合区间
    end_date: str = Field(alias="endDate")
    # 亚马逊ASIN列表
    asins: Optional[list] = None
    # 亚马逊SKU列表
    mskus: Optional[list] = None
    # 亚马逊FNSKU列表
    fnskus: Optional[list] = None
    # 国家代码 (库存位置)
    country_codes: Optional[list] = Field(None, alias="locations")
    # 事件类型
    # (1: Shipments, 2 :CustomerReturns, 3 :WhseTransfers, 4 :Receipts, 5 :VendorReturns, 6 :Adjustments)
    event_types: Optional[list] = Field(None, alias="eventTypes")
    # 货物关联ID (支持模糊查询)
    reference_id: Optional[NonNegativeInt] = Field(None, alias="referenceId")
    # 库存处置结果 (1: SELLABLE, 2: UNSELLABLE, 3: ALL)
    disposition: Optional[NonEmptyStr] = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("seller_ids", mode="before")
    @classmethod
    def _validate_seller_ids(cls, v) -> list[str]:
        return utils.validate_array_of_non_empty_str(v, "卖家ID seller_ids")

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v, info: ValidationInfo) -> str:
        dt = utils.validate_datetime(v, False, "查询日期 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)

    @field_validator("asins", "mskus", "fnskus", "country_codes", mode="before")
    @classmethod
    def _validate_list_of_str(cls, v, info: ValidationInfo) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_non_empty_str(v, "参数 %s" % info.field_name)

    @field_validator("event_types", mode="before")
    @classmethod
    def _validate_event_types(cls, v) -> list[int] | None:
        if v is None:
            return None
        res: list = []
        for i in utils.validate_array_of_non_empty_str(v, "事件类型 event_types"):
            if i == "Shipments":
                res.append("01")
            elif i == "CustomerReturns":
                res.append("02")
            elif i == "WhseTransfers":
                res.append("03")
            elif i == "Receipts":
                res.append("04")
            elif i == "VendorReturns":
                res.append("05")
            elif i == "Adjustments":
                res.append("06")
            else:
                res.append(i)
        return res

    @field_validator("disposition", mode="before")
    @classmethod
    def _validate_disposition(cls, v) -> str | None:
        if v is None:
            return None
        if v == "SELLABLE":
            return "01"
        if v == "UNSELLABLE":
            return "02"
        if v == "ALL":
            return "03"
        return v


# . Ledger Summaries
class LedgerSummary(LedgerDetail):
    """查询亚马逊库存汇总台账参数"""

    # 查询维度 (1: 月, 2: 日)
    query_dimension: NonNegativeInt = Field(alias="queryType")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @model_validator(mode="after")
    def _date_adjustments(self) -> Self:
        # 调整日期数据
        if self.query_dimension == 1:
            self.start_date = self.start_date[:7]
            self.end_date = self.end_date[:7]
        return self


# . Ledger Valuation
class LedgerValuation(PageOffestAndLength):
    """查询亚马逊库存价值台账参数"""

    # 开始日期, 不能跨月份
    start_date: str
    # 结束日期, 不能跨月份
    end_date: str
    # 日期类型
    date_type: NonEmptyStr = Field(alias="query_type")
    # 出入库类型列表
    # 1 期初库存-FBA上月结存
    # 10 调拨入库-FBA补货入库
    # 11 调拨入库-FBA途损补回
    # 12 调拨入库-FBA超签入库
    # 13 调拨入库-FBA超签入库 (Close后)
    # 14 调拨入库-FBA补货入库 (无发货单)
    # 20 调拨入库-FBA调仓入库
    # 35 调拨入库-FBA发货在途入库
    # 25 盘点入库-FBA盘点入库
    # 30 FBA退货-FBA无源单销售退货
    # 31 FBA退货-FBA有源单销售退货
    # 200 销售出库-FBA补发货销售
    # 201 销售出库-FBA多渠道销售订单
    # 202 销售出库-FBA亚马逊销售订单
    # 205 其他出库-FBA补货出库
    # 220 盘点出库-FBA盘点出库
    # 15 调拨出库-FBA调仓出库
    # 215 调拨出库-FBA移除
    # 225 调拨出库-FBA发货在途出库
    # 226 调拨出库-FBA发货途损
    # 227 调拨出库-后补发货单在途出库
    # 5 调整单- FBA对账差异入库调整
    # 210 调整单-FBA对账差异出库调整
    # 400 调整单-尾差调整
    # 420 调整单-负库存数量调整
    # 405 调整单-期初成本录入
    transaction_types: Optional[list] = Field(None, alias="business_types")
    # 出入库编码列表
    transaction_numbers: Optional[list] = Field(None, alias="business_numbers")
    # 源头单据号列表
    source_numbers: Optional[list] = Field(None, alias="origin_accounts")
    # 仓库名称列表
    warehouse_names: Optional[list] = Field(None, alias="wh_names")
    # 领星店铺名称列表
    seller_names: Optional[list] = Field(None, alias="shop_names")
    # 亚马逊SKU列表
    mskus: Optional[list] = None
    # 领星本地SKU列表
    lskus: Optional[list] = Field(None, alias="skus")
    # 库存处置结果列表 (1: 可用在途, 2: 可用, 3: 次品)
    dispositions: Optional[list] = Field(None, alias="disposition_types")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("transaction_types", mode="before")
    @classmethod
    def _validate_transaction_types(cls, v) -> list[int]:
        if v is None:
            return None
        return utils.validate_array_of_unsigned_int(v, "出入库类型 transaction_types")

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v, info: ValidationInfo) -> str:
        dt = utils.validate_datetime(v, False, "查询日期 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)

    @field_validator("date_type", mode="before")
    @classmethod
    def _validate_date_type(cls, v) -> str | Any:
        if v == 1:
            return "01"
        if v == 2:
            return "02"
        return v

    @field_validator(
        "transaction_numbers",
        "source_numbers",
        "warehouse_names",
        "seller_names",
        "mskus",
        "lskus",
        mode="before",
    )
    @classmethod
    def _validate_list_of_str(cls, v, info: ValidationInfo) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_non_empty_str(v, "参数 %s" % info.field_name)

    @field_validator("dispositions", mode="before")
    @classmethod
    def _validate_dispositions(cls, v) -> list[int] | None:
        if v is None:
            return None
        return utils.validate_array_of_unsigned_int(v, "库存处置结果 dispositions")


# 亚马逊广告数据 -----------------------------------------------------------------------------------------------------------------
# . Ads Invoices
class AdsInvoices(FinanceShare):
    """查询亚马逊广告发票参数"""

    # 开始日期
    start_date: str = Field(alias="invoice_start_time")
    # 结束日期
    end_date: str = Field(alias="invoice_end_time")
    # 广告类型 ('SP', 'SB', 'SBV', 'SD')
    ads_type: Optional[list[NonEmptyStr]] = None
    # 领星站点ID列表 (Seller.mid)
    mids: Optional[list] = None
    # 搜索字段 ('invoice_id', 'msku', 'asin', 'campaign_name')
    search_field: Optional[NonEmptyStr] = Field(None, alias="search_type")
    # 搜索值
    search_value: Optional[NonEmptyStr] = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v, info: ValidationInfo) -> str:
        dt = utils.validate_datetime(v, True, "查询时间 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)

    @field_validator("ads_type", mode="before")
    @classmethod
    def _validate_ads_type(cls, v) -> list[str] | None:
        if v is None:
            return None
        if v in ("SP", "sp"):
            return ["SPONSORED PRODUCTS"]
        if v in ("SB", "sb"):
            return ["SPONSORED BRANDS"]
        if v in ("SBV", "sbv"):
            return ["SPONSORED BRANDS VIDEO"]
        if v in ("SD", "sd"):
            return ["SPONSORED DISPLAY"]
        if isinstance(v, list):
            return v
        return [v]

    @field_validator("search_field", mode="before")
    @classmethod
    def _validate_search_field(cls, v) -> str | None:
        if v is None:
            return None
        return "ads_campaign" if v == "campaign_name" else v


# . Ads Invoice Detail
class AdsInvoiceDetail(Parameter):
    """查询亚马逊广告发票明细参数"""

    # 领星店铺ID (Seller.sid)
    sid: NonNegativeInt
    # 广告发票ID
    invoice_id: NonEmptyStr


# . Ads Campaign Invoices
class AdsCampaignInvoices(PageOffestAndLength):

    # 领星店铺ID
    sid: NonNegativeInt
    # 广告发票ID
    invoice_id: NonEmptyStr
    # 广告类型 ('SP', 'SB', 'SBV', 'SD')
    ads_type: Optional[list[NonEmptyStr]] = None
    # 搜索字段 ('campaign_name', 'msku')
    search_field: Optional[NonEmptyStr] = Field(None, alias="search_type")
    # 搜索值
    search_value: Optional[NonEmptyStr] = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("ads_type", mode="before")
    @classmethod
    def _validate_ads_type(cls, v) -> list[str] | None:
        if v is None:
            return None
        if v in ("SP", "sp"):
            return ["SPONSORED PRODUCTS"]
        if v in ("SB", "sb"):
            return ["SPONSORED BRANDS"]
        if v in ("SBV", "sbv"):
            return ["SPONSORED BRANDS VIDEO"]
        if v in ("SD", "sd"):
            return ["SPONSORED DISPLAY"]
        if isinstance(v, list):
            return v
        return [v]

    @field_validator("search_field", mode="before")
    @classmethod
    def _validate_search_field(cls, v) -> str | Any | None:
        if v is None:
            return None
        return "ads_campaign" if v == "campaign_name" else v


# 亚马逊损益报告 -----------------------------------------------------------------------------------------------------------------
# . Income Statement Sellers
class IncomeStatementSellers(FinanceShare):
    """查询损益报告-店铺维度参数"""

    # 领星站点ID列表 (Seller.mid)
    mids: Optional[list] = None
    # 结算开始日期
    start_date: str = Field(alias="startDate")
    # 结算结束日期
    end_date: str = Field(alias="endDate")
    # 查询维度 (0: 日, 1: 月 | 默认 0)
    query_dimension: Optional[NonNegativeInt] = Field(alias="monthlyQuery")
    # 交易状态 ('Deferred', 'Disbursed', 'DisbursedAndPreSettled', 'All' | 默认 'Disbursed')
    # Deferred: 订单未进入Transaction报告, 无法回款
    # Disbursed: 订单已经进入Transaction报告, 可以回款
    # DisbursedAndSettled: 可以回款和预结算订单
    # All: 所有状态
    transaction_status: Optional[NonEmptyStr] = Field(None, alias="orderStatus")
    # 是否返回汇总数据 (0: 否, 1: 是 | 默认 0)
    summarize: Optional[NonNegativeInt] = Field(None, alias="summaryEnabled")
    # 结算金额目标转换货币代码, 默认保持原币种
    currency_code: Optional[CurrencyCode] = Field(None, alias="currencyCode")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v, info: ValidationInfo) -> str:
        dt = utils.validate_datetime(v, False, "查询日期 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)

    @field_validator("transaction_status", mode="before")
    @classmethod
    def _validate_transaction_status(cls, v) -> str | None:
        if v is None:
            return None
        return "DisbursedAndPreSettled" if v == "DisbursedAndSettled" else v

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @model_validator(mode="after")
    def _date_adjustments(self) -> Self:
        # 调整查询维度 & 日期数据
        if self.query_dimension is not None and self.query_dimension == 1:
            self.start_date = self.start_date[:7]
            self.end_date = self.end_date[:7]
        return self


# . Income Statement
class IncomeStatement(IncomeStatementSellers):
    """查询损益报告-产品维度参数"""

    # 搜索字段
    search_field: Optional[NonEmptyStr] = Field(None, alias="searchField")
    # 搜索值
    search_value: Optional[list] = Field(None, alias="searchValue")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("search_value", mode="before")
    @classmethod
    def _validate_search_value(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_non_empty_str(v, "搜索值 search_value")
