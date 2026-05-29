# -*- coding: utf-8 -*-

# fmt: off
# 用户自定义费用管理 --------------------------------------------------------------------------------------------------------------
# https://apidoc.lingxing.com/#/docs/Finance/feeManagementType
USER_FEE_TYPES: str = "/bd/fee/management/open/feeManagement/otherFee/type"

# 亚马逊交易数据 -----------------------------------------------------------------------------------------------------------------
# https://apidoc.lingxing.com/#/docs/Finance/settlementTransactionList
TRANSACTIONS: str = "/bd/sp/api/open/settlement/transaction/detail/list"
# https://apidoc.lingxing.com/#/docs/Finance/settlementSummaryList
SETTLEMENTS: str = "/bd/sp/api/open/settlement/summary/list"
# https://apidoc.lingxing.com/#/docs/Finance/SettlementReport
SHIPMENT_SETTLEMENT: str = "/cost/center/api/settlement/report"
# https://apidoc.lingxing.com/#/docs/Finance/receivableReportList
RECEIVABLES: str = "/bd/sp/api/open/monthly/receivable/report/list"

# 亚马逊库存数据 -----------------------------------------------------------------------------------------------------------------
# https://apidoc.lingxing.com/#/docs/Finance/centerOdsDetailQuery
LEDGER_DETAIL: str = "/cost/center/ods/detail/query"
# https://apidoc.lingxing.com/#/docs/Finance/summaryQuery
LEDGER_SUMMARY: str = "/cost/center/ods/summary/query"
# https://apidoc.lingxing.com/#/docs/Finance/CostStream
LEDGER_VALUATION: str = "/cost/center/api/cost/stream"

# 亚马逊广告数据 -----------------------------------------------------------------------------------------------------------------
# https://apidoc.lingxing.com/#/docs/Finance/InvoiceList
ADS_INVOICES: str = "/bd/profit/report/open/report/ads/invoice/list"
# https://apidoc.lingxing.com/#/docs/Finance/InvoiceDetail
ADS_INVOICE_DETAIL: str = "/bd/profit/report/open/report/ads/invoice/detail"
# https://apidoc.lingxing.com/#/docs/Finance/InvoiceCampaignList
ADS_CAMPAIGN_INVOICES: str = "/bd/profit/report/open/report/ads/invoice/campaign/list"

# 亚马逊损益报告 -----------------------------------------------------------------------------------------------------------------
# https://apidoc.lingxing.com/#/docs/Finance/bdSeller
INCOME_STATEMENT_SELLERS: str = "/bd/profit/report/open/report/seller/list"
# https://apidoc.lingxing.com/#/docs/Finance/bdASIN
INCOME_STATEMENT_ASINS: str = "/bd/profit/report/open/report/asin/list"
# https://apidoc.lingxing.com/#/docs/Finance/bdParentASIN
INCOME_STATEMENT_PARENT_ASINS: str = "/bd/profit/report/open/report/parent/asin/list"
# https://apidoc.lingxing.com/#/docs/Finance/bdMSKU
INCOME_STATEMENT_MSKUS: str = "/bd/profit/report/open/report/msku/list"
# https://apidoc.lingxing.com/#/docs/Finance/bdSKU
INCOME_STATEMENT_LSKUS: str = "/bd/profit/report/open/report/sku/list"
