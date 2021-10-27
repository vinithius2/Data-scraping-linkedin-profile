class Education:
    def __init__(self, college, level, course):
        self.college = college
        self.level = level
        self.course = course

    def __str__(self):
        return "Education: {}".format(self.college, self.level, self.course)
