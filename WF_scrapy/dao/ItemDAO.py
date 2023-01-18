from typing import List

from WF_scrapy.pojo.Paper import Paper
from WF_scrapy.items import *


def convertPaperItem(paper) -> PaperItem:
    item = PaperItem()
    item['DOI'] = paper.DOI
    item['title'] = paper.title
    item['title_en'] = '' if paper.title_en is None else paper.title_en
    item['abstract'] = paper.abstract
    item['abstract_en'] = '' if paper.abstract_en is None else paper.abstract_en
    item['latest_update_time'] = paper.latest_update_time
    item['pages'] = int(str(paper.pages).split('(')[0].strip())
    item['paper_url'] = paper.paper_url

    item['classifications'] = paper.classification  # No error, my bro.
    item['authors'] = paper.authors  # No error, my bro.
    item['funds'] = paper.fund
    item['keywords'] = paper.keywords
    return item


# def convertAuthorItem(paper) -> List[AuthorItem]:
#     authors = paper.authors
#     items = []
#     for author in authors:
#         item = AuthorItem()
#         item['name'] = author.name
#         item['name_en'] = '' if author.name_en is None else author.name_en
#         items.append(item)
#         # TODO 待补充
#     return items
#
#
# def convertClassificationItem(paper) -> List[ClassificationItem]:
#     classifications = paper.classification
#     items = []
#     Author : 林俊杰
#     Date: 2023/1/3
#     for classification in classifications:
#         item = ClassificationItem()
#         item['content'] = classification.content
#         item['note'] = classification.note
#         items.append(item)
#     return items


class ItemDAO:
    def __init__(self):
        pass
