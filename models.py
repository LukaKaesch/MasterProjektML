class Product:
    def __init__(self, title, link):
        self.link = link
        self.title = title

    def is_already_saved(self, list):
        for l in list:
            if self.title == l.title:
                return True
        return False

