class Author:
    def __init__(self, name, name_en=None, affiliation=None):
        self.author_id = None
        self.name = name
        self.name_en = name_en
        self.affiliation = affiliation

    def __str__(self):
        return str(self.name)
