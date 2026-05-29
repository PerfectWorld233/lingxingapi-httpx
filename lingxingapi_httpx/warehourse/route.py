# -*- coding: utf-8 -*-

# fmt: off
# 仓库 - 仓库设置 ----------------------------------------------------------------------------------------------------------------
# https://apidoc.lingxing.com/#/docs/Warehouse/WarehouseLists
WAREHOUSES: str = "/erp/sc/data/local_inventory/warehouse"
# https://apidoc.lingxing.com/#/docs/Warehouse/warehouseBin
WAREHOUSE_BINS: str = "/erp/sc/routing/data/local_inventory/warehouseBin"

# 仓库 - 库存&流水 ---------------------------------------------------------------------------------------------------------------
# https://apidoc.lingxing.com/#/docs/Warehouse/FBAStock
FBA_INVENTORY: str = "/erp/sc/routing/fba/fbaStock/fbaList"
# https://apidoc.lingxing.com/#/docs/Warehouse/FBAStock_v2
FBA_INVENTORY_DETAILS: str = "/basicOpen/openapi/storage/fbaWarehouseDetail"
# https://apidoc.lingxing.com/#/docs/Warehouse/AwdWarehouseDetail
AWD_INVENTORY: str = "/basicOpen/openapi/storage/awdWarehouseDetail"
# https://apidoc.lingxing.com/#/docs/Warehouse/InventoryDetails
SELLER_INVENTORY: str = "/erp/sc/routing/data/local_inventory/inventoryDetails"
# https://apidoc.lingxing.com/#/docs/Warehouse/inventoryBinDetails
SELLER_INVENTORY_BINS: str = "/erp/sc/routing/data/local_inventory/inventoryBinDetails"
# https://apidoc.lingxing.com/#/docs/Warehouse/GetBatchDetailList
SELLER_INVENTORY_BATCHES: str = "/erp/sc/routing/data/local_inventory/getBatchDetailList"
# https://apidoc.lingxing.com/#/docs/Warehouse/GetBatchStatementList
SELLER_INVENTORY_RECORDS: str ="/erp/sc/routing/data/local_inventory/getBatchStatementList"
# https://apidoc.lingxing.com/#/docs/Warehouse/WarehouseStatementNew
SELLER_INVENTORY_OPERATIONS: str = "/erp/sc/routing/inventoryLog/WareHouseInventory/wareHouseCenterStatement"
# https://apidoc.lingxing.com/#/docs/Warehouse/wareHouseBinStatement
SELLER_INVENTORY_BIN_RECORDS: str = "/erp/sc/routing/data/local_inventory/wareHouseBinStatement"
