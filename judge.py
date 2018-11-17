class Judge(object):

    name = ""
    scores = None

    def __init__(self, name, scores):
        self.name = name
        self.scores = scores

    def __str__(self):
        return self.name