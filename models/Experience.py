class Experience:
    def __init__(self, company, position, years, months, description):
        self.company = company
        self.position = position
        self.years = years
        self.months = months
        self.description = description

    def __str__(self):
        return "Experience: {} {} {} {} {}".format(self.company, self.position, self.years, self.months, self.description)
