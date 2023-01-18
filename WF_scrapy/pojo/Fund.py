class Fund:
    def __init__(self, content):
        self.fund_id = None
        self.content = content
        fund_type = '普通'
        if ("国家自然科学基金" or "国家重点研发项目") in content:
            fund_type = '国家级'
        elif ("省" or "部" or "委员会" or "科技厅") in content:
            fund_type = '省部级'
        elif ("市" or "厅" or "局") in content:
            fund_type = '厅局级'
        self.type = fund_type
