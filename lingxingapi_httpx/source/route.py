# -*- coding: utf-8 -*-

# fmt: off
# 订单数据 -----------------------------------------------------------------------------------------------------------------------
# https://apidoc.lingxing.com/#/docs/SourceData/AllOrders
ORDERS: str = "/erp/sc/data/mws_report/allOrders"
# https://apidoc.lingxing.com/#/docs/SourceData/FbaOrders
FBA_ORDERS: str = "/erp/sc/data/mws_report/fbaOrders"
# https://apidoc.lingxing.com/#/docs/SourceData/fbaExchangeOrderList
FBA_REPLACEMENT_ORDERS: str = "/erp/sc/routing/data/order/fbaExchangeOrderList"
# https://apidoc.lingxing.com/#/docs/SourceData/RefundOrders
FBA_RETURN_ORDERS: str = "/erp/sc/data/mws_report/refundOrders"
# https://apidoc.lingxing.com/#/docs/SourceData/v1getAmazonFulfilledShipmentsList
FBA_SHIPMENTS_V1: str = "/erp/sc/data/mws_report_v1/getAmazonFulfilledShipmentsList"
# https://apidoc.lingxing.com/#/docs/SourceData/fbmReturnOrderList
FBM_RETURN_ORDERS: str = "/erp/sc/routing/data/order/fbmReturnOrderList"

# FBA 库存数据 -------------------------------------------------------------------------------------------------------------------
# https://apidoc.lingxing.com/#/docs/SourceData/RemovalOrderListNew
FBA_REMOVAL_ORDERS: str = "/erp/sc/routing/data/order/removalOrderListNew"
# https://apidoc.lingxing.com/#/docs/SourceData/RemovalShipmentList
FBA_REMOVAL_SHIPMENTS: str = "/erp/sc/statistic/removalShipment/list"
# https://apidoc.lingxing.com/#/docs/SourceData/ManageInventory
FBA_INVENTORY: str = "/erp/sc/data/mws_report/manageInventory"
# https://apidoc.lingxing.com/#/docs/SourceData/AfnFulfillableQuantity
FBA_RESERVED_INVENTORY: str = "/erp/sc/data/mws_report/reservedInventory"
# https://apidoc.lingxing.com/#/docs/SourceData/getFbaAgeList
FBA_INVENTORY_HEALTH: str = "/erp/sc/routing/fba/fbaStock/getFbaAgeList"
# https://apidoc.lingxing.com/#/docs/SourceData/AdjustmentList
FBA_INVENTORY_ADJUSTMENTS: str = "/basicOpen/openapi/mwsReport/adjustmentList"

# 导出报告 -----------------------------------------------------------------------------------------------------------------------
# https://apidoc.lingxing.com/#/docs/Statistics/reportCreateReportExportTask
EXPORT_REPORT_TASK: str = "/basicOpen/report/create/reportExportTask"
# https://apidoc.lingxing.com/#/docs/Statistics/reportQueryReportExportTask
EXPORT_REPORT_RESULT: str = "/basicOpen/report/query/reportExportTask"
# https://apidoc.lingxing.com/#/docs/Statistics/AmazonReportExportTask
EXPORT_REPORT_REFRESH: str = "/basicOpen/report/amazonReportExportTask"
