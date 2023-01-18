# TODO 此处先用简单的工具类方法进行，后续整理代码将其整理为适配类Adapter
from typing import List

from WF_scrapy.pojo.Affiliation import Affiliation
from WF_scrapy.pojo.Author import Author


def convertAuthor(authorList, affiliationList) -> List[Author]:
    affiliationDict = {}
    # resList = []  # 节省一下内存空间, 试下能不能用原来的列表
    for affiliation in affiliationList:
        try:
            index = str(affiliation.name).split('.')[0]
            affiliation.name = str(affiliation.name).split('.')[-1]
            affiliationDict[index] = affiliation
        except Exception as e:
            print('Affiliation分割.失败:', e)

    for author in authorList:
        try:
            code = str(author.name).split('\n')[1]
            author.name = str(author.name).split('\n')[0]
            author.affiliation = affiliationDict[code]
        except Exception as e:
            print('Author分割回车失败:', e)
            if len(affiliationList) == 1:
                author.affiliation = affiliationList[0]
            else:
                author.affiliation = Affiliation('unknown')

    return authorList
