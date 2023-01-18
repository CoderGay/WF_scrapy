class Classification:
    def __init__(self, content, note=None):
        self.class_id = None
        if "(" in content:
            note = content.split('(')[1][:-1]
            content = content.split('(')[0]
        self.content = content
        self.note = note
