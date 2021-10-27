class Person:
    def __init__(self, name=None, subtitle=None, local=None, about=None, url=None, email=None, phone_number=None,
                 certifications=[], education=[], experiences=[], languages=[], skills=[]):
        self.name = name
        self.subtitle = subtitle
        self.local = local
        self.about = about
        self.url = url
        self.email = email
        self.phone_number = phone_number
        self.certifications = certifications
        self.education = education
        self.experiences = experiences
        self.languages = languages
        self.skills = skills

    def __str__(self):
        return "Person: {} {} {} {} {} {} {} {} {} {} {} {}".format(
            self.name,
            self.subtitle,
            self.local,
            self.about,
            self.url,
            self.email,
            self.phone_number,
            self.certifications,
            self.education,
            self.experiences,
            self.languages,
            self.skills
        )
