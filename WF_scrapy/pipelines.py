# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from itemadapter import ItemAdapter
import pymysql
from WF_scrapy.items import PaperItem


# TODO 以下代码耦合性很强, 待整理
class WfScrapyPipeline(object):
    # TODO: You can optimize the code of Pipeline as follow:
    # def __init__(self):
    #     DB_MYSQL = None
    #     con = None
    #     cur = None

    def process_item(self, item, spider):
        DB_MYSQL = spider.settings.get('DB_MYSQL')
        con = pymysql.connect(**DB_MYSQL)
        cur = con.cursor()
        paper_id = 0

        if isinstance(item, PaperItem):
            paper_sql = (
                'insert into paper(DOI,title,title_en,abstract,abstract_en,latest_update_time,pages,paper_url) values (%s,%s,%s,%s,%s,%s,%s,%s)')
            paper_lis = (
                item['DOI'], item['title'], item['title_en'], item['abstract'],
                item['abstract_en'],
                item['latest_update_time'], int(item['pages']), item['paper_url'])
            # 查一下数据库有没有重复的
            if item['paper_url'] is not None:
                searchIdByUrl_sql = ('select paper_id from paper where paper_url= %s')
                query_lis = (item['paper_url'])
                cur.execute(searchIdByUrl_sql, query_lis)
                results = cur.fetchall()
                # 数据库没有重复的插入数据:
                if len(results) == 0:
                    try:
                        cur.execute(paper_sql, paper_lis)
                        cur.execute("select last_insert_id();")  # 查询自增序列PAPER_ID的值
                        insert_id_info = cur.fetchall()  # 获取自增序列PAPER_ID的值，获取 ID 必须在 commit 之前，否则获取为0
                        paper_id = int(insert_id_info[0][0])
                    except Exception as e:
                        print("===>Insert Error:", e)
                        con.rollback()
                    else:  # 没有出现异常
                        con.commit()
                else:
                    paper_id = int(results[0][0])

            # 开始插入`author`表
            author_sql = (
                'insert into author(name,name_en,affiliation_id) values (%s,%s,%s)')
            searchAuthorIdByName_sql = ('select author_id from author where name = %s and affiliation_id = %s')
            author_rs_sql = ('insert into author_rs(author_id,paper_id) values (%s,%s)')
            searchAursByDoubleId_sql = ('select aurs_id from author_rs where author_id = %s and paper_id = %s')
            try:
                for author in item['authors']:
                    # 获取作者的属性
                    author_name = author.name
                    author_name_en = author.name_en
                    author_affiliation = author.affiliation
                    # 开始插入`affiliation`表
                    affiliation_sql = (
                        'insert into affiliation(name) values (%s)')
                    searchAffIdByName_sql = ('select affiliation_id from affiliation where name = %s')
                    affiliation_rs_sql = ('insert into affiliation_rs(affiliation_id,paper_id) values (%s,%s)')
                    searchAffrsByDoubleId_sql = ('select affrs_id from affiliation_rs where affiliation_id = %s and paper_id = %s')
                    affiliation_id = 0
                    try:
                        # 获取发表单位的属性
                        affiliation_name = author_affiliation.name
                        affiliation_lis = (affiliation_name)
                        # 查询affiliation_name发表单位是否已在数据库中
                        query_affiliation_lis = (affiliation_name)
                        cur.execute(searchAffIdByName_sql, query_affiliation_lis)
                        results = cur.fetchall()
                        # 若该affiliation_name发表单位不在数据库中
                        if len(results) == 0:
                            # 则插入该发表单位进数据库中
                            cur.execute(affiliation_sql, affiliation_lis)
                            # 查询自增序列affiliation_id的值
                            cur.execute("select last_insert_id();")
                            # 获取最新的results
                            results = cur.fetchall()
                        # 获取affiliation表的相应affiliation_id
                        affiliation_id = results[0][0]
                        # 在多对多关系表affiliation_rs中插入该条记录
                        queryAffrs_lis = (int(affiliation_id), int(paper_id))
                        cur.execute(searchAffrsByDoubleId_sql, queryAffrs_lis)
                        results = cur.fetchall()
                        if len(results) == 0:
                            affrs_lis = (int(affiliation_id), int(paper_id))
                            cur.execute(affiliation_rs_sql, affrs_lis)
                    except Exception as e:
                        print("===>Insert Error:", e)
                        con.rollback()

                    # 重新回到插入`author`表的步骤
                    author_affiliation_id = affiliation_id
                    author_lis = (author_name, author_name_en, author_affiliation_id)
                    # 查询content分类是否已在数据库中
                    query_author_lis = (author_name, author_affiliation_id)
                    cur.execute(searchAuthorIdByName_sql, query_author_lis)
                    results = cur.fetchall()
                    # 若该name作者不在数据库中
                    if len(results) == 0:
                        # 则插入该作者进数据库中
                        cur.execute(author_sql, author_lis)
                        # 查询自增序列author_id的值
                        cur.execute("select last_insert_id();")
                        # 获取最新的results
                        results = cur.fetchall()
                    # 获取author表的相应author_id
                    author_id = results[0][0]
                    # 在多对多关系表author_rs中插入该条记录
                    queryAurs_lis = (int(author_id), int(paper_id))
                    cur.execute(searchAursByDoubleId_sql, queryAurs_lis)
                    results = cur.fetchall()
                    if len(results) == 0:
                        crs_lis = (int(author_id), int(paper_id))
                        cur.execute(author_rs_sql, crs_lis)
            except Exception as e:
                print("===>Insert Error:", e)
                con.rollback()

            # 开始插入`fund`表
            fund_sql = (
                'insert into fund(content,`type`) values (%s,%s)')
            searchIdByFund_sql = ('select fund_id from fund where content = %s')
            frs_sql = ('insert into fund_rs(fund_id,paper_id) values (%s,%s)')
            searchFrsByDoubleId_sql = ('select frs_id from fund_rs where fund_id = %s and paper_id = %s')
            try:
                for fund in item['funds']:
                    # 获取基金的属性
                    fund_content = fund.content
                    fund_type = fund.type
                    fund_lis = (fund_content, fund_type)
                    # 查询fund基金是否已在数据库中
                    query_fund_lis = (fund_content)
                    cur.execute(searchIdByFund_sql, query_fund_lis)
                    results = cur.fetchall()
                    # 若该fund基金不在数据库中
                    if len(results) == 0:
                        # 则插入该基金进数据库中
                        cur.execute(fund_sql, fund_lis)
                        # 查询自增序列classification_id的值
                        cur.execute("select last_insert_id();")
                        # 获取最新的results
                        results = cur.fetchall()
                    # 获取fund表的相应fund_id
                    fund_id = results[0][0]
                    # 在多对多关系表fund_rs中插入该条记录
                    queryFrs_lis = (int(fund_id), int(paper_id))
                    cur.execute(searchFrsByDoubleId_sql, queryFrs_lis)
                    results = cur.fetchall()
                    if len(results) == 0:
                        frs_lis = (int(fund_id), int(paper_id))
                        cur.execute(frs_sql, frs_lis)
            except Exception as e:
                print("===>Insert Error:", e)
                con.rollback()

            # 开始插入`keyword`表
            keyword_sql = (
                'insert into keyword(content) values (%s)')
            searchIdByKeyword_sql = ('select keyword_id from keyword where content = %s')
            krs_sql = ('insert into keyword_rs(keyword_id,paper_id) values (%s,%s)')
            searchKrsByDoubleId_sql = ('select krs_id from keyword_rs where keyword_id = %s and paper_id = %s')
            try:
                for keyword in item['keywords']:
                    # 获取关键词的属性
                    keyword_content = keyword.content
                    keyword_lis = (keyword_content)
                    # 查询keyword关键词是否已在数据库中
                    query_keyword_lis = (keyword_content)
                    cur.execute(searchIdByKeyword_sql, query_keyword_lis)
                    results = cur.fetchall()
                    # 若该keyword关键词不在数据库中
                    if len(results) == 0:
                        # 则插入该关键词进数据库中
                        cur.execute(keyword_sql, keyword_lis)
                        # 查询自增序列classification_id的值
                        cur.execute("select last_insert_id();")
                        # 获取最新的results
                        results = cur.fetchall()
                    # 获取keyword表的相应keyword_id
                    keyword_id = results[0][0]
                    # 在多对多关系表fund_rs中插入该条记录
                    queryKrs_lis = (int(keyword_id), int(paper_id))
                    cur.execute(searchKrsByDoubleId_sql, queryKrs_lis)
                    results = cur.fetchall()
                    if len(results) == 0:
                        krs_lis = (int(keyword_id), int(paper_id))
                        cur.execute(krs_sql, krs_lis)
            except Exception as e:
                print("===>Insert Error:", e)
                con.rollback()

            # 开始插入`classification`表
            classification_sql = (
                'insert into classification(content,note) values (%s,%s)')
            searchIdByContent_sql = ('select class_id from classification where content = %s')
            crs_sql = ('insert into classification_rs(class_id,paper_id) values (%s,%s)')
            searchCrsByDoubleId_sql = ('select crs_id from classification_rs where class_id = %s and paper_id = %s')
            try:
                for classification in item['classifications']:
                    # 获取分类的属性
                    content = classification.content
                    note = classification.note
                    classification_lis = (content, note)
                    # 查询content分类是否已在数据库中
                    query_lis = (content)
                    cur.execute(searchIdByContent_sql, query_lis)
                    results = cur.fetchall()
                    # 若该content分类不在数据库中
                    if len(results) == 0:
                        # 则插入该分类进数据库中
                        cur.execute(classification_sql, classification_lis)
                        # 查询自增序列classification_id的值
                        cur.execute("select last_insert_id();")
                        # 获取最新的results
                        results = cur.fetchall()
                    # 获取classification表的相应class_id
                    class_id = results[0][0]
                    # 在多对多关系表classification_rs中插入该条记录
                    queryCrs_lis = (int(class_id), int(paper_id))
                    cur.execute(searchCrsByDoubleId_sql, queryCrs_lis)
                    results = cur.fetchall()
                    if len(results) == 0:
                        crs_lis = (int(class_id), int(paper_id))
                        cur.execute(crs_sql, crs_lis)
            except Exception as e:
                print("===>Insert Error:", e)
                con.rollback()
            else:  # 没有出现异常,提交
                con.commit()
        cur.close()
        con.close()
        print("insert mysql is ok")
        return item

