# -*- coding: utf-8 -*-
from typing import Any
from pydantic import BaseModel, Field, field_validator
from lingxingapi_httpx.base.schema import ResponseV1, ResponseV1TraceId, FlattenDataRecords
from lingxingapi_httpx.fields import IntOrNone2Zero, FloatOrNone2Zero, StrOrNone2Blank


# 工具数据 ----------------------------------------------------------------------------------------------------------------------
# . Minitor Keywords
class MoniterKeyword(BaseModel):
    """关键词监控"""

    # 关键词监控ID [原字段 'id']
    moniter_id: int = Field(validation_alias="id")
    # 关键词 [原字段 'key_word']
    keyword: str = Field(validation_alias="key_word")
    # 关键词数量 [原字段 'keyword_num']
    keyword_count: int = Field(validation_alias="keyword_num")
    # 关键词备注 [原字段 'keyword_remark']
    keyword_note: str = Field(validation_alias="keyword_remark")
    # 监控终端 [原字段 'type']
    # (1: PC端, 2: 移动端)
    moniter_type: int = Field(validation_alias="type")
    # 监控国家 [原字段 'country']
    monitor_country: str = Field(validation_alias="country")
    # 监控邮编城市 [原字段 'postcode_name']
    monitor_city: str = Field(validation_alias="postcode_name")
    # 监控邮编 [原字段 'postcode']
    monitor_postcode: str = Field(validation_alias="postcode")
    # 监控排名类型 [原字段 'is_sponsored']
    # (0: 自然排名, 1: 广告排名)
    rank_type: int = Field(validation_alias="is_sponsored")
    # 关键词排名
    rank: int
    # 关键词排名页面 [原字段 'page']
    page: int = Field(validation_alias="page")
    # 关键词页面排名 [原字段 'current_page_rank']
    page_rank: int = Field(validation_alias="current_page_rank")
    # 关键词排名描述 [原字段 'rank_text']
    rank_desc: str = Field(validation_alias="rank_text")
    # SBV广告排名页面 [原字段 'sbv_page']
    sbv_page: int = Field(validation_alias="sbv_page")
    # SBV广告排名描述 [原字段 'sbv_text']
    sbv_desc: str = Field(validation_alias="sbv_text")
    # 关键词ASIN
    asin: str
    # 关键词父ASIN
    parent_asin: str
    # ASIN标题
    title: str
    # ASIN备注 [原字段 'asin_remark']
    asin_note: str = Field(validation_alias="asin_remark")
    # 监控创建人
    monitor_creator_name: str = Field(validation_alias="creator")
    # 监控人列表
    monitor_user_names: list[str] = Field(validation_alias="monitors")
    # ASIN监控创建时间 [原字段 'asin_create_time']
    monitor_asin_create_time: str = Field(validation_alias="asin_create_time")
    # 关键词监控创建时间 [原字段 'create_time']
    monitor_keyword_create_time: str = Field(validation_alias="create_time")
    # 监控更新时间 [原字段 'monitor_time']
    update_time: str = Field(validation_alias="monitor_time")


class MoniterKeywords(ResponseV1):
    """关键词监控列表"""

    data: list[MoniterKeyword]


# . Product Asins
class SubcategoryRank(BaseModel):
    """小类目排名"""

    # 小类目名称 [原字段 'small_category_text']
    subcategory: str = Field(validation_alias="small_category_text")
    # 小类目排名 [原字段 'small_rank']
    subcategory_rank: int = Field(validation_alias="small_rank")
    # 小类目初始排名 [原字段 'init_small_rank']
    subcategory_init_rank: int = Field(validation_alias="init_small_rank")


class MinitorAsin(BaseModel):
    """ASIN监控"""

    # fmt: off
    # 监控状态 (0: 关闭, 1: 开启)
    monitor_status: int
    # 监控等级 (1: A, 2: B, 3: C, 4: D) [原字段 'level_name']
    monitor_level: str = Field(validation_alias="level_name")
    # 领星站点ID
    mid: int
    # 监控ASIN
    asin: str
    # 父ASIN [原字段 'parent']
    parent_asin: StrOrNone2Blank = Field(validation_alias="parent")
    # 关联的子ASIN列表 [原字段 'children']
    child_asins: list[str] = Field(validation_alias="children")
    # ASIN链接
    asin_url: StrOrNone2Blank 
    # 商品主图 [原字段 'main_image']
    image_url: StrOrNone2Blank = Field(validation_alias="main_image")
    # ASIN所属类目列表 [原字段 'category_list']
    asin_categories: list[str] = Field(validation_alias="category_list")
    # 商品价格
    price: FloatOrNone2Zero
    # 商品价格货币符号 [原字段 'currency']
    price_currency_icon: StrOrNone2Blank = Field(validation_alias="currency")
    # BuyBox当前价格
    buybox_price: FloatOrNone2Zero
    # BuyBox初始价格 [原字段 'init_buybox_price']
    buybox_init_price: FloatOrNone2Zero = Field(validation_alias="init_buybox_price")
    # BuyBox价格货币符号 [原字段 'buybox_currency']
    buybox_currency_icon: StrOrNone2Blank = Field(validation_alias="buybox_currency")
    # BuyBox美元价格
    buybox_usd_price: FloatOrNone2Zero
    # 30天平均价格 [原字段 'avg_price']
    price_avg_30d: FloatOrNone2Zero = Field(validation_alias="avg_price")
    # 30天平均价格货币符号 [原字段 'avg_currency']
    price_avg_currency_icon: StrOrNone2Blank = Field(validation_alias="avg_currency")
    # 30天预估销量 [原字段 'bought_num']
    sales_qty_30d: IntOrNone2Zero = Field(validation_alias="bought_num")
    # 评论分 [原字段 'star']
    review_score: StrOrNone2Blank = Field(validation_alias="star")
    # 评论数 [原字段 'review_num']
    review_count: StrOrNone2Blank = Field(validation_alias="review_num")
    # 大类目名称 [原字段 'big_category']
    category: StrOrNone2Blank = Field(validation_alias="big_category")
    # 大类目排名 [原字段 'big_category_rank']
    category_rank: StrOrNone2Blank = Field(validation_alias="big_category_rank")
    # 大类目初始排名 [原字段 'init_big_category_rank']
    category_init_rank: IntOrNone2Zero = Field(validation_alias="init_big_category_rank")
    # 小类目排名 [原字段 'small_ranks']
    subcategories: list[SubcategoryRank] = Field(validation_alias="small_ranks")
    # FBA卖家数量 [原字段 'fba_seller_num']
    fba_seller_count: IntOrNone2Zero = Field(validation_alias="fba_seller_num")
    # 初始FBA卖家数量 [原字段 'init_fba_seller_num']
    fba_seller_init_count: IntOrNone2Zero = Field(validation_alias="init_fba_seller_num")
    # FBM卖家数量 [原字段 'fbm_seller_num']
    fbm_seller_count: IntOrNone2Zero = Field(validation_alias="fbm_seller_num")
    # 初始FBM卖家数量 [原字段 'init_fbm_seller_num']
    fbm_seller_init_count: IntOrNone2Zero = Field(validation_alias="init_fbm_seller_num")
    # 商品重量
    item_weight: StrOrNone2Blank
    # 商品尺寸
    product_dimensions: str
    # 搜索词
    search_term: str
    # 最新更新事件列表 [原字段 'last_update_event']
    latest_update_events: list[str] = Field(validation_alias="last_update_event")
    # 商品图片列表 [原字段 'thumbnail']
    images: list[str] = Field(validation_alias="thumbnail")
    # 商品标题
    title: str
    # 商品卖点 [原字段 'featurebullets']
    bullet_points: list[str] = Field(validation_alias="featurebullets")
    # 监控创建人ID [原字段 'creator_uid']
    creator_id: str = Field(validation_alias="creator_uid")
    # 监控创建人名称 [原字段 'creator']
    creator_name: str = Field(validation_alias="creator")
    # 监控人ID列表 [原字段 'monitor_uids']
    monitor_user_ids: list[str] = Field(validation_alias="monitor_uids")
    # fmt: on


class MoniterAsins(ResponseV1):
    """ASIN监控列表"""

    data: list[MinitorAsin]
