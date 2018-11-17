import os
import xml.etree.ElementTree as ET
from student import Student
from score import Score

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
                    debater.scores.append(Score(score.find('SCORE').text, 0, None))


if __name__ == '__main__':
    populate_students()
    add_scores_to_students()