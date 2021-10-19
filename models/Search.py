class Search:
    def __init__(self, url, date=None, person_id=None):
        self.url = url
        self.date = date
        self.person_id = person_id

    def __str__(self):
        return "Search: {}".format(self.url, self.date, self.person_id)
