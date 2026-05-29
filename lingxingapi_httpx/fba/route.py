# -*- coding: utf-8 -*-

# fmt: off
# FBA - FBA货件 (STA) ----------------------------------------------------------------------------------------------------------
# https://apidoc.lingxing.com/#/docs/FBA/QuerySTATaskList
STA_PLANS: str = "/amzStaServer/openapi/inbound-plan/page"
# https://apidoc.lingxing.com/#/docs/FBA/StaTaskDetail
STA_PLAN_DETAIL: str = "/amzStaServer/openapi/inbound-plan/detail"
# https://apidoc.lingxing.com/#/docs/FBA/ListPackingGroupItems
PACKING_GROUPS: str = "/amzStaServer/openapi/inbound-packing/listPackingGroupItems"
# https://apidoc.lingxing.com/#/docs/FBA/QuerySTATaskBoxInformation
PACKING_GROUP_BOXES: str = "/amzStaServer/openapi/inbound-plan/listInboundPlanGroupPacking"
# https://apidoc.lingxing.com/#/docs/FBA/ShipmentPreView
PLACEMENT_OPTIONS: str = "/amzStaServer/openapi/inbound-shipment/shipmentPreView"
# https://apidoc.lingxing.com/#/docs/FBA/getInboundPackingBoxInfo
PLACEMENT_OPTION_BOXES: str = "/amzStaServer/openapi/inbound-packing/getInboundPackingBoxInfo"
# https://apidoc.lingxing.com/#/docs/FBA/FBAShipmentList
SHIPMENTS: str = "/erp/sc/data/fba_report/shipmentList"
# https://apidoc.lingxing.com/#/docs/FBA/ShipmentDetailList
SHIPMENT_DETAILS: str = "/amzStaServer/openapi/inbound-shipment/shipmentDetailList"
# https://apidoc.lingxing.com/#/docs/FBA/ListShipmentBoxes
SHIPMENT_BOXES: str = "/amzStaServer/openapi/inbound-shipment/listShipmentBoxes"
# https://apidoc.lingxing.com/#/docs/FBA/GetTransportList
SHIPMENT_TRANSPORTS: str = "/amzStaServer/openapi/inbound-shipment/getTransportList"
# https://apidoc.lingxing.com/#/docs/FBA/FBAReceivedInventory
SHIPMENT_RECEIPT_RECORDS: str = "/erp/sc/data/fba_report/receivedInventory"
# https://apidoc.lingxing.com/#/docs/FBA/ShoppingAddress
SHIPMENT_DELIVERY_ADDRESS: str = "/basicOpen/openapi/fbaShipment/shoppingAddress"
# https://apidoc.lingxing.com/#/docs/FBA/ShipFromAddressList
SHIP_FROM_ADDRESSES: str = "/erp/sc/routing/fba/shipment/shipFromAddressList"
