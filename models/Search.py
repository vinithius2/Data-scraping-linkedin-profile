class Search:
    def __init__(self, url_filter, url_profile, score=None, datetime=None, person_id=None):
        self.url_filter = url_filter
        self.url_profile = url_profile
        self.datetime = datetime
        self.score = score
        self.person_id = person_id

    def __str__(self):
        return "Search: {} {} {} {} {}".format(
            self.url_filter,
            self.url_profile,
            self.score,
            self.datetime,
            self.person_id
        )
