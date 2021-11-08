class Search:
    def __init__(self, url_filter, url_profile, id_search=None, text_filter=None, datetime=None, person_id=None):
        self.id = id_search
        self.url_filter = url_filter
        self.url_profile = url_profile
        self.datetime = datetime
        self.text_filter = text_filter
        self.person_id = person_id

    def __str__(self):
        return "Search: {} {} {} {} {} {}".format(
            self.id,
            self.url_filter,
            self.url_profile,
            self.text_filter,
            self.datetime,
            self.person_id
        )
