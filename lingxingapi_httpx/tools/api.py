# -*- coding: utf-8 -*-c
import datetime
from typing import Literal
from lingxingapi_httpx import errors
from lingxingapi_httpx.base.api import BaseAPI
from lingxingapi_httpx.tools import param, route, schema

# Type Aliases ---------------------------------------------------------------------------------------------------------
ALERT_SEARCH_FIELD = Literal["rule_name", "asin", "msku"]


# API ------------------------------------------------------------------------------------------------------------------
class ToolsAPI(BaseAPI):
    """领星API `工具数据` 接口

    ## Notice
    请勿直接实例化此类
    """

    # 公共 API --------------------------------------------------------------------------------------
    async def MonitorKeywords(
        self,
        *,
        mid: int | None = None,
        start_date: str | datetime.date | datetime.datetime | None = None,
        end_date: str | datetime.date | datetime.datetime | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.MoniterKeywords:
        """查询关键词监控

        ## Docs
        - 工具: [关键词列表](https://apidoc.lingxing.com/#/docs/Tools/GetKeywordList)

        :param mid `<'str/None'>`: 领星站点ID列表 (Seller.mid), 默认 `None` (不筛选)
        :param start_date `<'str/date/datetime/None'>`: 关键词监控创建开始日期,
            参数来源 `MonitorKeyword.monitor_keyword_create_time`, 默认 `None` (不筛选)
        :param end_date `<'str/date/datetime/None'>`: 关键词监控创建结束日期,
            参数来源 `MonitorKeyword.monitor_keyword_create_time`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 最大值 2000, 默认 `None` (使用: 20)
        :return `<'MoniterKeywords'>`: 查询到的关键词监控结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 关键词监控ID [原字段 'id']
                    "moniter_id": 44118,
                    # 关键词 [原字段 'key_word']
                    "keyword": "65 ink cartridge for hp printers",
                    # 关键词数量 [原字段 'keyword_num']
                    "keyword_count": 70,
                    # 关键词备注 [原字段 'keyword_remark']
                    "keyword_note": "",
                    # 监控终端 (1: PC端, 2: 移动端) [原字段 'type']
                    "moniter_type": 1,
                    # 监控国家 [原字段 'country']
                    "monitor_country": "美国",
                    # 监控邮编城市 [原字段 'postcode_name']
                    "monitor_city": "New york",
                    # 监控邮编 [原字段 'postcode']
                    "monitor_postcode": "10008",
                    # 监控排名类型 (0: 自然排名, 1: 广告排名) [原字段 'is_sponsored']
                    "rank_type": 0,
                    # 关键词排名
                    "rank": 75,
                    # 关键词排名页面 [原字段 'page']
                    "page": 5,
                    # 关键词页面排名 [原字段 'current_page_rank']
                    "page_rank": 11,
                    # 关键词排名描述 [原字段 'rank_text']
                    "rank_desc": "75(第5页第11名)",
                    # SBV广告排名页面 [原字段 'sbv_page']
                    "sbv_page": -1,
                    # SBV广告排名描述 [原字段 'sbv_text']
                    "sbv_desc": "",
                    # 关键词ASIN
                    "asin": "B0DP8QGQN7",
                    # 关键词父ASIN
                    "parent_asin": "",
                    # ASIN标题
                    "title": "",
                    # ASIN备注 [原字段 'asin_remark']
                    "asin_note": "",
                    # 监控创建人
                    "monitor_creator_name": "周思琪",
                    # 监控人列表
                    "monitor_user_names": ["周思琪"],
                    # ASIN监控创建时间 [原字段 'asin_create_time']
                    "monitor_asin_create_time": "2025-09-10 15:22",
                    # 关键词监控创建时间 [原字段 'create_time']
                    "monitor_keyword_create_time": "2025-09-10 15:23",
                    # 监控更新时间 [原字段 'monitor_time']
                    "update_time": "2025-09-17 02:00",
                },
                ...
            ]
        }
        ```
        """
        url = route.MONITOR_KEYWORDS
        # 构建参数
        args = {
            "mid": mid,
            "start_date": start_date,
            "end_date": end_date,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.MonitorKeywords.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.MoniterKeywords.model_validate(data)

    async def MonitorAsins(
        self,
        *,
        start_time: str | datetime.date | datetime.datetime | None = None,
        end_time: str | datetime.date | datetime.datetime | None = None,
        monitor_levels: int | list[int] | None = None,
        search_value: str | list[str] | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.MoniterAsins:
        """查询ASIN监控

        ## Docs
        - 工具: [查询竞品监控列表](https://apidoc.lingxing.com/#/docs/Tools/CompetitiveMonitorList)

        :param start_time `<'str/date/datetime/None'>`: 更新开始时间, 默认 `None` (不筛选)
        :param end_time `<'str/date/datetime/None'>`: 更新结束时间, 默认 `None` (不筛选)
        :param monitor_levels `<'int/list[int]/None'>`: 监控等级编码或编码列表 (1: A, 2: B, 3: C, 4: D), 默认 `None` (不筛选)
        :param search_value `<'str/list[str]/None'>`: 搜索值, ASIN或ASIN列表, 默认 `None` (不筛选)
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 最大值 200, 默认 `None` (使用: 20)
        :return `<'MoniterAsins'>`: 查询到的ASIN监控结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 监控状态 (0: 关闭, 1: 开启)
                    "monitor_status": 1,
                    # 监控等级 (1: A, 2: B, 3: C, 4: D) [原字段 'level_name']
                    "monitor_level": "A",
                    # 领星站点ID
                    "mid": 5,
                    # 监控ASIN
                    "asin": "B0B*******",
                    # 父ASIN [原字段 'parent']
                    "parent_asin": "",
                    # 关联的子ASIN列表 [原字段 'children']
                    "child_asins": [],
                    # ASIN链接
                    "asin_url": "https://www.amazon.de/dp/B0B*******",
                    # 商品主图 [原字段 'main_image']
                    "image_url": "https://m.media-amazon.com/images/I/****.jpg",
                    # ASIN所属类目列表 [原字段 'category_list']
                    "asin_categories": [],
                    # 商品价格
                    "price": 32.98,
                    # 商品价格货币符号 [原字段 'currency']
                    "price_currency_icon": "€",
                    # BuyBox当前价格
                    "buybox_price": 32.98,
                    # BuyBox初始价格 [原字段 'init_buybox_price']
                    "buybox_init_price": 32.99,
                    # BuyBox价格货币符号 [原字段 'buybox_currency']
                    "buybox_currency_icon": "€",
                    # BuyBox美元价格
                    "buybox_usd_price": 35.6,
                    # 30天平均价格 [原字段 'avg_price']
                    "price_avg_30d": 0.0,
                    # 30天平均价格货币符号 [原字段 'avg_currency']
                    "price_avg_currency_icon": "$",
                    # 30天预估销量 [原字段 'bought_num']
                    "sales_qty_30d": 2000,
                    # 评论分 [原字段 'star']
                    "review_score": "4.2",
                    # 评论数 [原字段 'review_num']
                    "review_count": "16",
                    # 大类目名称 [原字段 'big_category']
                    "category": "Computer & Zubehör",
                    # 大类目排名 [原字段 'big_category_rank']
                    "category_rank": "670",
                    # 大类目初始排名 [原字段 'init_big_category_rank']
                    "category_init_rank": 355,
                    # 小类目排名 [原字段 'small_ranks']
                    "subcategories": [
                        {
                            # 小类目名称 [原字段 'small_category_text']
                            "subcategory": "Tintenpatronen für Tintenstrahldrucker",
                            # 小类目排名 [原字段 'small_rank']
                            "subcategory_rank": 73,
                            # 小类目初始排名 [原字段 'init_small_rank']
                            "subcategory_init_rank": 44,
                        },
                        ...
                    ],
                    # FBA卖家数量 [原字段 'fba_seller_num']
                    "fba_seller_count": 1,
                    # 初始FBA卖家数量 [原字段 'init_fba_seller_num']
                    "fba_seller_init_count": 0,
                    # FBM卖家数量 [原字段 'fbm_seller_num']
                    "fbm_seller_count": 0,
                    # 初始FBM卖家数量 [原字段 'init_fbm_seller_num']
                    "fbm_seller_init_count": 0,
                    # 商品重量
                    "item_weight": " 130 Gramm",
                    # 商品尺寸
                    "product_dimensions": "4,2 x 14,7 x 7,4 cm",
                    # 搜索词
                    "search_term": "",
                    # 最新更新事件列表 [原字段 'last_update_event']
                    "latest_update_events": ["优惠券价格"],
                    # 商品图片列表 [原字段 'thumbnail']
                    "images": [
                        "https://m.media-amazon.com/images/I/****.jpg",
                        ...
                    ],
                    # 商品标题
                    "title": "Product Title",
                    # 商品卖点 [原字段 'featurebullets']
                    "bullet_points": [
                        "bullet point 1",
                        ...
                    ],
                    # 监控创建人ID [原字段 'creator_uid']
                    "creator_id": "106*****",
                    # 监控创建人名称 [原字段 'creator']
                    "creator_name": "白小白",
                    # 监控人ID列表 [原字段 'monitor_uids']
                    "monitor_user_ids": ["106*****"],
                }
                ...
            ]
        }
        ```
        """
        url = route.MONITOR_ASINS
        # 构建参数
        args = {
            "start_time": start_time,
            "end_time": end_time,
            "monitor_levels": monitor_levels,
            "search_field": "asin",
            "search_value": search_value,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.MonitorAsins.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.MoniterAsins.model_validate(data)
