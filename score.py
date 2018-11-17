class Score(object):

    numerical_score = 0
    round = 0
    issued_by = None

    def __init__(self, numerical_score, round, issued_by):
        self.numerical_score = numerical_score
        self.round = round
        self.issued_by = issued_by
