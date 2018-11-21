import os
from xml.etree import ElementTree as ET

from judge import Judge
from score import Score
from student import Student


class Report(object):
    students = []
    scores = []
    tree = ET.parse(os.environ['DATA_PATH'])
    root = tree.getroot()

    def __init__(self):
        self.populate_students()
        self.add_scores_to_students()
        self.make_score_list()

    def populate_students(self):
        """
        Populate a list of students with names and empty scores
        """
        for debater in self.root.findall('ENTRY_STUDENT'):
            self.students.append(Student("{} {}".format(debater.find('FIRST').text, debater.find('LAST').text),
                                    debater.find('ID').text, []))

    def add_scores_to_students(self):
        """
        Add scores to students in list
        """
        for score in self.root.findall('BALLOT_SCORE'):
            if score.find('SCORE_ID').text == "POINTS":
                for debater in self.students:
                    if debater.id_num == score.find("RECIPIENT").text:
                        debater.scores.append(Score(score.find('SCORE').text, self.get_judge_issuing_score(score.find('BALLOT').text)))

    def make_score_list(self):
        for student in self.students:
            for score in student.scores:
                self.scores.append(float(score.numerical_score))

    def get_judge_issuing_score(self, ballot_id):
        """
        Get the Judge object of the judge who issued the score to the student
        :param ballot_id:
        :return:
        """
        for ballot in self.root.findall('BALLOT'):
            if ballot.find('ID').text == ballot_id:
                for judge in self.root.findall('JUDGE'):
                    if judge.find('ID').text == ballot.find('JUDGE').text:
                        return Judge("{} {}".format(judge.find('FIRST').text, judge.find('LAST').text), None)

    def get_students_with_high_variance(self, var):
        """
        Generate a list of students with point variance above a certain value
        :param var: non-inclusive minimum point difference for inclusion in list
        :return: list of students with variance above a certain point value (param var)
        """
        students_with_high_variance = []
        for student in self.students:
            numerical_scores = [score.numerical_score for score in student.scores]
            if int(max(numerical_scores)) - int(min(numerical_scores)) > var:
                students_with_high_variance.append(student)
        return students_with_high_variance

    def get_varied_to_normal_ratio(self, var):
        """

        :param var:
        :return:
        """
        return len(self.get_students_with_high_variance(var)) / len(self.students)


if __name__ == '__main__':
    report = Report()

    # Print detailed report with student/judge names and scores
    print("Students with point variance > 10:\n")
    for student in report.get_students_with_high_variance(10):
        print(student)

    # Print point variance ratio for given min flag values
    for var in [5, 10, 15]:
        print("Number of students with point variance > {}: {:.2%}\n".format(var, report.get_varied_to_normal_ratio(var)))

    # Print mean and median score
    print("Mean score: {:.2f}".format(sum(report.scores) / len(report.scores)))
    print("Median score: {:.2f}".format(sorted(report.scores)[int(len(report.scores)/2)]))
