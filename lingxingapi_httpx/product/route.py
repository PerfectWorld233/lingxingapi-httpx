# -*- coding: utf-8 -*-

# 产品 --------------------------------------------------------------------------------------------------------------------------
# https://apidoc.lingxing.com/#/docs/Product/ProductLists
PRODUCTS: str = "/erp/sc/routing/data/local_inventory/productList"
# https://apidoc.lingxing.com/#/docs/Product/batchGetProductInfo
PRODUCT_DETAILS: str = "/erp/sc/routing/data/local_inventory/batchGetProductInfo"
# https://apidoc.lingxing.com/#/docs/Product/productOperateBatch
ENABLE_DISABLE_PRODUCTS: str = "/basicOpen/product/productManager/product/operate/batch"
# https://apidoc.lingxing.com/#/docs/Product/SetProduct
EDIT_PRODUCT: str = "/erp/sc/routing/storage/product/set"
# https://apidoc.lingxing.com/#/docs/Product/spuList
SPU_PRODUCTS: str = "/erp/sc/routing/storage/spu/spuList"
# https://apidoc.lingxing.com/#/docs/Product/spuInfo
SPU_PRODUCT_DETAIL: str = "/erp/sc/routing/storage/spu/info"
# https://apidoc.lingxing.com/#/docs/Product/spuSet
EDIT_SPU_PRODUCT: str = "/erp/sc/routing/storage/spu/set"
# https://apidoc.lingxing.com/#/docs/Product/bundledProductList
BUNDLE_PRODUCTS: str = "/erp/sc/routing/data/local_inventory/bundledProductList"
# https://apidoc.lingxing.com/#/docs/Product/SetBundled
EDIT_BUNDLE_PRODUCT: str = "/erp/sc/routing/storage/product/setBundled"
# https://apidoc.lingxing.com/#/docs/Product/productAuxList
AUXILIARY_MATERIALS: str = "/erp/sc/routing/data/local_inventory/productAuxList"
# https://apidoc.lingxing.com/#/docs/Product/setAux
EDIT_AUXILIARY_MATERIAL: str = "/erp/sc/routing/storage/product/setAux"
# https://apidoc.lingxing.com/#/docs/Product/UpcList
PRODUCT_CODES: str = "/listing/publish/api/upc/upcList"
# https://apidoc.lingxing.com/#/docs/Product/AddCommodityCode
CREATE_PRODUCT_CODE: str = "/listing/publish/api/upc/addCommodityCode"
# https://apidoc.lingxing.com/#/docs/Product/GetProductTag
PRODUCT_GLOBAL_TAGS: str = "/label/operation/v1/label/product/list"
# https://apidoc.lingxing.com/#/docs/Product/CreateProductTag
CREATE_PRODUCT_GLOBAL_TAG: str = "/label/operation/v1/label/product/create"
# https://apidoc.lingxing.com/#/docs/Product/SetProductTag
SET_PRODUCT_TAG: str = "/label/operation/v1/label/product/mark"
# https://apidoc.lingxing.com/#/docs/Product/DelProductTag
UNSET_PRODUCT_TAG: str = "/label/operation/v1/label/product/unmarkLabel"
# https://apidoc.lingxing.com/#/docs/Product/attributeList
PRODUCT_GLOBAL_ATTRIBUTES: str = "/erp/sc/routing/storage/attribute/attributeList"
# https://apidoc.lingxing.com/#/docs/Product/attributeSet
EDIT_PRODUCT_GLOBAL_ATTRIBUTE: str = "/erp/sc/routing/storage/attribute/set"
# https://apidoc.lingxing.com/#/docs/Product/Brand
PRODUCT_BRANDS: str = "/erp/sc/data/local_inventory/brand"
# https://apidoc.lingxing.com/#/docs/Product/SetBrand
EDIT_PRODUCT_BRANDS: str = "/erp/sc/storage/brand/set"
# https://apidoc.lingxing.com/#/docs/Product/Category
PRODUCT_CATEGORIES: str = "/erp/sc/routing/data/local_inventory/category"
# https://apidoc.lingxing.com/#/docs/Product/SetCategory
EDIT_PRODUCT_CATEGORIES: str = "/erp/sc/routing/storage/category/set"
