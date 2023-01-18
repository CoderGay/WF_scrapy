# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 此处可视为ORMapping中的Object,不适宜细分类class, 建议按照以往先验知识将其视作一个Item对象
class PaperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # paper_id = scrapy.Field()

    # `paper` relation field
    DOI = scrapy.Field()
    title = scrapy.Field()
    title_en = scrapy.Field()
    abstract = scrapy.Field()
    abstract_en = scrapy.Field()
    latest_update_time = scrapy.Field()
    pages = scrapy.Field()
    paper_url = scrapy.Field()

    # `classification` relation field
    # classifications is a list[Classification]
    classifications = scrapy.Field()

    # `author` relation field
    # authors is a list[Author]
    authors = scrapy.Field()

    # `author` relation field
    # authors is a list[Author]
    funds = scrapy.Field()

    # `author` relation field
    # authors is a list[Author]
    keywords = scrapy.Field()

    # `affiliations` relation field
    # affiliations is a list[Affiliation]


# class AuthorItem(scrapy.Item):
#     # define the fields for your item here like:
#     name = scrapy.Field()
#     name_en = scrapy.Field()
#
#
# class AffiliationItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass
#
#
# class KeywordItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass
#
#
# class ClassificationItem(scrapy.Item):
#     # define the fields for your item here like:
#     content = scrapy.Field()
#     note = scrapy.Field()
#     pass
#
#
# class FundItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass
