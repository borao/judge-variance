class Score(object):

    numerical_score = 0
    issued_by = None

    def __init__(self, numerical_score, issued_by):
        self.numerical_score = numerical_score
        self.round = round
        self.issued_by = issued_by

    def __str__(self):
        return "{} ({})".format(self.numerical_score, self.issued_by)
