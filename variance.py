import os
import xml.etree.ElementTree as ET
from student import Student
from score import Score
from judge import Judge

tree = ET.parse(os.environ['DATA_PATH'])
root = tree.getroot()

students = []

def populate_students():
    """
    Populate a list of students with names and empty scores
    """
    for debater in root.findall('ENTRY_STUDENT'):
        students.append(Student("{} {}".format(debater.find('FIRST').text,  debater.find('LAST').text),
                                debater.find('ID').text, []))


def add_scores_to_students():
    """
    Add scores to students in list
    """
    for score in root.findall('BALLOT_SCORE'):
        if score.find('SCORE_ID').text == "POINTS":
            for debater in students:
                if debater.id_num == score.find("RECIPIENT").text:
                    debater.scores.append(Score(score.find('SCORE').text, get_judge_issuing_score(score.find('BALLOT').text)))


def get_judge_issuing_score(ballot_id):
    """
    Get the Judge object of the judge who issued the score to the student
    :param ballot_id:
    :return:
    """
    for ballot in root.findall('BALLOT'):
        if ballot.find('ID').text == ballot_id:
            for judge in root.findall('JUDGE'):
                if judge.find('ID').text == ballot.find('JUDGE').text:
                    return Judge("{} {}".format(judge.find('FIRST').text, judge.find('LAST').text), None)


def get_students_with_high_variance():
    students_with_high_variance = []
    for student in students:
        numerical_scores = [score.numerical_score for score in student.scores]
        if int(max(numerical_scores)) - int(min(numerical_scores)) > 10:
            students_with_high_variance.append(student)
    return students_with_high_variance


if __name__ == '__main__':
    populate_students()
    add_scores_to_students()
    for student in get_students_with_high_variance():
        print(student)
