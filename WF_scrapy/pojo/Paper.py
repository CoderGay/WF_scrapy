class Paper:
    def __init__(self, DOI, title, abstract, latest_update_time, paper_url, authors, classification, fund=None,
                 keywords=None, pages=None, title_en=None, abstract_en=None):
        if keywords is None:
            keywords = []
        self.id = None
        self.DOI = DOI
        self.title = title
        self.title_en = title_en
        self.abstract = abstract
        self.abstract_en = abstract_en
        self.latest_update_time = latest_update_time
        self.paper_url = paper_url
        self.authors = authors
        self.classification = classification
        self.fund = fund
        self.keywords = keywords
        self.pages = pages

    def __str__(self):
        return str(self.title)+str(self.paper_url)+'\n'+str(self.abstract)+'\n'+str(self.authors)+'\n'+str(self.classification)+'\nhref = '+str(self.paper_url)
