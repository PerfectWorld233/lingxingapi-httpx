# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import ValidationInfo, Field, field_validator
from lingxingapi_httpx import utils
from lingxingapi_httpx.base.param import PageOffestAndLength
from lingxingapi_httpx.fields import NonEmptyStr, NonNegativeInt


# 仓库 - 仓库设置 ----------------------------------------------------------------------------------------------------------------
# . Warehouses
class Warehouses(PageOffestAndLength):
    """查询仓库参数"""

    # 仓库类型 (1: 本地仓, 3: 海外仓, 4: 亚马逊平台仓, 6: AWD仓 | 默认: 1)
    warehouse_type: Optional[NonNegativeInt] = Field(alias="type")
    # 海外仓库类型 (1: 无API海外仓, 2: 有API海外仓 | 此参数只在warehouse_type=3时生效)
    overseas_warehouse_type: Optional[NonNegativeInt] = Field(alias="sub_type")
    # 是否已删除 (0: 未删除, 1: 已删除 | 默认: 0)
    deleted: Optional[NonNegativeInt] = Field(alias="is_deleted")


# . Warehouse Bins
class WarehouseBins(PageOffestAndLength):
    """查询仓库货架(仓位)参数"""

    # 仓库IDs (多个ID用逗号分隔)
    warehouse_ids: Optional[str] = Field(None, alias="wid")
    # 仓库货架(仓位)IDs (多个ID用逗号分隔)
    bin_ids: Optional[str] = Field(None, alias="bin_id")
    # 仓库货架(仓位)状态 (1: 启用, 0: 停用)
    bin_status: Optional[NonNegativeInt] = Field(None, alias="status")
    # 仓库货架(仓位)类型 (5: 可用, 6: 次品)
    bin_type: Optional[NonNegativeInt] = Field(None, alias="type")
    # 分页偏移量
    offset: Optional[NonNegativeInt] = None
    # 分页长度
    length: Optional[NonNegativeInt] = Field(None, alias="limit")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("warehouse_ids", mode="before")
    @classmethod
    def _validate_warehouse_ids(cls, v) -> str | None:
        if v is None:
            return None
        ids = utils.validate_array_of_unsigned_int(v, "仓库ID warehouse_ids")
        return ",".join(map(str, ids))

    @field_validator("bin_ids", mode="before")
    @classmethod
    def _validate_bin_ids(cls, v) -> str | None:
        if v is None:
            return None
        ids = utils.validate_array_of_unsigned_int(v, "仓库货架(仓位)ID bin_ids")
        return ",".join(map(str, ids))


# 仓库 - 库存&流水 ---------------------------------------------------------------------------------------------------------------
# . FBA Inventory
class FbaInventory(PageOffestAndLength):
    """查询FBA库存参数"""

    # 领星店铺ID (多个ID用逗号分隔)
    sids: str = Field(alias="sid")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("sids", mode="before")
    @classmethod
    def _validate_sids(cls, v) -> str:
        ids = utils.validate_array_of_unsigned_int(v, "领星店铺ID sids")
        return ",".join(map(str, ids))


# . FBA Inventory Detail
class FbaInventoryDetails(PageOffestAndLength):
    """查询FBA库存详情参数"""

    # fmt: off
    # 搜索字段 ('msku', 'lsku', 'fnsku', 'product_name', 'asin', 'parent_asin', 'spu', 'spu_name')
    search_field: Optional[NonEmptyStr] = None
    # 搜索内容
    search_value: Optional[NonEmptyStr] = None
    # 产品分类ID (多个ID用逗号分隔)
    category_ids: Optional[str] = Field(None, alias="cid")
    # 产品品牌ID (多个ID用逗号分隔)
    brand_ids: Optional[str] = Field(None, alias="bid")
    # 产品负责人
    operator_ids: Optional[str] = Field(None, alias="asin_principal")
    # 产品属性
    attr_value_id: Optional[NonNegativeInt] = Field(None, alias="attribute")
    # 配送方式 ('FBA', 'FBM')
    fulfillment_channel: Optional[NonEmptyStr] = Field(None, alias="fulfillment_channel_type")
    # 产品状态 (0: 停售, 1: 在售)
    status: Optional[NonNegativeInt] = None
    # 是否合并父ASIN (0: 不合并, 1: 合并 | 默认: 0) [暂时不支持]
    # merge_parent_asin: Optional[NonNegativeInt] = Field(0, alias="is_parant_asin_merge")
    # 是否去除零库存 (0: 保留, 1: 去除 | 默认: 0)
    exclude_zero_stock: Optional[NonNegativeInt] = Field(0, alias="is_hide_zero_stock")
    # 是否去除已删除产品 (0: 保留, 1: 去除 | 默认: 0)
    exclude_deleted: Optional[NonNegativeInt] = Field(0, alias="is_contain_del_ls")
    # 是否返回多国店铺本地可售库存信息列表数据
    include_afn_fulfillable_local: NonNegativeInt = Field(1, alias="query_fba_storage_quantity_list")
    # fmt: on

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("search_field", mode="before")
    @classmethod
    def _validate_search_field(cls, v) -> str | None:
        if v is None:
            return None
        if v == "msku":
            return "seller_sku"
        if v == "lsku":
            return "sku"
        return v

    @field_validator("category_ids", mode="before")
    @classmethod
    def _validate_category_ids(cls, v) -> str | None:
        if v is None:
            return None
        ids = utils.validate_array_of_unsigned_int(v, "产品分类IDs category_ids")
        return ",".join(map(str, ids))

    @field_validator("brand_ids", mode="before")
    @classmethod
    def _validate_brand_ids(cls, v) -> str | None:
        if v is None:
            return None
        ids = utils.validate_array_of_unsigned_int(v, "产品品牌IDs brand_ids")
        return ",".join(map(str, ids))

    @field_validator("operator_ids", mode="before")
    @classmethod
    def _validate_operator_ids(cls, v) -> str | None:
        if v is None:
            return None
        ids = utils.validate_array_of_unsigned_int(v, "产品负责人IDs operator_ids")
        return ",".join(map(str, ids)) if ids else None


# . AWD Inventory
class AwdInventory(PageOffestAndLength):
    """查询AWD仓库库存参数"""

    # 搜索字段 ('msku', 'lsku', 'fnsku', 'product_name', 'asin', 'parent_asin', 'spu', 'spu_name')
    search_field: Optional[NonEmptyStr] = None
    # 搜索内容
    search_value: Optional[NonEmptyStr] = None
    # 仓库IDs (多个ID用逗号分隔)
    warehouse_ids: Optional[str] = Field(None, alias="wids")
    # 产品分类IDs (多个ID用逗号分隔)
    category_ids: Optional[str] = Field(None, alias="cid")
    # 产品品牌IDs (多个ID用逗号分隔)
    brand_ids: Optional[str] = Field(None, alias="bid")
    # 产品负责人IDs (多个ID用逗号分隔)
    operator_ids: Optional[str] = Field(None, alias="asin_principal")
    # 产品属性ID
    attr_value_id: Optional[NonNegativeInt] = Field(None, alias="attribute")
    # 产品状态 (0: 停售, 1: 在售)
    status: Optional[NonNegativeInt] = None
    # 是否去除零库存 (0: 保留, 1: 去除 | 默认: 0)
    exclude_zero_stock: Optional[NonNegativeInt] = Field(0, alias="is_hide_zero_stock")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("search_field", mode="before")
    @classmethod
    def _validate_search_field(cls, v) -> str | None:
        if v is None:
            return None
        if v == "msku":
            return "seller_sku"
        if v == "lsku":
            return "sku"
        return v

    @field_validator("warehouse_ids", mode="before")
    @classmethod
    def _validate_warehouse_ids(cls, v) -> str | None:
        if v is None:
            return None
        ids = utils.validate_array_of_unsigned_int(v, "AWD仓库ID warehouse_ids")
        return ",".join(map(str, ids))

    @field_validator("category_ids", mode="before")
    @classmethod
    def _validate_category_ids(cls, v) -> str | None:
        if v is None:
            return None
        ids = utils.validate_array_of_unsigned_int(v, "产品分类IDs category_ids")
        return ",".join(map(str, ids))

    @field_validator("brand_ids", mode="before")
    @classmethod
    def _validate_brand_ids(cls, v) -> str | None:
        if v is None:
            return None
        ids = utils.validate_array_of_unsigned_int(v, "产品品牌IDs brand_ids")
        return ",".join(map(str, ids))

    @field_validator("operator_ids", mode="before")
    @classmethod
    def _validate_operator_ids(cls, v) -> str | None:
        if v is None:
            return None
        ids = utils.validate_array_of_unsigned_int(v, "产品负责人IDs operator_ids")
        return ",".join(map(str, ids))


# . Seller Inventory
class SellerInventory(PageOffestAndLength):
    """卖家(本地/海外)仓库库存参数"""

    # 仓库IDs (多个ID用逗号分隔)
    warehouse_ids: Optional[str] = Field(None, alias="wid")
    # 领星本地SKU
    lsku: Optional[NonEmptyStr] = Field(None, alias="sku")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("warehouse_ids", mode="before")
    @classmethod
    def _validate_warehouse_ids(cls, v) -> str | None:
        if v is None:
            return None
        ids = utils.validate_array_of_unsigned_int(v, "仓库ID warehouse_ids")
        return ",".join(map(str, ids))


# . Seller Inventory Bin
class SellerInventoryBins(PageOffestAndLength):
    """卖家(本地/海外)仓库库存货架(仓位)参数"""

    # 仓库IDs (多个ID用逗号分隔)
    warehouse_ids: Optional[str] = Field(None, alias="wid")
    # 仓库货架(仓位)类型 (多个类型用逗号分隔)
    # (1: 待检暂存, 2: 可用暂存, 3: 次品暂存, 4: 拣货暂存, 5: 可用, 6: 次品)
    bin_types: Optional[str] = Field(None, alias="bin_type_list")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("warehouse_ids", mode="before")
    @classmethod
    def _validate_warehouse_ids(cls, v) -> str | None:
        if v is None:
            return None
        ids = utils.validate_array_of_unsigned_int(v, "仓库ID warehouse_ids")
        return ",".join(map(str, ids))

    @field_validator("bin_types", mode="before")
    @classmethod
    def _validate_bin_types(cls, v) -> str | None:
        if v is None:
            return None
        types = utils.validate_array_of_unsigned_int(v, "仓库货架(仓位)类型 bin_types")
        return ",".join(map(str, types)) if types else None


# . Seller Inventory Batch
class SellerInventoryBatches(PageOffestAndLength):
    """查询卖家(本地/海外)仓库出入库批次参数"""

    # fmt: off
    # 搜索字段 
    # ('msku', 'lsku', 'fnsku', 'product_name', 'transaction_number', 'batch_number') 
    # ('source_batch_number', 'purchase_plan_number', 'purchase_number', 'receiving_number')
    search_field: Optional[NonEmptyStr] = None
    # 搜索内容
    search_value: Optional[NonEmptyStr] = None
    # 仓库IDs (多个ID用逗号分隔)
    warehouse_ids: Optional[str] = Field(None, alias="wids")
    # 出入库类型 (多个类型用逗号分隔)
    # (19: 其他入库, 22: 采购入库, 24: 调拨入库, 23: 委外入库, 25: 盘盈入库)
    # (16: 换标入库, 17: 加工入库, 18: 拆分入库, 26: 退货入库, 27: 移除入库, 45: 赠品入库)
    transaction_types: Optional[str] = Field(None, alias="stock_in_type_list")
    # 去除零库存 (0: 保留, 1: 去除 | 默认: 0)
    exclude_zero_stock: Optional[NonNegativeInt] = Field(0, alias="show_zero_stock", ge=0, le=1)
    # fmt: on

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("search_field", mode="before")
    @classmethod
    def _validate_search_field(cls, v) -> str | None:
        if v is None:
            return None
        if v == "seller_sku":
            return "msku"
        if v == "lsku":
            return "sku"
        if v == "transaction_number":
            return "order_sn"
        if v == "purchase_plan_number":
            return "purchase_plan"
        if v == "purchase_number":
            return "purchase_order"
        if v == "receiving_number":
            return "receipt_order"
        return v

    @field_validator("warehouse_ids", mode="before")
    @classmethod
    def _validate_warehouse_ids(cls, v) -> str | None:
        if v is None:
            return None
        ids = utils.validate_array_of_unsigned_int(v, "仓库ID warehouse_ids")
        return ",".join(map(str, ids))

    @field_validator("transaction_types", mode="before")
    @classmethod
    def _validate_transaction_types(cls, v) -> str | None:
        if v is None:
            return None
        types = utils.validate_array_of_unsigned_int(v, "出入库类型 transaction_types")
        return ",".join(map(str, types)) if types else None

    @field_validator("exclude_zero_stock", mode="after")
    @classmethod
    def _validate_exclude_zero_stock(cls, v: None | int) -> int | None:
        return None if v is None else 0 if v else 1


# . Seller Inventory Records
class SellerInventoryRecords(PageOffestAndLength):
    """查询卖家(本地/海外)仓库出入库批次记录参数"""

    # 搜索字段
    # ('msku', 'lsku', 'fnsku', 'product_name', 'transaction_number', 'batch_number')
    # ('source_batch_number', 'purchase_plan_number', 'purchase_number', 'receiving_number')
    search_field: Optional[NonEmptyStr] = None
    # 搜索内容
    search_value: Optional[NonEmptyStr] = None
    # 仓库IDs (多个ID用逗号分隔)
    warehouse_ids: Optional[str] = Field(None, alias="wid_list")
    # 出入库类型 (多个类型用逗号分隔)
    # (19: 其他入库, 22: 采购入库, 24: 调拨入库, 23: 委外入库, 25: 盘盈入库)
    # (16: 换标入库, 17: 加工入库, 18: 拆分入库, 47: VC-PO出库, 48: VC-DF出库)
    # (42: 其他出库, 41: 调拨出库, 32: 委外出库, 33: 盘亏出库, 34: 换标出库)
    # (35: 加工出库, 36: 拆分出库, 37: FBA出库, 38: FBM出库, 39: 退货出库)
    # (26: 退货入库, 27: 移除入库, 28: 采购质检, 29: 委外质检, 71: 采购上架)
    # (72: 委外上架, 65: WFS出库, 45: 赠品入库, 46: 赠品质检入库, 73: 赠品上架)
    # (201: 期初成本调整, 202: 尾差成本调整)
    transaction_types: Optional[str] = Field(None, alias="statement_type_list")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("search_field", mode="before")
    @classmethod
    def _validate_search_field(cls, v) -> str | None:
        if v is None:
            return None
        if v == "seller_sku":
            return "msku"
        if v == "lsku":
            return "sku"
        if v == "transaction_number":
            return "order_sn"
        if v == "purchase_plan_number":
            return "purchase_plan"
        if v == "purchase_number":
            return "purchase_order"
        if v == "receiving_number":
            return "receipt_order"
        return v

    @field_validator("warehouse_ids", mode="before")
    @classmethod
    def _validate_warehouse_ids(cls, v) -> str | None:
        if v is None:
            return None
        ids = utils.validate_array_of_unsigned_int(v, "仓库ID warehouse_ids")
        return ",".join(map(str, ids))

    @field_validator("transaction_types", mode="before")
    @classmethod
    def _validate_transaction_types(cls, v) -> str | None:
        if v is None:
            return None
        types = utils.validate_array_of_unsigned_int(v, "出入库类型 transaction_types")
        return ",".join(map(str, types)) if types else None


# . Seller Inventory Operations
class SellerInventoryOperations(PageOffestAndLength):
    """卖家(本地/海外)仓库库存操作流水参数"""

    # 仓库IDs (多个ID用逗号分隔)
    warehouse_ids: Optional[str] = Field(None, alias="wids")
    # 出入库操作类型 (多个类型用逗号分隔)
    # (19: 其他入库, 22: 采购入库, 24: 调拨入库, 23: 委外入库, 25: 盘盈入库)
    # (16: 换标入库, 17: 加工入库, 18: 拆分入库, 47: VC-PO出库, 48: VC-DF出库)
    # (42: 其他出库, 41: 调拨出库, 32: 委外出库, 33: 盘亏出库, 34: 换标出库)
    # (35: 加工出库, 36: 拆分出库, 37: FBA出库, 38: FBM出库, 39: 退货出库)
    # (26: 退货入库, 27: 移除入库, 28: 采购质检, 29: 委外质检, 71: 采购上架)
    # (72: 委外上架, 65: WFS出库, 45: 赠品入库, 46: 赠品质检入库, 73: 赠品上架)
    # (201: 期初成本调整, 202: 尾差成本调整)
    transaction_types: Optional[str] = Field(None, alias="types")
    # 出入库操作子类型 (多个类型用逗号分隔)
    # (1901: 其他入库 手工其他入库, 1902: 其他入库 用户初始化, 1903: 其他入库 系统初始化)
    # (2201: 采购入库 手工采购入库, 2202: 采购入库 采购单创建入库单, 2801: 采购质检 质检)
    # (7101: 采购上架 PDA上架入库, 7201: 委外上架 PDA委外上架, 2401: 调拨入库 调拨单入在途)
    # (2402: 调拨入库 调拨单收货, 2403: 调拨入库 备货单入在途, 2404: 调拨入库 备货单收货)
    # (2405: 调拨入库 备货单入库结束到货, 2301: 委外入库 委外订单完成加工后入库)
    # (2901: 委外质检 委外订单质检, 2501: 盘盈入库 盘点单入库, 2502: 盘盈入库 数量调整单正向)
    # (1501: FBM退货 退货入库, 1502: FBM退货 退货入库质检, 1601: 换标入库 换标调整入库)
    # (1701: 加工入库 加工单入库, 1702: 加工入库 委外订单加工入库, 1801: 拆分入库 拆分单入库)
    # (2601: 自动退货入库, 2602: 手动退货入库, 2701: 移除入库, 4201: 其他出库 手工其他出库)
    # (4101: 调拨出库 调拨单出库, 4102: 调拨出库 备货单出库, 3201: 委外出库 委外订单完成加工后出库)
    # (3301: 盘亏出库 盘点单出库, 3302: 盘亏出库 数量调整单负向, 3401: 换标出库 换标调整出库)
    # (3501: 加工出库 加工单出库, 3502: 加工出库 委外订单加工出库, 3601: 拆分出库 拆分单出库)
    # (3701: FBA出库 发货单出库, 3702: FBA出库 手工FBA出库, 3801: FBM出库 销售出库单)
    # (3901: 退货出库 手工退货出库, 3902: 退货出库 采购单生成的退货出库单, 10001: 库存锁定-出库)
    # (10002: 库存锁定-调拨, 10003: 库存锁定-调整, 10004: 库存锁定-加工, 10005: 库存锁定-加工计划)
    # (10006: 库存锁定-拆分, 10007: 库存锁定-海外备货, 10008: 库存锁定-发货, 10009: 库存锁定-自发货)
    # (10010: 库存锁定-主动释放, 10012: 库存锁定-发货拣货, 10013: 库存锁定-发货计划)
    # (10014: 库存锁定-WFS库存调整, 10011: 仓位转移和一键上架)
    transaction_sub_types: Optional[str] = Field(None, alias="sub_types")
    # 操作开始日期, 闭合区间
    start_date: Optional[NonEmptyStr] = None
    # 操作结束日期, 闭合区间
    end_date: Optional[NonEmptyStr] = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("warehouse_ids", mode="before")
    @classmethod
    def _validate_warehouse_ids(cls, v) -> str | None:
        if v is None:
            return None
        ids = utils.validate_array_of_unsigned_int(v, "仓库ID warehouse_ids")
        return ",".join(map(str, ids))

    @field_validator("transaction_types", mode="before")
    @classmethod
    def _validate_transaction_types(cls, v) -> str | None:
        if v is None:
            return None
        types = utils.validate_array_of_unsigned_int(v, "出入库类型 transaction_types")
        return ",".join(map(str, types)) if types else None

    @field_validator("transaction_sub_types", mode="before")
    @classmethod
    def _validate_transaction_sub_types(cls, v) -> str | None:
        if v is None:
            return None
        sub_types = utils.validate_array_of_unsigned_int(
            v, "出入库子类型 transaction_sub_types"
        )
        return ",".join(map(str, sub_types)) if sub_types else None

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v: Optional[str], info: ValidationInfo) -> str | None:
        if v is None:
            return None
        dt = utils.validate_datetime(v, False, "操作时间 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)


# . Seller Inventory Bin Records
class SellerInventoryBinRecords(PageOffestAndLength):
    """查询卖家(本地/海外)仓库货架(仓位)出入流水参数"""

    # 仓库IDs (多个ID用逗号分隔)
    warehouse_ids: Optional[str] = Field(None, alias="wid")
    # 出入库类型 (多个类型用逗号分隔)
    # (16: 换标入库, 17: 加工入库, 18: 拆分入库, 19: 其他入库, 22: 采购入库, 23: 委外入库)
    # (24: 调拨入库, 25: 盘盈入库, 26: 退货入库, 27: 移除入库, 28: 采购质检, 29: 委外质检)
    # (32: 委外出库, 33: 盘亏出库, 34: 换标出库, 35: 加工出库, 36: 拆分出库, 37: FBA出库)
    # (38: FBM出库, 39: 退货出库, 41: 调拨出库, 42: 其他出库, 65: WFS出库, 71: 采购上架)
    # (72: 委外上架, 100: 库存调整, 200: 成本补录, 30001: 已撤销)
    transaction_types: Optional[str] = Field(None, alias="type")
    # 仓库货架(仓位)类型 (多个类型用逗号分隔)
    # (1: 待检暂存, 2: 可用暂存, 3: 次品暂存, 4: 拣货暂存, 5: 可用, 6: 次品)
    bin_types: Optional[str] = Field(None, alias="bin_type_list")
    # 操作开始日期, 闭合区间
    start_date: Optional[NonEmptyStr] = None
    # 操作结束日期, 闭合区间
    end_date: Optional[NonEmptyStr] = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("warehouse_ids", mode="before")
    @classmethod
    def _validate_warehouse_ids(cls, v) -> str | None:
        if v is None:
            return None
        ids = utils.validate_array_of_unsigned_int(v, "仓库ID warehouse_ids")
        return ",".join(map(str, ids))

    @field_validator("transaction_types", mode="before")
    @classmethod
    def _validate_transaction_types(cls, v) -> str | None:
        if v is None:
            return None
        types = utils.validate_array_of_unsigned_int(v, "出入库类型 transaction_types")
        return ",".join(map(str, types)) if types else None

    @field_validator("bin_types", mode="before")
    @classmethod
    def _validate_bin_types(cls, v) -> str | None:
        if v is None:
            return None
        types = utils.validate_array_of_unsigned_int(v, "仓库货架(仓位)类型 bin_types")
        return ",".join(map(str, types)) if types else None

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v: Optional[str], info: ValidationInfo) -> str | None:
        if v is None:
            return None
        dt = utils.validate_datetime(v, False, "操作时间 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)
